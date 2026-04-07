from ..models import RaspClient, RaspData
from ..database import db
from sqlalchemy import asc, text
import csv, io
from datetime import datetime, timedelta, date
from ..constants.weather_variables import VARIABLE_LABEL_MAP, VARIABLE_FILENAME_MAP
from ..utils.filename import safe_filename

def get_historical_hourly_average(rc_id, start_date, end_date, variable):
    """
    Retorna médias horárias por dia de uma variável climática.
    """

    # Converte datas
    try:
        start = datetime.strptime(start_date, "%Y-%m-%d").date()
        end = datetime.strptime(end_date, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError("Invalid date format (YYYY-MM-DD)")

    # Impede data futura
    if end > date.today():
        end = date.today()

    try:
        result = db.session.execute(
            text("CALL sp_graphicdata(:rc_id, :start, :end, :variable)"),
            {
                "rc_id": rc_id,
                "start": start,
                "end": end,
                "variable": variable
            }
        )

        rows = result.fetchall()

    except Exception as e:
        print("ERRO NA PROCEDURE:", repr(e))
        raise

    return [
        {
            "day": row[0].strftime("%Y-%m-%d"),
            "avgHour": int(row[1]),
            variable: float(row[2])
        }
        for row in rows
    ]


# Buscar e normalizar dados
def get_historical_variable_data(rc_id, variable, start_date, end_date):
    """
    Recupera todas as entradas do banco de dados para uma variável específica.
    Dentro de um intervalo de tempo para uma estação específica.
    """
    
    # 1. Map string input to SQLAlchemy column
    # Valid variable names map to database columns
    column_mapping = {
        "temp": RaspData.temp,
        "humidity": RaspData.humidity,
        "pressure": RaspData.pressure,
        "wind_speed": RaspData.wind_speed,
    }

    selected_column = column_mapping.get(variable)

    if selected_column is None:
        raise ValueError(f"Invalid variable: {variable}. Available: {list(column_mapping.keys())}")

    # 2. Date parsing
    try:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end_dt = datetime.strptime(end_date, "%Y-%m-%d") 
        # Add 1 day to end_date to include the full last day (until 23:59:59)
        end = end_dt + timedelta(days=1)
    except ValueError:
        raise ValueError("Invalid date format. Use YYYY-MM-DD")

    # 3. Prevent future queries
    today_limit = datetime.combine(date.today(), datetime.min.time()) + timedelta(days=1)
    if end > today_limit:
        end = today_limit

    # 4. Query raw data (No grouping, just filtering and sorting)
    results = (
        RaspData.query
        .with_entities(
            RaspData.timestamp,
            selected_column.label("value")
        )
        .filter(
            RaspData.rcID == rc_id,
            RaspData.timestamp >= start,
            RaspData.timestamp < end
        )
        .order_by(asc(RaspData.timestamp)) # Chronological order
        .all()
    )

    # 5. Format output
    return [
        {
            "timestamp": r.timestamp.isoformat(),
            "value": r.value
        }
        for r in results
    ]


# Formatar dados para exportação formato CSV
def get_historical_variable_csv(rc_id, variable, start_date, end_date):

    data = get_historical_variable_data(
        rc_id=rc_id,
        variable=variable,
        start_date=start_date,
        end_date=end_date
    )

    output = io.StringIO()
    output.write("\ufeff")

    writer = csv.writer(output, delimiter=";")

    variable_label = VARIABLE_LABEL_MAP.get(variable, variable)
    writer.writerow(["Data", "Hora", variable_label])

    for row in data:
        dt = datetime.fromisoformat(row["timestamp"])
        date_str = dt.strftime("%Y-%m-%d")
        time_str = dt.strftime("%H:%M")

        value = f"{row['value']}".replace(".", ",")

        writer.writerow([date_str, time_str, value])

    csv_content = output.getvalue()
    output.close()

    return csv_content


def export_historical_variable_csv(rc_id, variable, start_date, end_date):
    # Buscar estação
    station = RaspClient.query.filter_by(rcID=rc_id).first()
    if not station:
        raise ValueError("Station not found")

    # Gera csv
    csv_data = get_historical_variable_csv(
        rc_id, variable, start_date, end_date
    )

    # Monta filename
    safe_station = safe_filename(station.name or "estacao")
    safe_variable = VARIABLE_FILENAME_MAP.get(variable, variable)

    filename = f"{safe_station}_{safe_variable}_{start_date}_{end_date}.csv"

    return csv_data, filename

