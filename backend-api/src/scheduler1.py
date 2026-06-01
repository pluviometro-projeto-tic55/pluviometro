#scheduler que vai automaticamente chamar as principais funções da API

from apscheduler.schedulers.background import BackgroundScheduler
from flask import current_app
from datetime import datetime
from .services.forecast_services import get_station_data_by_id
from .var import predict_weekly_weather
from .models import RaspClient
from . import socketio, db
from .var import train_and_save_model

def broadcast_weather_data(app):

# pega todas as estações registradas
    with app.app_context():

        stations = RaspClient.query.with_entities(RaspClient.rcID).all()

        for station in stations:
            rc_id = station.rcID
            data = get_station_data_by_id(rc_id)

            if data:

                socketio.emit(f'update_weather_{rc_id}', data)
                print(f"Broadcasted data for station {rc_id}") #teste

# gera a previsão e envia via socket
def broadcast_forecast_data(app):

    with app.app_context():
        # faz um loop por todas as estações registradas e faz a previsão delas
        try:
            stations = RaspClient.query.with_entities(RaspClient.rcID).all()

            for station in stations:
                rc_id = station.rcID
                
                # gera a previsão usando a função do var.py
                forecast_data = predict_weekly_weather(rc_id)

                if forecast_data:
                    socketio.emit(f'update_forecast_{rc_id}', forecast_data)
                    print(f"Broadcasted VAR forecast for station {rc_id}")
                else:
                    print(f"No forecast generated for station {rc_id} (check model/data)")
                    
        except Exception as e:
            print(f"Error in broadcast_forecast_data: {e}")

def train_all_models(app):
    with app.app_context():
        stations = RaspClient.query.all()
        for station in stations:
            train_and_save_model(station.rcID)

def start_scheduler(app):
    scheduler = BackgroundScheduler()

    scheduler.add_job(func = broadcast_weather_data, args=[app], trigger = "interval", seconds = 300)
    scheduler.add_job(func = broadcast_forecast_data, args=[app], trigger = "interval", seconds = 310, next_run_time = datetime.now())
    scheduler.add_job(func = train_all_models, args = [app], trigger = "cron", hour = 3)
    scheduler.add_job(func = train_all_models, args = [app], trigger = "date", run_date = datetime.now())
    scheduler.start()