from flask import Flask, app
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO
from flasgger import Swagger
from .database import db
from .routes.forecast_routes import forecast_bp
from .routes.station_routes import station_bp
from .routes.auth_routes import auth_bp
from .routes.external_routes import external_bp
from .routes.history_routes import history_bp
import os
from dotenv import load_dotenv

load_dotenv()

socketio = SocketIO(cors_allowed_origins="*")
jwt = JWTManager()

def create_app(testing=False, database_uri=None):
    app = Flask(__name__)

    if testing:
        app.config["TESTING"] = True
    
    if database_uri:
        app.config["SQLALCHEMY_DATABASE_URI"] = database_uri
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI")

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # JWT
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")

    # Swagger
    app.config["SWAGGER"] = {
        "title": "LabClima - API de Monitoramento Climático",
        "uiversion": 3,
        'securityDefinitions': {
            'Bearer': {
                'type': 'apiKey',
                'name': 'Authorization',
                'in': 'header',
                'description': 'Add: Bearer <JWT>'
            }
        }
    }

    Swagger(app)

    CORS(app, resources={r"/*": {"origins": "*"}})

    db.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*")
    jwt.init_app(app)

    # Blueprints
    app.register_blueprint(auth_bp, url_prefix="/api")
    app.register_blueprint(station_bp, url_prefix="/api")
    app.register_blueprint(external_bp, url_prefix="/api")
    app.register_blueprint(history_bp, url_prefix="/api" )
    app.register_blueprint(forecast_bp, url_prefix="/api")

    return app
