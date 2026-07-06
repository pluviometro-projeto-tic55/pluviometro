#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import time
import statistics
import pymysql
import logging
import board
import smbus2
import bme280
import socket
import uuid
import sqlite3
from datetime import datetime

# sensorscript v3 com buffer SQLite

# ============================================
# SQLITE BUFFER
# ============================================
SQLITE_DB_PATH = os.path.expanduser("~/.config/station/buffer_sensores.db")


def init_sqlite():
    """
    Cria o banco SQLite local e a tabela de buffer caso ainda não existam.
    """

    os.makedirs(
        os.path.dirname(SQLITE_DB_PATH),
        exist_ok=True
    )

    conn = sqlite3.connect(SQLITE_DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS buffer_raspdata (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rcID INTEGER NOT NULL,
            Temp REAL,
            Humidity REAL,
            Pressure REAL,
            Lux REAL,
            created_at TEXT NOT NULL
        )
        """
    )

    conn.commit()
    conn.close()


def save_to_sqlite(rcID, temp, hum, press, lux):
    """
    Salva a leitura no SQLite local.
    """

    conn = sqlite3.connect(SQLITE_DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO buffer_raspdata
        (
            rcID,
            Temp,
            Humidity,
            Pressure,
            Lux,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            rcID,
            temp,
            hum,
            press,
            lux,
            datetime.now().isoformat(timespec="seconds")
        )
    )

    conn.commit()
    conn.close()


def has_internet():
    """
    Testa se existe conexão com a internet.
    """

    try:
        conn = socket.create_connection(
            ("8.8.8.8", 53),
            timeout=5
        )
        conn.close()
        return True

    except OSError:
        return False


# ============================================
# LEITURA DO RCID ID DA ESTACAO
# ============================================
def get_rcid():

    try:
        path = os.path.expanduser("~/.config/station/rcid.txt")

        with open(path, "r") as f:
            return int(f.read().strip())

    except Exception as e:
        print(f"Erro ao ler rcID: {e}")
        return None


# ============================================
# I2C
# ============================================
bus = smbus2.SMBus(1)

# ============================================
# INICIALIZAÇÃO DOS SENSORES
# ============================================
HAS_BME280 = False
HAS_BH1750 = False

# BME280
try:

    bme280_addr = 0x76

    bme280.load_calibration_params(
        bus,
        bme280_addr
    )

    HAS_BME280 = True

    print("[OK] BME280 detectado.")

except Exception:
    print("[AVISO] BME280 não encontrado.")

# BH1750
try:

    bh1750_addr = 0x23
    bh1750_mode = 0x10

    bus.write_byte(
        bh1750_addr,
        bh1750_mode
    )

    HAS_BH1750 = True

    print("[OK] BH1750 detectado.")

except Exception:
    print("[AVISO] BH1750 não encontrado.")

# nenhum sensor
if not HAS_BME280 and not HAS_BH1750:

    print("ERRO CRÍTICO: Nenhum sensor detectado.")

    exit(1)


# ============================================
# LEITURA DOS SENSORES
# ============================================
def read_bme280():

    if not HAS_BME280:
        return None

    try:

        data = bme280.sample(
            bus,
            bme280_addr
        )

        return (
            data.temperature,
            data.humidity,
            data.pressure
        )

    except Exception as e:

        logging.error(
            f"Erro BME280: {e}"
        )

        return None


def read_bh1750():

    if not HAS_BH1750:
        return None

    try:

        data = bus.read_i2c_block_data(
            bh1750_addr,
            bh1750_mode,
            2
        )

        raw = (data[0] << 8) | data[1]

        return raw / 1.2

    except Exception as e:

        logging.error(
            f"Erro BH1750: {e}"
        )

        return None


# ============================================
# FILTRO DE DADOS
# ============================================
def is_valid(temp, hum, press, lux):

    if temp is not None and (
        temp < -30 or temp > 70
    ):
        return False

    if hum is not None and (
        hum < 0 or hum > 100
    ):
        return False

    if press is not None and (
        press < 800 or press > 1200
    ):
        return False

    if lux is not None and lux < 0:
        return False

    return True


def is_suspicious_humidity(humidity_values):
    """
    Detecta leituras de umidade possivelmente travadas em 100%.
    """

    return (
        humidity_values
        and len(humidity_values) >= 6
        and all(h == 100.0 for h in humidity_values)
    )


# ============================================
# BANCO MARIADB
# ============================================
DB_HOST = "DB_HOST_PLACEHOLDER"
DB_USER = "DB_USER_PLACEHOLDER"
DB_PASS = "DB_PASS_PLACEHOLDER"
DB_NAME = "DB_NAME_PLACEHOLDER"


def db_connect():

    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME,
        connect_timeout=5
    )


def sync_sqlite_to_mariadb():
    """
    Envia todos os dados pendentes do SQLite para o MariaDB.

    Só apaga do SQLite depois que o INSERT no MariaDB der certo.
    """

    if not has_internet():

        logging.warning(
            "Sem internet. Dados continuarão no SQLite."
        )

        return

    sqlite_conn = None
    maria_conn = None

    try:

        sqlite_conn = sqlite3.connect(SQLITE_DB_PATH)
        sqlite_conn.row_factory = sqlite3.Row
        sqlite_cursor = sqlite_conn.cursor()

        sqlite_cursor.execute(
            """
            SELECT
                id,
                rcID,
                Temp,
                Humidity,
                Pressure,
                Lux,
                created_at
            FROM buffer_raspdata
            ORDER BY id ASC
            """
        )

        rows = sqlite_cursor.fetchall()

        if not rows:

            logging.info(
                "Nenhum dado pendente no SQLite."
            )

            return

        maria_conn = db_connect()
        maria_cursor = maria_conn.cursor()

        total_enviados = 0

        for row in rows:

            try:

                maria_cursor.execute(
                    """
                    INSERT INTO raspdata
                    (
                        rcID,
                        Temp,
                        Humidity,
                        Pressure,
                        Lux
                    )
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (
                        row["rcID"],
                        row["Temp"],
                        row["Humidity"],
                        row["Pressure"],
                        row["Lux"]
                    )
                )

                maria_conn.commit()

                sqlite_cursor.execute(
                    """
                    DELETE FROM buffer_raspdata
                    WHERE id = ?
                    """,
                    (row["id"],)
                )

                sqlite_conn.commit()

                total_enviados += 1

            except Exception as e:

                maria_conn.rollback()

                logging.error(
                    f"Erro ao enviar dado SQLite id={row['id']} "
                    f"para MariaDB: {e}"
                )

                break

        logging.info(
            f"Sincronização finalizada. "
            f"{total_enviados} registro(s) enviado(s)."
        )

    except Exception as e:

        logging.error(
            f"Erro geral na sincronização SQLite -> MariaDB: {e}"
        )

    finally:

        if maria_conn:
            maria_conn.close()

        if sqlite_conn:
            sqlite_conn.close()


def update_ip_mac(rcID):
    """
    Atualiza IP e MAC no MariaDB se houver conexão.
    """

    if not has_internet():

        logging.warning(
            "Sem internet. Pulando atualização de IP/MAC."
        )

        return

    mac_atual = "{:012X}".format(
        uuid.getnode()
    )

    try:

        s = socket.socket(
            socket.AF_INET,
            socket.SOCK_DGRAM
        )

        s.connect(("8.8.8.8", 80))

        ip_atual = s.getsockname()[0]

        s.close()

        conn = db_connect()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT IP, MAC
            FROM raspclient
            WHERE rcID = %s
            """,
            (rcID,)
        )

        db_data = cursor.fetchone()

        if not db_data or (
            ip_atual != db_data[0]
            or mac_atual != db_data[1]
        ):

            cursor.execute(
                """
                UPDATE raspclient
                SET IP = %s,
                    MAC = %s
                WHERE rcID = %s
                """,
                (
                    ip_atual,
                    mac_atual,
                    rcID
                )
            )

            conn.commit()

            logging.info(
                f"IP/MAC atualizados: "
                f"{ip_atual} | {mac_atual}"
            )

        conn.close()

    except Exception as e:

        logging.error(
            f"Erro sincronização IP/MAC: {e}"
        )


# ============================================
# LOOP PRINCIPAL
# ============================================
def main():

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    logging.info("Iniciando coleta...")

    init_sqlite()

    rcID = get_rcid()

    if rcID is None:

        logging.error(
            "rcID não encontrado"
        )

        return

    update_ip_mac(rcID)

    # ============================================
    # BUFFERS DAS MÉDIAS
    # ============================================
    m_temp = []
    m_hum = []
    m_press = []
    m_lux = []

    # evita salvar repetido
    last_saved_data = None

    last_send = time.time()

    # ============================================
    # LOOP
    # ============================================
    while True:

        # leitura sensores
        bme = read_bme280()
        lux = read_bh1750()

        if bme is not None:

            temp, hum, press = bme

        else:

            temp = None
            hum = None
            press = None

        # validação
        if is_valid(
            temp,
            hum,
            press,
            lux
        ):

            if temp is not None:
                m_temp.append(temp)

            if hum is not None:
                m_hum.append(hum)

            if press is not None:
                m_press.append(press)

            if lux is not None:
                m_lux.append(lux)

        # ============================================
        # SALVA A CADA 5 MINUTOS
        # ============================================
        if time.time() - last_send >= 300:

            has_data = any([
                m_temp,
                m_hum,
                m_press,
                m_lux
            ])

            if has_data:

                avg_temp = (
                    round(statistics.mean(m_temp), 2)
                    if m_temp else None
                )

                avg_hum = (
                    round(statistics.mean(m_hum), 2)
                    if m_hum else None
                )

                if avg_hum == 100.0 and is_suspicious_humidity(m_hum):

                    logging.warning(
                        "Possível umidade travada em 100%. "
                        "A leitura de umidade do período não será gravada."
                    )

                    avg_hum = None

                avg_press = (
                    round(statistics.mean(m_press), 2)
                    if m_press else None
                )

                avg_lux = (
                    round(statistics.mean(m_lux), 2)
                    if m_lux else None
                )

                current_data = (
                    avg_temp,
                    avg_hum,
                    avg_press,
                    avg_lux
                )

                # ============================================
                # EVITA DUPLICADOS
                # ============================================
                if last_saved_data == current_data:

                    logging.info(
                        "Dados repetidos. Ignorando salvamento no SQLite."
                    )

                else:

                    try:

                        save_to_sqlite(
                            rcID,
                            avg_temp,
                            avg_hum,
                            avg_press,
                            avg_lux
                        )

                        last_saved_data = current_data

                        logging.info(
                            f"Dados salvos no SQLite: "
                            f"T={avg_temp} "
                            f"H={avg_hum} "
                            f"P={avg_press} "
                            f"L={avg_lux}"
                        )

                    except Exception as e:

                        logging.error(
                            f"Erro ao salvar no SQLite: {e}"
                        )

                # ============================================
                # TENTA SINCRONIZAR COM O MARIADB
                # ============================================
                sync_sqlite_to_mariadb()

            else:

                logging.warning(
                    "Nenhuma leitura válida nos últimos 5 minutos."
                )

            # limpa buffers
            m_temp.clear()
            m_hum.clear()
            m_press.clear()
            m_lux.clear()

            last_send = time.time()

        time.sleep(10)


if __name__ == "__main__":
    main()