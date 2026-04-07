import pytest
from src.services.forecast_services import calc_heat_index
import math

# ============================
# Casos básicos de funcionamento
# ============================

def test_heat_index_low_values_below_80f():
    """
    Calcula índice de calor para valores baixos (< 80°F)
    """
    temperature_c = 20  # ~68°F
    humidity = 40

    result = calc_heat_index(temperature_c, humidity)

    assert isinstance(result, (int, float))
    assert temperature_c - 5 <= result <= temperature_c + 2  # sensação térmica tende a ser próxima ou menor
    assert not math.isnan(result)


def test_heat_index_high_values_above_80f():
    """
    Calcula índice de calor para valores altos (>= 80°F),
    """
    temperature_c = 32  # ~89.6°F
    humidity = 70

    result = calc_heat_index(temperature_c, humidity)

    assert isinstance(result, (int, float))
    assert result > temperature_c  # índice de calor maior que a temperatura real
    assert not math.isnan(result)


# ============================
# Conversão Celsius - Fahrenheit
# ============================

def test_temperature_conversion_celsius_to_fahrenheit_and_back():
    """
    Garante que a conversão C → F → C ocorre corretamente
    e que o retorno final está em Celsius.
    """
    temperature_c = 25
    humidity = 50

    result = calc_heat_index(temperature_c, humidity)

    # Resultado deve estar em Celsius
    assert result < 100  # impossível em Celsius para esse cenário
    assert result > -50


def test_return_value_is_celsius():
    """
    Verifica explicitamente que o valor retornado está em Celsius
    e não em Fahrenheit.
    """
    temperature_c = 30
    humidity = 60

    result = calc_heat_index(temperature_c, humidity)

    # Se estivesse em Fahrenheit seria > 80
    assert result < 60


# ============================
# Casos de borda 
# ============================

def test_zero_humidity():
    """
    Testa comportamento com umidade zero.
    """
    temperature_c = 30
    humidity = 0

    result = calc_heat_index(temperature_c, humidity)

    assert isinstance(result, (int, float))
    assert not math.isnan(result)


def test_extreme_humidity():
    """
    Testa comportamento com umidade extremamente alta.
    """
    temperature_c = 30
    humidity = 100

    result = calc_heat_index(temperature_c, humidity)

    assert isinstance(result, (int, float))
    assert result >= temperature_c


def test_negative_temperature():
    """
    Testa temperaturas negativas (cenário frio extremo).
    """
    temperature_c = -5
    humidity = 50

    result = calc_heat_index(temperature_c, humidity)

    assert isinstance(result, (int, float))
    assert result < 0


# ============================
# Validação de erros / entradas inválidas
# ============================

def test_none_temperature_raises_error():
    """
    Garante que valores nulos para temperatura geram erro.
    """
    with pytest.raises(ValueError):
        calc_heat_index(None, 50)


def test_none_humidity_raises_error():
    """
    Garante que valores nulos para umidade geram erro.
    """
    with pytest.raises(ValueError):
        calc_heat_index(30, None)


def test_invalid_type_temperature():
    """
    Garante que tipos inválidos geram erro.
    """
    with pytest.raises(TypeError):
        calc_heat_index("30", 50)


def test_invalid_type_humidity():
    """
    Garante que tipos inválidos geram erro.
    """
    with pytest.raises(TypeError):
        calc_heat_index(30, "50")


