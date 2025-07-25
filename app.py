from flask import Flask
from config.supabase_client import supabase
from routes import register_routes
from errors.handlers import register_error_handlers
from logs.logger import logger
from services.supabase_test import test_supabase_connection
from flask_cors import CORS
import os

from routes.user_routes import user_bp

def create_app():
    app = Flask(__name__)

    CORS(app, resources={r"/*": {"origins": "*"}})
   
    register_routes(app)
    register_error_handlers(app)
    app.register_blueprint(user_bp)

    try:
        test_supabase_connection()
        logger.info("Conexão com Supabase estabelecida com sucesso.")
    except Exception as e:
        logger.error(f"Erro ao conectar com Supabase: {str(e)}")

    return app

if __name__ == '__main__':
    app = create_app()
    debug_mode = os.getenv('FLASK_ENV') == 'development'
    port = int(os.getenv('PORT', 5000))

    logger.info(f"Iniciando aplicação na porta {port}")
    logger.info(f"Modo debug: {debug_mode}")

    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug_mode
    )
