from ..models import RaspClient, RaspData
from sqlalchemy import desc
from datetime import datetime, timedelta, timezone
from .external_weather_service import get_external_weather_values, get_station_coordinates

def calc_heat_index(temperature, humidity):
    """
    Calcula o índice de calor com base na temperatura (°C) e umidade (%).
    """

    if temperature is None or humidity is None:
        raise ValueError("Temperature and humidity must not be None")
    
    if not all(isinstance(v, (int, float)) for v in (temperature, humidity)):
        raise TypeError("Temperature and humidity must be numeric")

    # Fórmula simplificada do índice de calor
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

    return hi


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
    
    #pega a leitura que é de 3 horas OU MAIS antes da leitura mais recente
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


def calc_cloudiness(lux, pressure, humidity):
    if lux is None or pressure is None or humidity is None:
        raise ValueError("Lux, pressure and humidity must not be None")

    if not all(isinstance(v, (int, float)) for v in (lux, pressure, humidity)):
        raise TypeError("Lux, pressure, and humidity must be numeric")

    if lux < 8000:
        lux = 0.5
    elif lux >= 8000 and lux <= 20000:
        lux = 0.25
    else:
        lux = 0

    if pressure < 1010:
        pressure = 0.3
    elif pressure >= 1010 and pressure <= 1015:
        pressure = 0.15
    else:
        pressure = 0

    if humidity > 70:
        humidity = 0.2
    elif humidity >= 55 and humidity <= 70:
        humidity = 0.1
    else:
        humidity = 0

    return round((lux + pressure + humidity), 2) 


def get_station_data_by_id(rc_id):
    """
    Busca e formata os dados mais recentes para um ID de estação específico.
    """
    # Estamos usando vento/chuva da api externa até a instalação do pluviômetro/anemômetro
  
    # Coordenadas 
    latitude, longitude = get_station_coordinates(rc_id)

    # Dados API externa
    try:
        _, _, _, api_wind, api_rain = get_external_weather_values(latitude, longitude)
    except ConnectionError:
        api_wind = None
        api_rain = None

    # Filtragem por id da estação e último registro
    data_details = RaspData.query.filter_by(rcID=rc_id).order_by(desc(RaspData.timestamp)).first()

    station_status = RaspClient.query.filter_by(rcID=rc_id).first()

    if not data_details:
        return None

    past_pressure = get_pressure_3_hours_ago(data_details.rcID)
    trend = calc_pressure_trend(data_details.pressure, past_pressure)

    last_update_minutes = int(
        (datetime.now(timezone.utc) - data_details.timestamp).total_seconds() / 60
    )

    response_details = {
        "rdID": data_details.rdID,
        "rcID": data_details.rcID,
        "timestamp": data_details.timestamp.isoformat(),
        "last_update": max(last_update_minutes, 0),
        "status": station_status.status,
        "temperature": data_details.temp,
        "humidity": data_details.humidity,
        "humidity_status": classify_humidity(data_details.humidity),
        "heat_index": calc_heat_index(data_details.temp, data_details.humidity),
        "pressure": data_details.pressure,
        "wind_speed": api_wind,
        "wind_speed_status": classify_wind_status(api_wind) if api_wind is not None else None,
        "rain_chance": api_rain,
        "rain_chance_status": classify_rain_probability(api_rain) if api_rain is not None else None,
        "pressure_trend": trend,
        "pressure_trend_status": classify_pressure_trend(trend),
        "cloudiness": calc_cloudiness(
            data_details.lux,
            data_details.pressure,
            data_details.humidity
        ),
    }

    return response_details


