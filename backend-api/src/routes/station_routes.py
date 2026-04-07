from flask import Blueprint, jsonify
from src.services.station_service import get_all_stations, get_station_details
from flask_jwt_extended import get_jwt_identity, jwt_required

station_bp = Blueprint("stations", __name__)

@station_bp.route('/stations', methods=['GET'])
def list_stations():
    """
    Lista todas as estações cadastradas
    ---
    tags:
      - Estações
    responses:
      200:
        description: Lista de estações retornada com sucesso
        schema:
          type: array
          items:
            type: object
            properties:
              rcId:
                type: integer
                example: 1
              name:
                type: string
                example: Colégio João XXIII
              local:
                type: string
                example: R. Sepé Tiarajú, 1013 - Santa Tereza, Porto Alegre
      404:
        description: Nenhuma estação cadastrada
      500:
        description: Erro interno do servidor
    """
    try:
        stations = get_all_stations()

        if stations is None:
            return jsonify({
                "message": "No monitoring stations registered."
            }), 404

        return jsonify(stations), 200

    except Exception:
        return jsonify({
            "error": "Internal server error while fetching monitoring stations."
        }), 500


@station_bp.route("/stations/details", methods=["GET"])
@jwt_required()
def list_stations_details():
    """
    Retorna detalhes completos das estações
    ---
    tags:
      - Estações
    security:
      - Bearer: []
    responses:
      200:
        description: Detalhes completos
        schema:
          type: array
          items:
            type: object
            properties:
              contact:
                type: string
                example: +55 11 99999-9999
              name:
                type: string
                example: Colégio João XXIII
              local:
                type: string
                example: R. Sepé Tiarajú, 1013 - Santa Tereza, Porto Alegre
              latitude:
                type: number
                format: float
                example: -30.0277
              longitude:
                type: number
                format: float
                example: -51.2296
              email:
                type: string
                example: admin@estacao.com
              height:
                type: number
                example: 760
              height_sea_level:
                type: number
                example: 760
              status:
                type: string
                example: Offline - Verifique se a estação está ligada!
              rcId:
                type: integer
                example: 1
              timestamp:
                type: string
                format: date-time
                example: 2024-06-01T12:00:00Z
      401:
        description: Token inválido ou ausente
      404:
        description: Estação não encontrada
      500:
        description: Erro interno do servidor
    """
    try:
        user_id = get_jwt_identity()
        stations = get_station_details(user_id)

        if stations is None:
            return jsonify({
                "message": "No monitoring stations registered."
            }), 404

        return jsonify(stations), 200
    
    except Exception:
        return jsonify({
            "error": "Internal server error while fetching monitoring stations."
        }), 500

