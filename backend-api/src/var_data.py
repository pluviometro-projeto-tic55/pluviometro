import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sqlalchemy import asc, desc
from .models import RaspData
from .database import db

# função para preparar os dados para o modelo VAR
def prepare_var_data(rc_id, days=365):
    
    # pega o ultimo registro da estação selecionada
    last_record = RaspData.query.filter(RaspData.rcID == rc_id)\
        .order_by(desc(RaspData.timestamp))\
        .first()

    if not last_record:
        return None

    # usa a timestamp do ultimo registro para definir o intervalo
    end_date = last_record.timestamp
    start_date = end_date - timedelta(days=days)

    # consulta os dados da estação
    records = RaspData.query.filter(
        RaspData.rcID == rc_id,
        RaspData.timestamp >= start_date,
        RaspData.timestamp <= end_date 
    ).order_by(asc(RaspData.timestamp)).all()

    if not records:
        return None

    # coloca esses dados em uma lista de dicts
    data_list = [{
        'timestamp': record.timestamp,
        'temp': record.temp,
        'humidity': record.humidity,
        'pressure': record.pressure,
        'lux': record.lux,
        'wind_speed': record.wind_speed,
        'pluv': record.pluv,
    } for record in records]


    df = pd.DataFrame(data_list)

    # 
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.set_index('timestamp', inplace=True)

    # corrige intervalos irregulares para 'x' minutos exatos (30 nesse caso)
    df_resampled = df.resample('30min').mean()

    # interpola registros NaN
    df_interpolated = df_resampled.interpolate(method='time')

    # preenche quaisquer valores NaN restantes
    df_final = df_interpolated.bfill().ffill()
    
    # Trata colunas que ainda têm NaN (ex: wind_speed completamente vazio)
    # Substitui com a média da coluna ou com 0 se tudo for NaN
    for col in df_final.columns:
        if df_final[col].isna().any():
            col_mean = df_final[col].mean()
            if pd.isna(col_mean):
                # Se a coluna é toda NaN, usa 0
                df_final[col] = df_final[col].fillna(0)
            else:
                # Se há algum valor, usa a média
                df_final[col] = df_final[col].fillna(col_mean)

    return df_final