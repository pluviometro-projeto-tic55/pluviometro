from flask import Blueprint, jsonify, request, Response
from ..services.history_service import export_historical_variable_csv, get_historical_hourly_average

history_bp = Blueprint('history', __name__)

@history_bp.route('/stations/<int:rc_id>/history/export', methods=['GET'])
def get_historical_single_variable(rc_id):
    """
    Exporta o histórico de uma variável climática em formato CSV
    ---
    tags:
      - Dados Climáticos
    produces:
      - text/csv
    parameters:
      - name: rc_id
        in: path
        type: integer
        required: true
        description: ID da estação
        example: 1

      - name: variable
        in: query
        type: string
        required: true
        description: Variável climática a ser exportada
        enum:
          - temp
          - humidity
          - pressure
          - wind_speed

      - name: start_date
        in: query
        type: string
        format: date
        required: true
        description: Data inicial (YYYY-MM-DD)
        example: 2026-01-01

      - name: end_date
        in: query
        type: string
        format: date
        required: true
        description: Data final (YYYY-MM-DD)
        example: 2026-01-07

    responses:
      200:
        description: |
          Arquivo CSV para download contendo:
          - Data (YYYY-MM-DD)
          - Hora (HH:MM)
          - Valor da variável selecionada
        
        headers:
          Content-Disposition:
            type: string
            description: attachment; filename="{variable}_{start_date}_{end_date}.csv"

      400:
        description: Parâmetros inválidos ou ausentes

      500:
        description: Erro interno do servidor
    """
    try:
        variable = request.args.get("variable", type=str)
        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")

        # validação de parâmetros
        if not all([rc_id, variable, start_date, end_date]):
            return jsonify({"error": "Invalid or missing parameters (rc_id, variable, start_date, end_date)."}), 400

        csv_data, filename = export_historical_variable_csv(
            rc_id=rc_id,
            variable=variable,
            start_date=start_date,
            end_date=end_date
        )

        response = Response(
            csv_data,
            mimetype="text/csv; charset=utf-8-sig",
            headers={
                "Content-Disposition": f'attachment; filename="{filename}"'
            }
        )

        response.headers["Access-Control-Expose-Headers"] = "Content-Disposition"
        return response, 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    except Exception as e:
        return jsonify({"error": "Internal server error."}), 500


@history_bp.route('/stations/<int:rc_id>/history', methods=['GET'])
def get_hourly_average_history(rc_id):
    """
    Retorna médias horárias por dia de uma variável climática
    ---
    tags:
      - Dados Climáticos
    parameters:
      - name: rc_id
        in: path
        type: integer
        required: true
        description: ID da estação
        example: 1

      - name: variable
        in: query
        type: string
        required: true
        description: Variável climática
        enum:
          - temp
          - humidity
          - pressure
          - wind_speed

      - name: start_date
        in: query
        type: string
        required: true
        format: date
        description: Data inicial (YYYY-MM-DD)
        example: 2026-01-04

      - name: end_date
        in: query
        type: string
        required: true
        format: date
        description: Data final (YYYY-MM-DD)
        example: 2026-01-07

    responses:
      200:
        description: Lista de médias horárias por dia
        schema:
          type: array
          items:
            type: object
            properties:
              day:
                type: string
                example: 2026-01-04
              avgHour:
                type: integer
                example: 3
              temperature:
                type: number
                example: 25.4
              humidity:
                type: number
                example: 63.2
              pressure:
                type: number
                example: 1013.5
              wind_speed:
                type: number
                example: 12.3

      400:
        description: Parâmetros inválidos
      500:
        description: Erro interno do servidor
    """

    try:
        variable = request.args.get("variable", type=str)
        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")

        if not all([rc_id, variable, start_date, end_date]):
          return jsonify({"error": "Invalid or missing parameters (rc_id, variable, start_date, end_date)."}), 400

        data = get_historical_hourly_average(
            rc_id=rc_id,
            variable=variable,
            start_date=start_date,
            end_date=end_date
        )

        return jsonify(data), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    except Exception as e:
      return jsonify({"error": "Internal server error."}), 500

