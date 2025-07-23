from config.supabase_client import supabase
from logs.logger import logger

def test_supabase_connection():
    result = supabase.table("users").select("*").execute()
    logger.info(f"{len(result.data)} usuários encontrados no Supabase.")
