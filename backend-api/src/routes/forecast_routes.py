from flask import Blueprint, jsonify, request, Response
from ..services.forecast_services import get_station_data_by_id
from ..var import get_cached_forecast
from ..database import db
from sqlalchemy import func, and_
from datetime import datetime, timedelta
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
        from ..models import Forecast
        
        # Buscar 4 primeiros registros (00:00) dos próximos 4 dias
        forecasts = db.session.query(Forecast).filter(
            and_(
                Forecast.rcID == rc_id,
                func.hour(Forecast.timestamp) == 0,
                Forecast.timestamp >= datetime(2026, 5, 25),
                Forecast.timestamp <= datetime(2026, 5, 28)
            )
        ).order_by(Forecast.timestamp).limit(4).all()
        
        if not forecasts:
            return jsonify({"message": "Previsão não disponível."}), 404
        
        # Transformar para formato esperado pelo frontend
        daily_summary = []
        weekdays = ["segunda-feira", "terça-feira", "quarta-feira", "quinta-feira", "sexta-feira"]
        
        for idx, forecast in enumerate(forecasts):
            date_str = forecast.timestamp.strftime("%Y-%m-%d")
            
            daily_summary.append({
                "date": date_str,
                "max_temp": int(forecast.temp_max) if forecast.temp_max else 0,
                "min_temp": int(forecast.temp_min) if forecast.temp_min else 0,
                "heat_index": int(forecast.temp_max) if forecast.temp_max else 0,
                "avg_wind_speed": int(forecast.c_wind_speed) if forecast.c_wind_speed else 0,
                "cloudiness": 0,
                "description": forecast.general_summary or "N/A"
            })
        
        return jsonify({"daily_summary": daily_summary}), 200
    
    except Exception as e:
        logger.error(f"Error fetching forecast: {str(e)}", exc_info=True)
        return jsonify({"error": "Internal server error."}), 500