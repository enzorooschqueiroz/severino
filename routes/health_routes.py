from flask import Blueprint, jsonify
from datetime import datetime

health_routes = Blueprint('health', __name__)

@health_routes.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'service': 'auth-api',
        'version': '1.0.0'
    }), 200

@health_routes.route('/', methods=['GET'])
def root():
    return jsonify({
        'service': 'Auth API',
        'version': '1.0.0',
        'status': 'running',
        'endpoints': {
            'health': '/health',
            'docs': 'Em breve...'
        }
    }), 200
