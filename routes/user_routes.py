# routes/user_routes.py
from flask import Blueprint, request, jsonify
from services.user_services import create_user
from services.user_services import login_user
from services.user_services import get_user_by_email
import logging

logger = logging.getLogger(__name__)
user_bp = Blueprint('user', __name__)

@user_bp.route('/register', methods=['POST'])
def register_user():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "Dados JSON ausentes"}), 400

        full_name = data.get('full_name')
        email = data.get('email')
        password_hash = data.get('password_hash')

        if not all([full_name, email, password_hash]):
            return jsonify({"error": "Campos obrigatórios: full_name, email, password_hash"}), 400

        result = create_user(full_name, email, password_hash)
        return jsonify(result), 201

    except Exception as e:
        logger.error(f"Erro ao registrar usuário: {str(e)}")
        return jsonify({"error": str(e)}), 500

@user_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        if not all([email, password]):
            return jsonify({"error": "Campos obrigatórios: email e password"}), 400

        result = login_user(email, password)
        return jsonify(result), 200

    except Exception as e:
        logger.error(f"Erro ao fazer login: {str(e)}")
        return jsonify({"error": str(e)}), 401

@user_bp.route('/users/email/<email>', methods=['GET'])
def get_user_by_email_route(email):
    try:
        result = get_user_by_email(email)
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Erro ao buscar usuário por e-mail: {str(e)}")
        return jsonify({"error": str(e)}), 404
