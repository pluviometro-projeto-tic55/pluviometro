from flask import Blueprint, jsonify
from ..services.forecast_services import get_station_data_by_id
from ..var import get_cached_forecast, predict_weekly_weather
from ..services.external_weather_service import get_station_coordinates, get_external_weather_values
import logging

forecast_bp = Blueprint('data', __name__)
logger = logging.getLogger(__name__)


def _enrich_daily_summary_with_external_rain(rc_id, forecast_data):
  """
  Enriquecimento opcional: usa a previsão externa de chuva (mm/%)
  para os próximos dias e anexa ao daily_summary por data.
  """
  if not forecast_data or not forecast_data.get("daily_summary"):
    return forecast_data

  try:
    latitude, longitude = get_station_coordinates(rc_id)
    external_tuple = get_external_weather_values(latitude, longitude)

    # Índice 6 no tuple é forecast_4days
    forecast_4days = external_tuple[6] if isinstance(external_tuple, tuple) and len(external_tuple) > 6 else None
    if not forecast_4days:
      return forecast_data

    external_by_date = {
      item.get("date"): item
      for item in forecast_4days
      if item.get("date")
    }

    for day in forecast_data["daily_summary"]:
      day_date = day.get("date")
      external_day = external_by_date.get(day_date)
      if not external_day:
        continue

      if external_day.get("rain_mm") is not None:
        day["rain_mm"] = external_day.get("rain_mm")

      if external_day.get("rain_chance") is not None:
        day["rain_chance"] = external_day.get("rain_chance")

    return forecast_data

  except Exception as exc:
    # Não derruba o endpoint de forecast quando a API externa falhar.
    logger.warning(f"Could not enrich forecast rain from external API: {exc}")
    return forecast_data

@forecast_bp.route('/stations/<int:rc_id>/current', methods=['GET'])
def get_data_details(rc_id):
    """
    Retorna os dados climáticos atuais de uma estação
    ---
    tags:
      - Dados Climáticos
    parameters:
      - name: rc_id
        in: path
        type: integer
        required: true
        description: ID da estação
    responses:
      200:
        description: Dados da estação retornados com sucesso
      404:
        description: Estação não encontrada ou sem dados
    """
    try:
        data = get_station_data_by_id(rc_id)

        if data is None:
          return jsonify({"error": "Station ID not found or data unavailable."}), 404

        return jsonify(data), 200
    
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    except Exception as e:
        return jsonify({"error": "Internal server error."}), 500


@forecast_bp.route('/stations/<int:rc_id>/comparison', methods=['GET'])
def get_station_comparison(rc_id):
    """
    Retorna os dados climáticos da estação em modo bruto (raw_local=True)
    para o modal de comparação com a API externa.
    ---
    tags:
      - Dados Climáticos
    parameters:
      - name: rc_id
        in: path
        type: integer
        required: true
        description: ID da estação
    responses:
      200:
        description: Dados de comparação retornados com sucesso
      404:
        description: Estação não encontrada ou sem dados
    """
    try:
        data = get_station_data_by_id(rc_id, raw_local=True)

        if data is None:
          return jsonify({"error": "Station ID not found or data unavailable."}), 404

        return jsonify(data), 200
    
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    except Exception as e:
        logger.error(f"Error fetching comparison data: {str(e)}", exc_info=True)
        return jsonify({"error": "Internal server error."}), 500


@forecast_bp.route('/stations/<int:rc_id>/forecast', methods=['GET'])
def get_station_forecast(rc_id):
    """
    Retorna previsão de 4 dias do modelo VAR.
    Busca um registro por dia do banco de dados.
    ---
    tags:
      - Dados Climáticos
    parameters:
      - name: rc_id
        in: path
        type: integer
        required: true
        description: ID da estação
    responses:
      200:
        description: Dados da previsão retornados com sucesso
      404:
        description: Nenhuma previsão encontrada
    """
    try:
      # Prioriza cache gerado pelo scheduler (fonte principal da previsao no frontend).
      forecast_data = get_cached_forecast(rc_id)

      # Compatibilidade: cache antigo sem rain_mm no resumo diario deve ser regenerado.
      if (
        forecast_data
        and forecast_data.get("daily_summary")
        and "rain_mm" not in forecast_data["daily_summary"][0]
      ):
        forecast_data = None

      # Fallback: tenta gerar na hora quando cache estiver ausente.
      if forecast_data is None:
        forecast_data = predict_weekly_weather(rc_id)

      if not forecast_data or not forecast_data.get("daily_summary"):
        return jsonify({"message": "Previsão não disponível."}), 404

      forecast_data = _enrich_daily_summary_with_external_rain(rc_id, forecast_data)

      return jsonify(forecast_data), 200
    
    except Exception as e:
        logger.error(f"Error fetching forecast: {str(e)}", exc_info=True)
        return jsonify({"error": "Internal server error."}), 500