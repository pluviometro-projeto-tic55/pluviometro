import pytest
from src.services.external_weather_service import get_external_weather_values

# ============================
# Helpers de mock
# ============================

class MockResponse:
    def __init__(self, status_code, json_data=None):
        self.status_code = status_code
        self._json_data = json_data or {}

    def json(self):
        return self._json_data
    

# ============================
# Testes principais
# ============================

def test_get_external_weather_values_success(monkeypatch):
    mock_payload = {
        "current": {
            "pressure_mb": 1013,
            "temp_c": 25,
            "humidity": 60,
            "wind_kph": 12,
        },
        "forecast": {
            "forecastday": [
                {"date": "2026-05-25", "day": {"daily_chance_of_rain": 30, "maxtemp_c": 28, "mintemp_c": 20, "avgtemp_c": 24, "condition": {"text": "Nublado", "icon": "..."}}},
                {"date": "2026-05-26", "day": {"daily_chance_of_rain": 40, "maxtemp_c": 29, "mintemp_c": 21, "avgtemp_c": 25, "condition": {"text": "Chuva", "icon": "..."}}},
            ]
        }
    }

    def mock_get(*args, **kwargs):
        return MockResponse(200, mock_payload)

    monkeypatch.setattr("src.services.requests.get", mock_get)

    result = get_external_weather_values("fake-api-key")

    assert result[0:5] == (1013, 25, 60, 12, 30)
    assert len(result[5]) >= 1  # Verifica que forecast_4days está presente


def test_get_external_weather_values_missing_fields(monkeypatch):
    """
    Retorna None para campos ausentes no payload,
    sem quebrar a função.
    """
    mock_payload = {
        "current": {
            "temp_c": 22
        },
        "forecast": {
            "forecastday": []
        }
    }

    def mock_get(*args, **kwargs):
        return MockResponse(200, mock_payload)

    monkeypatch.setattr("src.services.requests.get", mock_get)

    result = get_external_weather_values("fake-api-key")

    assert result[0:5] == (None, 22, None, None, None)
    assert result[5] == []  # forecast_4days vazio


def test_get_external_weather_values_empty_forecast(monkeypatch):
    """
    Trata corretamente forecast vazio.
    """
    mock_payload = {
        "current": {
            "pressure_mb": 1010,
            "temp_c": 20,
            "humidity": 50,
            "wind_kph": 10,
        },
        "forecast": {
            "forecastday": []
        }
    }

    def mock_get(*args, **kwargs):
        return MockResponse(200, mock_payload)

    monkeypatch.setattr("src.services.requests.get", mock_get)

    result = get_external_weather_values("fake-api-key")

    assert result[0:5] == (1010, 20, 50, 10, None)
    assert result[5] == []


def test_get_external_weather_values_http_error(monkeypatch):
    """
    Lança ConnectionError quando a API retorna erro HTTP.
    """
    def mock_get(*args, **kwargs):
        return MockResponse(500)

    monkeypatch.setattr("src.services.requests.get", mock_get)

    with pytest.raises(ConnectionError):
        get_external_weather_values("fake-api-key")

