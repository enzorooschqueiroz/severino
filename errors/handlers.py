from flask import jsonify
from logs.logger import logger

def register_error_handlers(app):
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
