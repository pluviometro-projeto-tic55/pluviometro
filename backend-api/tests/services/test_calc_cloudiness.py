import pytest
from src.services.forecast_services import calc_cloudiness

# ============================
# Testes principais
# ============================

def test_cloudiness_low_lux():
    """
    Calcula nebulosidade para baixa luminosidade (< 3000).
    """
    lux = 1000        # < 3000 → 0.5
    pressure = 1020   
    humidity = 40     

    result = calc_cloudiness(lux, pressure, humidity)

    assert result == 0.5


def test_cloudiness_low_pressure():
    """
    Calcula nebulosidade para pressão baixa (< 1010 hPa).
    """
    lux = 8000       
    pressure = 1005  # < 1010 → 0.3
    humidity = 40   

    result = calc_cloudiness(lux, pressure, humidity)

    assert result == 0.3


def test_cloudiness_high_humidity():
    """
    Calcula nebulosidade para umidade alta (> 70%).
    """
    lux = 8000        
    pressure = 1020 
    humidity = 80    # > 70 → 0.2

    result = calc_cloudiness(lux, pressure, humidity)

    assert result == 0.2


def test_cloudiness_combined_factors():
    """
    Combina corretamente todos os fatores e arredonda o resultado.
    """
    lux = 1000        # 0.5
    pressure = 1005  # 0.3
    humidity = 80    # 0.2

    result = calc_cloudiness(lux, pressure, humidity)

    assert result == 1.0


# ============================
# Validação de intervalo
# ============================

def test_cloudiness_is_between_0_and_1():
    """
    Garante que o índice de nebulosidade esteja entre 0 e 1.
    """
    result = calc_cloudiness(
        lux=500,
        pressure=1000,
        humidity=90
    )

    assert 0 <= result <= 1


# ============================
# Testes de fronteira
# ============================

@pytest.mark.parametrize(
    "lux,expected",
    [
        (2999, 0.5),
        (3000, 0.25),
        (7000, 0.25),
        (7001, 0),
    ],
)
def test_lux_thresholds(lux, expected):
    """
    Testa valores de fronteira para luminosidade.
    """
    result = calc_cloudiness(lux, 1020, 40)

    assert result == expected


@pytest.mark.parametrize(
    "pressure,expected",
    [
        (1009, 0.3),
        (1010, 0.15),
        (1015, 0.15),
        (1016, 0),
    ],
)
def test_pressure_thresholds(pressure, expected):
    """
    Testa valores de fronteira para pressão.
    """
    result = calc_cloudiness(8000, pressure, 40)

    assert result == expected


@pytest.mark.parametrize(
    "humidity,expected",
    [
        (54, 0),
        (55, 0.1),
        (70, 0.1),
        (71, 0.2),
    ],
)
def test_humidity_thresholds(humidity, expected):
    """
    Testa valores de fronteira para umidade.
    """
    result = calc_cloudiness(8000, 1020, humidity)

    assert result == expected


# ============================
# Arredondamento
# ============================

def test_cloudiness_rounding():
    """
    Garante arredondamento correto para duas casas decimais.
    """
    lux = 3000        # 0.25
    pressure = 1010  # 0.15
    humidity = 55    # 0.1

    result = calc_cloudiness(lux, pressure, humidity)

    assert result == 0.5

# ============================
# Validação de erros / entradas inválidas
# ============================

def test_cloudiness_raises_error_when_lux_is_none():
    with pytest.raises(ValueError):
        calc_cloudiness(None, 1010, 60)


def test_cloudiness_raises_error_when_pressure_is_none():
    with pytest.raises(ValueError):
        calc_cloudiness(3000, None, 60)


def test_cloudiness_raises_error_when_humidity_is_none():
    with pytest.raises(ValueError):
        calc_cloudiness(3000, 1010, None)
