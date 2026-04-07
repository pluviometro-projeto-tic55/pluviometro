import pymysql
import socket
import uuid
import os

# ------------------------------------
# Conexao com o banco
# ------------------------------------
def db_connect():
    try:
        return pymysql.connect(
            host="000.000.000.000", ## ip do server onde o banco esta instalado
            user="root",
            password="ncssp",
            database="weatherdb"
        )
    except Exception as e:
        print(f"Error when connect database: {e}")
        return None

# ------------------------------------
# Armazenar o rcID localmente
# ------------------------------------
def save_rcid(rcid):
    try:
        with open(r"rcid.txt", "w") as f:
            f.write(str(rcid))
        print("rcID saved")
    except Exception as e:
        print(f"Error when save rcID: {e}")

# ------------------------------------
# Obter dados unicos
# ------------------------------------
def get_device_info():
    hostname = socket.gethostname()
    mac = hex(uuid.getnode())[2:].upper()
    return hostname, mac

# ------------------------------------
# Registrar no banco
# ------------------------------------
def register_device():
    hostname, mac = get_device_info()

    conn = db_connect()
    if conn is None:
        print("Error when connect database")
        return

    cursor = conn.cursor()

    # Verifica se ja existe no banco
    cursor.execute("SELECT rcID FROM RaspClient WHERE mac = %s", (mac,))
    result = cursor.fetchone()

    if result:
        rcID = result[0]
        print(f"Device already registered. rcID = {rcID}")
    else:
        cursor.execute("""
            INSERT INTO RaspClient (hostname, mac)
            VALUES (%s, %s)
        """, (hostname, mac))
        conn.commit()
        rcID = cursor.lastrowid
        print(f"New device registered. rcID = {rcID}")

    conn.close()

    # chama a funcao p/ salvar o rcID
    save_rcid(rcID)


# ------------------------------------
# execution
# ------------------------------------
if __name__ == "__main__":
    register_device()
