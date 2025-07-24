# utils/jwt_implementation.py
from dotenv import load_dotenv
import os 
import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify

load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def generate_jwt(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=ALGORITHM)
    return encoded_jwt

def decode_jwt(token: str) -> dict:
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise Exception("Token expirado")
    except jwt.InvalidTokenError:
        raise Exception("Token inválido")
    
def jwt_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get('Authorization', None)
        if not auth_header:
            return jsonify({"error": "Authorization header missing"}), 401

        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != "bearer":
            return jsonify({"error": "Invalid authorization header format"}), 401

        token = parts[1]

        try:
            payload = decode_jwt(token)
        except Exception as e:
            return jsonify({"error": str(e)}), 401

        # Coloca o payload no kwargs para usar dentro da rota, ex: user info
        kwargs['jwt_payload'] = payload

        return func(*args, **kwargs)
    return wrapper

def user_owns_resource(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        jwt_payload = kwargs.get('jwt_payload')
        user_id_from_token = jwt_payload.get('user_id')
        user_id_from_route = kwargs.get('user_id')

        if user_id_from_token != user_id_from_route:
            return jsonify({"error": "Acesso negado: usuário não autorizado"}), 403

        return func(*args, **kwargs)
    return wrapper
