from config.supabase_client import supabase
from utils.security import hash_password
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