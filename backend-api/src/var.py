import os
import pickle
import pandas as pd
from datetime import datetime
from statsmodels.tsa.api import VAR
from .services.forecast_services import calc_heat_index, calc_cloudiness
from .var_data import prepare_var_data
from .models import Forecast
from .database import db


def _clamp_non_negative(value):
    if value is None or pd.isna(value):
        return None
    return max(float(value), 0.0)
# define o diretório para salvar os modelos .pkl
MODEL_DIR = os.path.join(os.path.dirname(__file__), 'model_store')

if not os.path.exists(MODEL_DIR):
    os.makedirs(MODEL_DIR)

FORECAST_CACHE_DIR = os.path.join(os.path.dirname(__file__), 'forecast_cache')

if not os.path.exists(FORECAST_CACHE_DIR):
    os.makedirs(FORECAST_CACHE_DIR)

# separa o arquivo por id da estação
def get_model_path(rc_id):
    return os.path.join(MODEL_DIR, f'station_{rc_id}_var_model.pkl')

# Define o caminho para o cache da previsão (último sucesso)
def get_forecast_cache_path(rc_id):
    return os.path.join(FORECAST_CACHE_DIR, f'station_{rc_id}_forecast_cache.pkl')

# função para treinar e salvar o modelo VAR
def train_and_save_model(rc_id, days=180, maxlags=48):

    df = prepare_var_data(rc_id, days)
    
    # Validate data length (VAR needs more rows than lags)
    if df is None or len(df) < maxlags + 10:
        print(f"[VAR] Insufficient data to train model for Station {rc_id}")
        return None

    try:
        # treinamento do modelo VAR
        model = VAR(df)
        results = model.fit(maxlags=maxlags, ic='aic')
        
        # salva em arquivo .pkl
        file_path = get_model_path(rc_id)
        with open(file_path, 'wb') as f:
            pickle.dump(results, f)
            
        print(f"[VAR] Model for Station {rc_id} trained and saved to {file_path}")
        print(f"[VAR] Selected Lag Order: {results.k_ar}")
        return results

    except Exception as e:
        print(f"[VAR] Error training model: {e}")
        return None

# checa se ja tem um modelo salvo para a estação
def load_model(rc_id):

    file_path = get_model_path(rc_id)
    if os.path.exists(file_path):
        try:
            with open(file_path, 'rb') as f:
                return pickle.load(f)
        except Exception as e:
            print(f"[VAR] Error loading model file: {e}")
            return None
    return None

def _generate_forecast_data(rc_id):
    """
    Internal function: Contains the core logic to generate the 7-day forecast.
    """
    # carrega modelo treinado em arquivo .pkl
    results = load_model(rc_id)
    
    if results is None:
        print(f"[VAR] No pre-trained model found for Station {rc_id}. Attempting to train now...")
        results = train_and_save_model(rc_id)

        if results is None:
            print(f"[VAR] Auto-training failed for Station {rc_id} (likely insufficient data).")
            return None

    # pega os dados dos ultimos 4 dias para iniciar a previsão
    df_recent = prepare_var_data(rc_id, days=4)
    
    if df_recent is None:
        print(f"[VAR] No recent data available for Station {rc_id}.")
        return None

    # Compatibilidade de esquema: se o modelo salvo foi treinado com colunas antigas,
    # retreina para alinhar com o dataframe atual.
    model_columns = list(df_recent.columns)
    model_names = list(getattr(results, "names", []))
    if model_names and model_names != model_columns:
        print(
            f"[VAR] Model schema mismatch for Station {rc_id}. "
            f"Model={model_names} Data={model_columns}. Retraining..."
        )
        results = train_and_save_model(rc_id)
        if results is None:
            print(f"[VAR] Retraining failed for Station {rc_id} after schema mismatch.")
            return None

    # checa se tem dados suficientes para a quantidade de lags que o modelo selecionou
    lag_order = results.k_ar
    if len(df_recent) < lag_order:
        print(f"[VAR] Insufficient recent data. Needed {lag_order}, got {len(df_recent)}.")
        return None
        
    try:
        # reserva a quantidade de registros correta para a previsão
        steps = 4 * 24 * 2 # dias/horas/registro por hora
        input_data = df_recent.values[-lag_order:]
        
        forecast_array = results.forecast(y=input_data, steps=steps)
        
        # cria dataframe da previsão
        last_timestamp = df_recent.index[-1]
        freq = pd.to_timedelta('30min')
        future_dates = [last_timestamp + freq * (i+1) for i in range(steps)]
        
        df_forecast = pd.DataFrame(forecast_array, index=future_dates, columns=df_recent.columns)
        
        # 1. Recupera os dados REAIS de hoje (do início do dia até o último registro)
        start_of_today = last_timestamp.normalize()
        df_today_actuals = df_recent[df_recent.index >= start_of_today]

        # 2. Combina o histórico real de hoje com a previsão futura
        # Isso garante que o dia atual tenha dados completos (passado + futuro)
        df_combined = pd.concat([df_today_actuals, df_forecast])

        # cria dict pra 'daily summary'
        aggregation = {
            'temp': ['min', 'max', 'mean'],
            'humidity': 'mean',
            'wind_speed': 'mean',
            'lux': 'mean',
            'pressure': 'mean',
            'pluv': 'mean',
        }
        
        # Usamos df_combined ao invés de df_forecast para incluir o dia atual completo
        daily_agg = df_combined.resample('D').agg(aggregation)
        
        daily_summary = []
        for date, row in daily_agg.iterrows():
            # extrai médias temporárias para cálculo
            avg_temp = row[('temp', 'mean')]
            avg_hum = row[('humidity', 'mean')]
            avg_lux = row[('lux', 'mean')]
            avg_pressure = row[('pressure', 'mean')]

            # Verifica se os valores são válidos (previne erros se houver gaps)
            if pd.isna(avg_temp) or pd.isna(avg_hum):
                continue

            # calculos adicionais (sensação térmica e nebulosidade)
            heat_index = calc_heat_index(avg_temp, avg_hum)
            cloudiness = calc_cloudiness(avg_lux, avg_pressure, avg_hum)

            daily_summary.append({
                "date": date.strftime('%Y-%m-%d'),
                "min_temp": round(row[('temp', 'min')], 1),
                "max_temp": round(row[('temp', 'max')], 1),
                "heat_index": round(heat_index, 1),
                "cloudiness": round(cloudiness, 1),
                "avg_wind_speed": round(row[('wind_speed', 'mean')], 1),
                "rain_mm": (
                    round(_clamp_non_negative(row[('pluv', 'mean')]), 2)
                    if pd.notna(row[('pluv', 'mean')])
                    else None
                ),
            })
            
        # cria dict pra 'hourly forecast'
        # Usamos df_combined aqui também
        hourly_agg = df_combined.resample('H').mean()
        
        hourly_grouped = {}

        for timestamp, row in hourly_agg.iterrows():
            date_key = timestamp.strftime('%Y-%m-%d')
            
            if date_key not in hourly_grouped:
                hourly_grouped[date_key] = []

            hourly_grouped[date_key].append({
                "timestamp": timestamp.isoformat(),
                "temp": round(row['temp'], 2),
                "humidity": round(row['humidity'], 2),
                "pressure": round(row['pressure'], 2),
                "wind_speed": round(row['wind_speed'], 2),
                "lux": round(row['lux'], 2) if 'lux' in row else 0,
                "rain_mm": (
                    round(_clamp_non_negative(row['pluv']), 2)
                    if 'pluv' in row and pd.notna(row['pluv'])
                    else None
                ),
            })

        # Converte o dicionário agrupado para uma lista estruturada
        hourly_forecast = [
            {"date": date, "hours": data} 
            for date, data in hourly_grouped.items()
        ]

        return {
            "daily_summary": daily_summary,
            "hourly_forecast": hourly_forecast
        }
        
    except Exception as e:
        print(f"[VAR] Error generating forecast: {e}")
        return None
    
def save_forecast_to_db(rc_id, forecast_data):
    """
    Saves or updates the forecast data into the database 'Forecast' table.
    """
    try:
        # Create a lookup map for daily summaries for faster access by date
        daily_map = {d['date']: d for d in forecast_data['daily_summary']}

        # Loop through the grouped hourly data
        for day_group in forecast_data['hourly_forecast']:
            date_key = day_group['date']
            daily_info = daily_map.get(date_key)

            for hour_data in day_group['hours']:
                ts = datetime.fromisoformat(hour_data['timestamp'])

                # checa se ja tem um registro pra essa timestamp dessa estação, se tiver atualiza, se não tiver cria um novo
                record = Forecast.query.filter_by(rcID=rc_id, timestamp=ts).first()

                if not record:
                    record = Forecast(rcID=rc_id, timestamp=ts)
                
                # Helper function to replace NaN with None (NULL in database)
                def get_valid(val, default=None):
                    if val is not None and pd.notna(val):
                        return float(val) if isinstance(val, (int, float)) else val
                    return default
                
                record.c_temp = get_valid(hour_data.get('temp'))
                record.c_humidity = get_valid(hour_data.get('humidity'))
                record.c_pressure = get_valid(hour_data.get('pressure'))
                record.c_wind_speed = get_valid(hour_data.get('wind_speed'))
                record.c_lux = get_valid(hour_data.get('lux'))
                forecast_rain = get_valid(hour_data.get('rain_mm'))
                record.c_pluv = max(forecast_rain, 0.0) if forecast_rain is not None else None
                
                if daily_info:
                    record.temp_min = int(daily_info.get('min_temp', 0))
                    record.temp_max = int(daily_info.get('max_temp', 0))
                    record.feels_like = int(daily_info.get('heat_index', 0))
                    
                db.session.add(record)

        db.session.commit()
        print(f"[VAR] Database updated with forecast for Station {rc_id}")

    except Exception as e:
        db.session.rollback()
        print(f"[VAR] Error saving forecast to DB: {e}")

def predict_weekly_weather(rc_id):
    """
    Wrapper function:
    1. Tries to generate a fresh forecast.
    2. If successful -> Caches the result, Saves to DB, and returns it.
    3. If failed -> Loads the last cached result (if available) and returns it.
    """
    
    # tenta gerar previsão
    forecast_data = None
    try:
        forecast_data = _generate_forecast_data(rc_id)
    except Exception as e:
        print(f"[VAR] Unexpected error in forecast generation logic: {e}")
        forecast_data = None

    cache_path = get_forecast_cache_path(rc_id)

    # se a geração foi bem-sucedida, salva no cache e no banco de dados, e retorna a previsão
    if forecast_data is not None:
        try:
            with open(cache_path, 'wb') as f:
                pickle.dump(forecast_data, f)
            print(f"[VAR] Forecast for Station {rc_id} generated and cached.")
        except Exception as e:
            print(f"[VAR] Warning: Could not save forecast cache: {e}")
        
        save_forecast_to_db(rc_id, forecast_data)
        
        return forecast_data

    else:
        if os.path.exists(cache_path):
            print(f"[VAR] Generation failed. Falling back to cached forecast for Station {rc_id}.")
            try:
                with open(cache_path, 'rb') as f:
                    cached_data = pickle.load(f)
                return cached_data
            except Exception as e:
                print(f"[VAR] Error loading cached forecast: {e}")
        else:
            print(f"[VAR] Generation failed and no cache available for Station {rc_id}.")
        
        return None

def get_cached_forecast(rc_id):
    """
    Pega o cache da previsão para uma estação específica, se existir.
    """
    cache_path = get_forecast_cache_path(rc_id)
    
    if os.path.exists(cache_path):
        try:
            with open(cache_path, 'rb') as f:
                return pickle.load(f)
        except Exception as e:
            print(f"[VAR] Error reading cache for Station {rc_id}: {e}")
            return None
    return None