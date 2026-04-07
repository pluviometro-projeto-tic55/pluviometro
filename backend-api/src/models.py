from sqlalchemy.sql import func
from .database import db
import datetime

# ----Tabela RaspClient----
class RaspClient(db.Model):
    __tablename__ = 'RaspClient'

    "Classe para a tabela de cadastro das estações."

    # Identificador único da estação
    rcID = db.Column(db.Integer, primary_key=True)

    # Identificação do dispositivo
    serial = db.Column("Serial", db.String(50), nullable=False, unique=True)
    ip = db.Column("IP", db.String(30))  # IPv4 ou IPv6
    mac = db.Column("MAC", db.String(30))

    # Data e hora do cadastro
    timestamp = db.Column(db.DateTime, server_default=func.now())

    # Dados da estação
    name = db.Column("Name", db.String(50))
    latitude = db.Column("Latitude", db.Float)
    longitude = db.Column("Longitude", db.Float)
    height = db.Column("Height", db.Float)
    height_sea_level = db.Column("Height_sea_level", db.Float) #Altura relativa ao nível do mar
    local = db.Column("Local", db.String(255)) #Nome do local ou endereço
    contact = db.Column("Contact", db.String(50)) #Telefone de contato
    status = db.Column("Status", db.String(100))

    email = db.Column("Email", db.String(50))
    password = db.Column("Password", db.String(255), nullable=False)

    #Conexão com a tabela RaspData
    data_records = db.relationship("RaspData", backref = "client", lazy = True)

    #Conexão com a tabela Forecast
    forecasts = db.relationship("Forecast", backref = "client", lazy = True)


# ----Tabela RaspData----
class RaspData(db.Model):

    __tablename__ = 'RaspData'
    
    "Classe para a tabela que armazena os dados crus recebidos diretamente da estação."
    
    #Identificador único do registro
    rdID = db.Column(db.Integer, primary_key = True)

    #Identifica qual estação enviou os dados
    rcID = db.Column(db.Integer, db.ForeignKey("RaspClient.rcID"), nullable = False)

    timestamp = db.Column(db.DateTime, server_default = func.now())
    temp = db.Column(db.Float)
    humidity = db.Column(db.Float)
    pressure = db.Column(db.Float)
    lux = db.Column(db.Float)
    wind_speed = db.Column(db.Float)
    wind_direction = db.Column(db.String(16)) #Ex: N, NW, S, SE
    pluv = db.Column(db.Float) 

# ----Tabela Forecast----
class Forecast(db.Model):

    __tablename__ = 'Forecast'

    "Classe para a tabela que armazena as previsões meteorológicas"
    
    #Identificador único do registro
    fcID = db.Column(db.Integer, primary_key = True)
    
    #Identifica qual estação enviou os dados
    rcID = db.Column(db.Integer, db.ForeignKey("RaspClient.rcID"), nullable = False)

    timestamp = db.Column(db.DateTime, server_default = func.now())
    c_temp = db.Column(db.Float)
    c_humidity = db.Column(db.Float)
    c_pressure = db.Column(db.Float)
    c_wind_speed = db.Column(db.Float)
    c_wind_direction = db.Column(db.String(16))
    c_pluv = db.Column(db.Float) 
    c_lux = db.Column("c_Lux", db.Float) 

    rain_chance = db.Column(db.String(32))
    storm_chance = db.Column(db.String(32))
    general_summary = db.Column("General", db.String(128))
    temp_min = db.Column("Temp_min", db.Integer) 
    temp_max = db.Column("Temp_max", db.Integer)
    feels_like = db.Column("Feels_like", db.Integer) 





