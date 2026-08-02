from flask import Blueprint, jsonify
from ..services.forecast_services import get_station_data_by_id
from ..var import get_cached_forecast, predict_weekly_weather
import logging

forecast_bp = Blueprint('data', __name__)
logger = logging.getLogger(__name__)

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

      # Fallback: tenta gerar na hora quando cache estiver ausente.
      if forecast_data is None:
        forecast_data = predict_weekly_weather(rc_id)

      if not forecast_data or not forecast_data.get("daily_summary"):
        return jsonify({"message": "Previsão não disponível."}), 404

      return jsonify(forecast_data), 200
    
    except Exception as e:
        logger.error(f"Error fetching forecast: {str(e)}", exc_info=True)
        return jsonify({"error": "Internal server error."}), 500