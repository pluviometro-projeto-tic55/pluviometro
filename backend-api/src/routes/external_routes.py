from flask import Blueprint, jsonify
from ..services.external_weather_service import get_station_coordinates, get_external_weather_values

external_bp = Blueprint("external", __name__)

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
            api_pressure, api_temp, api_humidity, api_wind, api_rain = external_data
            external_data = {
                "external_pressure": api_pressure,
                "external_temperature": api_temp,
                "external_humidity": api_humidity,
                "external_wind_speed": api_wind,
                "external_rain_chance": api_rain
            }

        return jsonify(external_data), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    except ConnectionError:
        return jsonify({
            "error": "The external API is temporarily unavailable. Please try again later."
        }), 503

    except Exception:
        return jsonify({"error": "Internal server error."}), 500