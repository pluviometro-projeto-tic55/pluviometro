from ..models import RaspClient
import os, requests

def get_station_coordinates(rc_id):
    station = RaspClient.query.filter_by(rcID=rc_id).first()

    if not station:
        raise ValueError("Station not found")

    if station.latitude is None or station.longitude is None:
        raise ValueError("The station does not have its latitude/longitude recorded.")

    return station.latitude, station.longitude


def get_external_weather_values(latitude, longitude):
    apiKey = os.getenv('API_KEY')
    if not apiKey:
        raise ConnectionError("API_KEY not configured in environment variables")
    
    url = f"https://api.weatherapi.com/v1/forecast.json?key={apiKey}&q={latitude},{longitude}&days=4&aqi=no"

    try:
        response = requests.get(url, timeout=5)
    except requests.RequestException as exc:
        raise ConnectionError("External weather API unavailable") from exc

    if response.status_code != 200:
        raise ConnectionError(f"Failed to fetch data: {response.status_code}")

    data = response.json()

    current_data = data.get('current', {})
    api_pressure = current_data.get('pressure_mb')
    api_temp = current_data.get('temp_c')
    api_humidity = current_data.get('humidity')
    api_wind = current_data.get('wind_kph')
    # WeatherAPI nao retorna lux diretamente; usamos UV como proxy externo de luminosidade.
    api_luminosity = current_data.get('uv')
    api_uv_index = current_data.get('uv')
    api_is_day = current_data.get('is_day')
    api_condition = current_data.get('condition', {}).get('text')
    api_last_updated_epoch = current_data.get('last_updated_epoch')

    forecast_days = data.get("forecast", {}).get("forecastday", [])
   
    api_rain = (
        forecast_days[0].get("day", {}).get("daily_chance_of_rain")
        if forecast_days else None
    )
    api_rain_mm = (
        forecast_days[0].get("day", {}).get("totalprecip_mm")
        if forecast_days else None
    )

    # Extrair previsão de 4 dias
    forecast_4days = []
    for day in forecast_days[:4]:
        forecast_4days.append({
            "date": day.get("date"),
            "max_temp": day.get("day", {}).get("maxtemp_c"),
            "min_temp": day.get("day", {}).get("mintemp_c"),
            "avg_temp": day.get("day", {}).get("avgtemp_c"),
            "rain_chance": day.get("day", {}).get("daily_chance_of_rain"),
            "rain_mm": day.get("day", {}).get("totalprecip_mm"),
            "condition": day.get("day", {}).get("condition", {}).get("text"),
            "icon": day.get("day", {}).get("condition", {}).get("icon")
        })

    first_forecast_day = forecast_days[0] if forecast_days else {}
    api_sunrise = first_forecast_day.get('astro', {}).get('sunrise')
    api_sunset = first_forecast_day.get('astro', {}).get('sunset')

    return (
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
    )

