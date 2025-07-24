# services/user_services.py
from config.supabase_client import supabase
from utils.password_hashing import hash_password, verify_password
from utils.jwt_implementation import generate_jwt
from models.user_model import UserCreate
import logging

logger = logging.getLogger(__name__)

def create_user(full_name: str, email: str, password_hash: str):
    try:
        hashed_password = hash_password(password_hash)
        user_data = {
            "full_name": full_name,
            "email": email,
            "password_hash": hashed_password
        }
        response = supabase.table("users").insert(user_data).execute()
        return response.data
    except Exception as e:
        logger.error(f"Erro ao criar usuário: {str(e)}")
        raise

def login_user(email: str, password: str):
    
    try:
        # Buscar o usuário no Supabase
        response = supabase.table("users").select("*").eq("email", email).execute()
        users = response.data

        if not users:
            raise Exception("Usuário não encontrado")

        user = users[0]
        if not verify_password(password, user["password_hash"]):
            raise Exception("Senha incorreta")

        token = generate_jwt({
            "user_id": user["id"],
            "email": user["email"]
        })

        return {
            "access_token": token,
            "token_type": "bearer"
        }

    except Exception as e:
        logger.error(f"Erro ao fazer login: {str(e)}")
        raise

def get_user_by_email(email: str):
    try:
        response = supabase.table("users").select("*").eq("email", email).single().execute()
        if not response.data:
            raise Exception("Usuário não encontrado")
        return response.data
    except Exception as e:
        logger.error(f"Erro ao buscar usuário por e-mail: {str(e)}")
        raise

