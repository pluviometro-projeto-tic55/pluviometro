from flask import Blueprint, jsonify, request, Response
from ..services.forecast_services import get_station_data_by_id
from ..var import get_cached_forecast

forecast_bp = Blueprint('data', __name__)

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
    Retorna a última previsão meteorológica em cache para a estação.
    Permite que o frontend carregue a previsão imediatamente.
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
        description: Nenhuma previsão em cache encontrada
    """
    data = get_cached_forecast(rc_id)
    
    if data:
        return jsonify(data), 200
    
    return jsonify({"message": "Previsão não disponível no momento. Aguarde a próxima atualização."}), 404