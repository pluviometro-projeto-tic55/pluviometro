from ..models import RaspClient, RaspData
from sqlalchemy import desc
from datetime import datetime, timedelta, timezone
from .external_weather_service import get_external_weather_values
import logging
import math

# Configuração de logging estruturado para o módulo meteorológico
logger = logging.getLogger(__name__)
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s in %(module)s: %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


def _safe_mean(values):
    numeric_values = [value for value in values if isinstance(value, (int, float))]
    if not numeric_values:
        return None
    return sum(numeric_values) / len(numeric_values)


def _last_non_null_value(rc_id, column):
    """
    Retorna o valor mais recente não nulo de uma coluna da RaspData.
    """
    try:
        reading = (
            RaspData.query
            .filter(
                RaspData.rcID == rc_id,
                column.isnot(None),
            )
            .order_by(desc(RaspData.timestamp))
            .first()
        )
        return getattr(reading, column.key) if reading else None
    except Exception as e:
        logger.error(f"Erro ao buscar último valor não nulo para rcID {rc_id}: {e}")
        return None


def _safe_heat_index(temperature, humidity):
    if temperature is None or humidity is None:
        return None
    try:
        return calc_heat_index(temperature, humidity)
    except (TypeError, ValueError) as e:
        logger.warning(f"Falha ao calcular índice de calor: {e}")
        return None


def _safe_cloudiness(lux, pressure, humidity):
    if lux is None or pressure is None or humidity is None:
        return None
    try:
        return calc_cloudiness(lux, pressure, humidity)
    except (TypeError, ValueError) as e:
        logger.warning(f"Falha ao calcular nebulosidade: {e}")
        return None


def _safe_dew_point(temperature, humidity):
    if temperature is None or humidity is None:
        return None
    try:
        return calc_dew_point(temperature, humidity)
    except (TypeError, ValueError) as e:
        logger.warning(f"Falha ao calcular ponto de orvalho: {e}")
        return None


def _safe_air_density(temperature, pressure, humidity):
    if temperature is None or pressure is None or humidity is None:
        return None
    try:
        return calc_air_density(temperature, pressure, humidity)
    except (TypeError, ValueError) as e:
        logger.warning(f"Falha ao calcular densidade do ar: {e}")
        return None


def calc_heat_index(temperature, humidity):
    """
    Calcula o índice de calor com base na temperatura (°C) e umidade (%).
    """
    if temperature is None or humidity is None:
        raise ValueError("Temperature and humidity must not be None")
    
    if not all(isinstance(v, (int, float)) for v in (temperature, humidity)):
        raise TypeError("Temperature and humidity must be numeric")

    temperature_f = (temperature * 9/5) + 32  # Converter para Fahrenheit

    hi = 0.5 * (temperature_f + 61.0 + ((temperature_f - 68.0) * 1.2) + (humidity * 0.094))
    
    if hi >= 80:
        hi = (
            -42.379 
            + 2.04901523 * temperature_f
            + 10.14333127 * humidity 
            - 0.22475541 * temperature_f * humidity 
            - 6.83783 * (10 ** -3) * (temperature_f ** 2) 
            - 5.481717 * (10 ** -2) * (humidity ** 2) 
            + 1.22874 * (10 ** -3) * (temperature_f ** 2) * humidity 
            + 8.5282 * (10 ** -4) * temperature_f * (humidity ** 2) 
            - 1.99 * (10 ** -6) * (temperature_f ** 2) * (humidity ** 2)
        )

    hi = (hi - 32) * 5/9  # Converter de volta para Celsius
    return round(hi, 2)


def calc_dew_point(temperature, humidity):
    """
    Calcula o ponto de orvalho (°C) usando a fórmula de Magnus-Tetens.
    """
    if temperature is None or humidity is None:
        raise ValueError("Temperature and humidity must not be None")
    if not all(isinstance(v, (int, float)) for v in (temperature, humidity)):
        raise TypeError("Temperature and humidity must be numeric")
    if humidity <= 0:
        humidity = 0.1  # Evita log(0)

    a = 17.27
    b = 237.7
    alpha = ((a * temperature) / (b + temperature)) + math.log(humidity / 100.0)
    dew_point = (b * alpha) / (a - alpha)
    return round(dew_point, 2)


def calc_air_density(temperature, pressure, humidity):
    """
    Calcula a densidade do ar (kg/m³) considerando temperatura (°C), pressão (hPa) e umidade (%).
    """
    if temperature is None or pressure is None or humidity is None:
        raise ValueError("Temperature, pressure, and humidity must not be None")
    
    p_pa = pressure * 100.0
    t_k = temperature + 273.15
    
    es = 6.112 * math.exp((17.67 * temperature) / (temperature + 243.5))
    v_pressure = (humidity / 100.0) * es * 100.0
    d_pressure = p_pa - v_pressure

    r_dry = 287.058
    r_vapor = 461.495

    density = (d_pressure / (r_dry * t_k)) + (v_pressure / (r_vapor * t_k))
    return round(density, 3)


def calc_pressure_trend(current_pressure, past_pressure):
    """
    Calcula a tendência de pressão atmosférica (hPa).
    """
    if current_pressure is None or past_pressure is None:
        return 0.0

    if not all(isinstance(v, (int, float)) for v in (current_pressure, past_pressure)):
        raise TypeError("Pressure values must be numeric")

    return round(current_pressure - past_pressure, 2)


def classify_pressure_trend(trend):
    if trend > 1:
        return "Subindo"
    elif trend < -1:
        return "Caindo"
    return "Estável"


def classify_humidity(humidity):
    if humidity is None:
        return None

    if not isinstance(humidity, (int, float)):
        raise TypeError("Humidity must be numeric")

    if humidity < 30:
        return "Muito Seco"
    elif humidity < 40:
        return "Seco"
    elif humidity <= 60:
        return "Confortável"
    elif humidity <= 80:
        return "Úmido"
    else:
        return "Muito Úmido"


def classify_dew_point(dew_point):
    """
    Classifica a sensação de conforto com base no ponto de orvalho (°C).
    """
    if dew_point is None:
        return None
    if not isinstance(dew_point, (int, float)):
        raise TypeError("Dew point must be numeric")

    if dew_point < 10:
        return "Seco e agradável"
    elif 10 <= dew_point < 16:
        return "Confortável"
    elif 16 <= dew_point < 18:
        return "Um pouco úmido"
    elif 18 <= dew_point < 21:
        return "Úmido e abafado"
    elif 21 <= dew_point < 24:
        return "Muito úmido, desconfortável"
    else:
        return "Extremamente abafado, opressivo"


def classify_wind_status(speed_kmh):
    """
    Classifica o vento segundo níveis específicos da Escala de Beaufort.
    """
    if speed_kmh is None:
        return None

    if not isinstance(speed_kmh, (int, float)):
        raise TypeError("Wind speed must be numeric")

    if speed_kmh < 1:
        return "Calmo"
    elif 6 <= speed_kmh <= 11:
        return "Brisa leve"
    elif 20 <= speed_kmh <= 28:
        return "Vento moderado"
    elif 39 <= speed_kmh <= 49:
        return "Vento fresco"
    elif 62 <= speed_kmh <= 74:
        return "Ventania"
    elif 89 <= speed_kmh <= 102:
        return "Vendaval"
    elif speed_kmh > 118:
        return "Furacão"

    return "Transição"


def classify_rain_probability(probability):
    """
    Classifica a probabilidade de chuva (%).
    """
    if probability is None:
        return None

    if not isinstance(probability, (int, float)):
        raise TypeError("Rain probability must be numeric")

    if probability <= 10:
        return "Sem chuva"
    elif probability <= 30:
        return "Baixa chance"
    elif probability <= 50:
        return "Chance moderada"
    elif probability <= 70:
        return "Alta chance"
    elif probability <= 90:
        return "Muito alta chance"
    else:
        return "Chuva praticamente certa"


def get_pressure_3_hours_ago(rc_id):
    """
    Retorna a pressão da leitura mais recente
    que tenha ocorrido pelo menos 3 horas antes
    da última leitura registrada para a estação.
    """
    try:
        latest_reading = (
            RaspData.query
            .filter(RaspData.rcID == rc_id)
            .order_by(desc(RaspData.timestamp))
            .first()
        )
        
        if not latest_reading:
            return None

        latest_ts = latest_reading.timestamp
        
        if latest_ts.tzinfo is None:
            latest_ts = latest_ts.replace(tzinfo=timezone.utc)

        three_hours_before_latest = latest_ts - timedelta(hours=3)
        
        reading = (
            RaspData.query
            .filter(
                RaspData.rcID == rc_id,
                RaspData.timestamp <= three_hours_before_latest
            )
            .order_by(desc(RaspData.timestamp))
            .first()
        )
        
        return reading.pressure if reading else None
    except Exception as e:
        logger.error(f"Erro ao buscar pressão de 3 horas atrás para rcID {rc_id}: {e}")
        return None


def calc_cloudiness(lux, pressure, humidity):
    if lux is None or pressure is None or humidity is None:
        raise ValueError("Lux, pressure and humidity must not be None")

    if not all(isinstance(v, (int, float)) for v in (lux, pressure, humidity)):
        raise TypeError("Lux, pressure, and humidity must be numeric")

    if lux < 8000:
        lux_score = 0.5
    elif 8000 <= lux <= 20000:
        lux_score = 0.25
    else:
        lux_score = 0

    if pressure < 1010:
        press_score = 0.3
    elif 1010 <= pressure <= 1015:
        press_score = 0.15
    else:
        press_score = 0

    if humidity > 70:
        hum_score = 0.2
    elif 55 <= humidity <= 70:
        hum_score = 0.1
    else:
        hum_score = 0

    return round((lux_score + press_score + hum_score), 2) 


def get_station_data_by_id(rc_id, raw_local=False):
    """
    Busca e formata os dados mais recentes para um ID de estação específico,
    incluindo análises meteorológicas avançadas, ponto de orvalho e densidade do ar.
    """
    station_status = RaspClient.query.filter_by(rcID=rc_id).first()

    if not station_status:
        logger.warning(f"Estação com rcID {rc_id} não encontrada.")
        return None

    data_details = RaspData.query.filter_by(rcID=rc_id).order_by(desc(RaspData.timestamp)).first()

    latest_timestamp = data_details.timestamp if data_details else datetime.utcnow()
    window_start = latest_timestamp - timedelta(hours=1)

    recent_readings = (
        RaspData.query
        .filter(
            RaspData.rcID == rc_id,
            RaspData.timestamp >= window_start,
            RaspData.timestamp <= latest_timestamp,
        )
        .order_by(desc(RaspData.timestamp))
        .all()
    )

    avg_temp_1h = _safe_mean([reading.temp for reading in recent_readings])
    avg_humidity_1h = _safe_mean([reading.humidity for reading in recent_readings])
    avg_pressure_1h = _safe_mean([reading.pressure for reading in recent_readings])
    avg_lux_1h = _safe_mean([reading.lux for reading in recent_readings])
    avg_rain_mm_1h = _safe_mean([reading.pluv for reading in recent_readings])

    last_temp = _last_non_null_value(rc_id, RaspData.temp)
    last_humidity = _last_non_null_value(rc_id, RaspData.humidity)
    last_pressure = _last_non_null_value(rc_id, RaspData.pressure)
    last_lux = _last_non_null_value(rc_id, RaspData.lux)
    last_rain_mm = _last_non_null_value(rc_id, RaspData.pluv)
    last_wind_speed = _last_non_null_value(rc_id, RaspData.wind_speed)

    api_temp = None
    api_humidity = None
    api_pressure = None
    api_wind = None
    api_rain = None
    api_luminosity = None

    if station_status.latitude is not None and station_status.longitude is not None:
        try:
            (
                api_pressure,
                api_temp,
                api_humidity,
                api_wind,
                api_rain,
                _,
                _,
                api_luminosity,
                *_,
            ) = get_external_weather_values(station_status.latitude, station_status.longitude)
        except (ConnectionError, ValueError) as e:
            logger.error(f"Erro ao buscar dados externos para rcID {rc_id}: {e}")
            api_wind = None
            api_rain = None

    if not data_details:
        timestamp = datetime.now(timezone.utc)
        temperature = avg_temp_1h if avg_temp_1h is not None else (last_temp if last_temp is not None else api_temp)
        humidity = avg_humidity_1h if avg_humidity_1h is not None else (last_humidity if last_humidity is not None else api_humidity)
        
        pressure = avg_pressure_1h if avg_pressure_1h is not None else (last_pressure if last_pressure is not None else api_pressure)
        luminosity = avg_lux_1h if avg_lux_1h is not None else (last_lux if last_lux is not None else api_luminosity)
        rain_mm = avg_rain_mm_1h if avg_rain_mm_1h is not None else last_rain_mm
        wind_speed = last_wind_speed if last_wind_speed is not None else api_wind
        
        source_mode = "rolling_average_1h"
        if avg_temp_1h is None and avg_humidity_1h is None and avg_pressure_1h is None:
            source_mode = "external_fallback"
        if temperature is None and humidity is None and pressure is None and luminosity is None:
            source_mode = "no_data"

        dew_point = _safe_dew_point(temperature, humidity)
        air_density = _safe_air_density(temperature, pressure, humidity)

        return {
            "rdID": None,
            "rcID": rc_id,
            "timestamp": timestamp.isoformat(),
            "last_update": None,
            "status": station_status.status,
            "temperature": temperature,
            "humidity": humidity,
            "external_humidity": api_humidity,
            "humidity_status": classify_humidity(humidity) if humidity is not None else None,
            "heat_index": _safe_heat_index(temperature, humidity),
            "dew_point": dew_point,
            "dew_point_status": classify_dew_point(dew_point),
            "air_density": air_density,
            "pressure": pressure,
            "wind_speed": wind_speed,
            "wind_speed_status": classify_wind_status(wind_speed) if wind_speed is not None else None,
            "rain_mm": rain_mm,
            "rain_chance": api_rain,
            "rain_chance_status": classify_rain_probability(api_rain) if api_rain is not None else None,
            "pressure_trend": 0.0,
            "pressure_trend_status": classify_pressure_trend(0.0),
            "luminosity": luminosity,
            "cloudiness": _safe_cloudiness(luminosity, pressure, humidity),
            "is_estimated": True,
            "estimate_source": source_mode,
        }

    past_pressure = get_pressure_3_hours_ago(data_details.rcID)
    trend = calc_pressure_trend(data_details.pressure, past_pressure)

    timestamp = data_details.timestamp
    if timestamp.tzinfo is None:
        timestamp = timestamp.replace(tzinfo=timezone.utc)

    last_update_minutes = int((datetime.now(timezone.utc) - timestamp).total_seconds() / 60)

    temperature = data_details.temp if data_details.temp is not None else (
        avg_temp_1h if avg_temp_1h is not None else last_temp
    )
    humidity = data_details.humidity if data_details.humidity is not None else (
        avg_humidity_1h if avg_humidity_1h is not None else last_humidity
    )
    
    pressure = data_details.pressure if data_details.pressure is not None else (
        avg_pressure_1h if avg_pressure_1h is not None else last_pressure
    )
    luminosity = data_details.lux if data_details.lux is not None else (
        avg_lux_1h if avg_lux_1h is not None else last_lux
    )
    rain_mm = data_details.pluv if data_details.pluv is not None else (
        avg_rain_mm_1h if avg_rain_mm_1h is not None else last_rain_mm
    )
    wind_speed = (
        data_details.wind_speed
        if data_details.wind_speed is not None
        else (last_wind_speed if last_wind_speed is not None else api_wind)
    )

    used_local_average = any([
        data_details.temp is None and avg_temp_1h is not None,
        data_details.humidity is None and avg_humidity_1h is not None,
        data_details.pressure is None and avg_pressure_1h is not None,
        data_details.lux is None and avg_lux_1h is not None,
        data_details.pluv is None and avg_rain_mm_1h is not None,
    ])

    used_last_known = any([
        data_details.temp is None and avg_temp_1h is None and last_temp is not None,
        data_details.humidity is None and avg_humidity_1h is None and last_humidity is not None,
        data_details.pressure is None and avg_pressure_1h is None and last_pressure is not None,
        data_details.lux is None and avg_lux_1h is None and last_lux is not None,
        data_details.pluv is None and avg_rain_mm_1h is None and last_rain_mm is not None,
        data_details.wind_speed is None and last_wind_speed is not None,
    ])

    dew_point = _safe_dew_point(temperature, humidity)
    air_density = _safe_air_density(temperature, pressure, humidity)
    local_humidity = humidity

    response_details = {
        "rdID": data_details.rdID,
        "rcID": data_details.rcID,
        "timestamp": data_details.timestamp.isoformat(),
        "last_update": max(last_update_minutes, 0),
        "status": station_status.status,
        "temperature": temperature,
        "humidity": local_humidity,
        "external_humidity": api_humidity,
        "humidity_status": classify_humidity(local_humidity) if local_humidity is not None else None,
        "heat_index": _safe_heat_index(temperature, local_humidity),
        "dew_point": dew_point,
        "dew_point_status": classify_dew_point(dew_point),
        "air_density": air_density,
        "pressure": pressure,
        "wind_speed": wind_speed,
        "wind_speed_status": classify_wind_status(wind_speed) if wind_speed is not None else None,
        "rain_mm": rain_mm,
        "rain_chance": api_rain,
        "rain_chance_status": classify_rain_probability(api_rain) if api_rain is not None else None,
        "pressure_trend": trend,
        "pressure_trend_status": classify_pressure_trend(trend),
        "luminosity": luminosity,
        "cloudiness": _safe_cloudiness(luminosity, pressure, local_humidity),
        "is_estimated": used_local_average or used_last_known,
        "estimate_source": "rolling_average_1h" if used_local_average else ("last_known" if used_last_known else "live"),
    }

    return response_details