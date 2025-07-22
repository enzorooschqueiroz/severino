# app.py
from flask import Flask, jsonify
from datetime import datetime
import os
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_app():
    """Factory para criar a aplicação Flask"""
    app = Flask(__name__)
    
    # Configurações básicas
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-change-in-production')
    
    # Registrar rotas
    register_routes(app)
    
    # Handler de erro global
    register_error_handlers(app)
    
    return app

def register_routes(app):
    """Registrar todas as rotas"""
    
    @app.route('/health', methods=['GET'])
    def health_check():
        """Health check endpoint - verificar se a API está funcionando"""
        try:
            return jsonify({
                'status': 'healthy',
                'timestamp': datetime.utcnow().isoformat(),
                'service': 'auth-api',
                'version': '1.0.0'
            }), 200
        except Exception as e:
            logger.error(f"Health check falhou: {str(e)}")
            return jsonify({
                'status': 'unhealthy',
                'timestamp': datetime.utcnow().isoformat(),
                'error': str(e)
            }), 500
    
    @app.route('/', methods=['GET'])
    def root():
        """Endpoint raiz com informações da API"""
        return jsonify({
            'service': 'Auth API',
            'version': '1.0.0',
            'status': 'running',
            'endpoints': {
                'health': '/health',
                'docs': 'Em breve...'
            }
        }), 200

def register_error_handlers(app):
    """Registrar handlers de erro globais"""
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'error': 'Endpoint não encontrado',
            'status_code': 404
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f"Erro interno: {str(error)}")
        return jsonify({
            'error': 'Erro interno do servidor',
            'status_code': 500
        }), 500
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'error': 'Método não permitido',
            'status_code': 405
        }), 405

if __name__ == '__main__':
    app = create_app()
    
    # Configurações de execução
    debug_mode = os.getenv('FLASK_ENV') == 'development'
    port = int(os.getenv('PORT', 5000))
    
    logger.info(f"Iniciando aplicação na porta {port}")
    logger.info(f"Modo debug: {debug_mode}")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug_mode
    )