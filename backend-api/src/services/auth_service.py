from passlib.hash import bcrypt
from flask_jwt_extended import create_access_token
from ..models import RaspClient

def login_user(email: str, password: str):
    user = RaspClient.query.filter_by(email=email).first()

    if not user or not bcrypt.verify(password, user.password):
        return None

    token = create_access_token(identity=str(user.rcID))

    return {
        "token": token,
        "user": {
            "rcID": user.rcID,
            "name": user.name
        }
    }
