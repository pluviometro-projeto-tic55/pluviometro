from flask import Blueprint, jsonify
import logging
from ..services.external_weather_service import get_station_coordinates, get_external_weather_values

external_bp = Blueprint("external", __name__)
logger = logging.getLogger(__name__)

@external_bp.route('/stations/<int:rc_id>/external/current', methods=['GET'])
def get_external_data(rc_id):
    """
    Retorna os dados meteorológicos atuais de uma API externa com base na localização da estação.
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
        description: Dados meteorológicos externos obtidos com sucesso
        schema:
          type: object
          properties:
            external_pressure:
              type: number
            external_temperature:
              type: number
            external_humidity:
              type: number
            external_wind_speed:
              type: number
            external_rain_chance:
              type: number
      400:
        description: Estação inválida
      503:
        description: API externa temporariamente indisponível
      500:
        description: Erro interno do servidor
    """
    try:
        latitude, longitude = get_station_coordinates(rc_id)
        external_data = get_external_weather_values(latitude, longitude)

        if isinstance(external_data, tuple):
            (
                api_pressure,
                api_temp,
                api_humidity,
                api_wind,
                api_rain,
                api_rain_mm,
                forecast_4days,
                api_luminosity,
                api_uv_index,
                api_is_day,
                api_condition,
                api_last_updated_epoch,
                api_sunrise,
                api_sunset,
            ) = external_data

            external_data = {
                "external_pressure": api_pressure,
                "external_temperature": api_temp,
                "external_humidity": api_humidity,
                "external_wind_speed": api_wind,
                "external_rain_chance": api_rain,
                "external_rain_mm": api_rain_mm,
                "forecast_4days": forecast_4days,
                "external_luminosity": api_luminosity,
                "external_uv_index": api_uv_index,
                "external_is_day": api_is_day,
                "external_condition": api_condition,
                "external_last_updated_epoch": api_last_updated_epoch,
                "external_sunrise": api_sunrise,
                "external_sunset": api_sunset,
            }

        return jsonify(external_data), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    except ConnectionError as e:
        logger.error(f"API Connection Error: {e}")
        return jsonify({
            "error": "The external API is temporarily unavailable. Please try again later."
        }), 503

    except Exception as e:
        logger.error(f"Unexpected error: {type(e).__name__}: {e}", exc_info=True)
        return jsonify({"error": "Internal server error."}), 500