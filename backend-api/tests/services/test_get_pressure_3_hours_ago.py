from datetime import datetime, timezone, timedelta

from src.services.forecast_services import get_pressure_3_hours_ago
from src.models import RaspClient, RaspData

# ============================
# Helpers
# ============================

def create_station(session, rc_id=1):
    station = RaspClient(
        rcID=rc_id,
        serial=f"SERIAL-{rc_id}",
        name="Station Test",
    )
    session.add(station)
    session.commit()
    return station


def create_reading(session, rc_id, pressure, timestamp):
    reading = RaspData(
        rcID=rc_id,
        pressure=pressure,
        timestamp=timestamp,
    )
    session.add(reading)
    session.commit()
    return reading


def utc_now():
    return datetime.now(timezone.utc)

# ============================
# Testes principais
# ============================

def test_returns_pressure_from_reading_older_than_3_hours(session):
    """
    Retorna pressão da leitura válida com mais de 3 horas,
    usando a leitura mais recente como referência.
    """
    create_station(session)

    now = utc_now()

    create_reading(session, 1, 1015, now - timedelta(hours=5))
    create_reading(session, 1, 1018, now - timedelta(hours=4))
    create_reading(session, 1, 1020, now)  # leitura mais recente

    result = get_pressure_3_hours_ago(1)

    assert result == 1018


def test_returns_none_when_no_readings_older_than_3_hours(session):
    """
    Retorna None quando não há leituras com 3 horas ou mais
    antes da leitura mais recente.
    """
    create_station(session)

    now = utc_now()

    create_reading(session, 1, 1015, now - timedelta(hours=2))
    create_reading(session, 1, 1018, now)

    result = get_pressure_3_hours_ago(1)

    assert result is None


def test_returns_none_when_station_has_no_readings(session):
    """
    Retorna None quando a estação não possui registros.
    """
    create_station(session)

    result = get_pressure_3_hours_ago(1)

    assert result is None


def test_uses_latest_reading_as_reference(session):
    """
    Garante que a leitura mais recente é usada como base,
    e não a mais antiga.
    """
    create_station(session)

    now = utc_now()

    # leitura antiga
    create_reading(session, 1, 1005, now - timedelta(hours=10))
    # leitura intermediária
    create_reading(session, 1, 1010, now - timedelta(hours=6))
    # leitura mais recente
    create_reading(session, 1, 1020, now - timedelta(hours=1))
    result = get_pressure_3_hours_ago(1)

    # 3h antes da leitura mais recente (1h atrás) -> 4h atrás
    # leitura válida mais próxima é a de 6h atrás
    assert result == 1010


# ============================
# Casos de borda
# ============================

def test_exactly_3_hours_difference_is_valid(session):
    """
    Leitura exatamente 3 horas antes deve ser considerada válida.
    """
    create_station(session)

    now = utc_now()

    create_reading(session, 1, 1008, now - timedelta(hours=3))
    create_reading(session, 1, 1020, now)

    result = get_pressure_3_hours_ago(1)

    assert result == 1008


def test_multiple_stations_isolation(session):
    """
    Garante que leituras de outras estações não interferem.
    """
    create_station(session, rc_id=1)
    create_station(session, rc_id=2)

    now = utc_now()

    create_reading(session, 1, 1010, now - timedelta(hours=4))
    create_reading(session, 2, 990, now - timedelta(hours=5))
    create_reading(session, 1, 1020, now)

    result = get_pressure_3_hours_ago(1)

    assert result == 1010


def test_station_does_not_exist(session):
    """
    Retorna None quando rc_id não existe no banco.
    """
    result = get_pressure_3_hours_ago(999)

    assert result is None
