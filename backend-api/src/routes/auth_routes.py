from flask import Blueprint, request, jsonify
from ..services.auth_service import login_user

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/auth/login", methods=["POST"])
def login():
    """
    Autentica usuário e retorna JWT
    ---
    tags:
      - Autenticação
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - email
            - password
          properties:
            email:
              type: string
              example: admin@estacao.com
            password:
              type: string
              example: admin@123
    responses:
      200:
        description: Login realizado com sucesso
        schema:
          type: object
          properties:
            token:
              type: string
              example: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
            user:
              type: object
              properties:
                rcID:
                  type: integer
                  example: 1
                name:
                  type: string
                  example: Estação Central
      400:
        description: Email ou senha não enviados
      401:
        description: Credenciais inválidas
    """

    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Invalid or missing JSON"}), 400

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    try:
        result = login_user(email, password)

        if not result:
            return jsonify({"error": "Invalid credentials"}), 401

        return jsonify(result), 200

    except Exception:
        return jsonify({"error": "Internal server error"}), 500