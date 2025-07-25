from .health_routes import health_routes

def register_routes(app):
    app.register_blueprint(health_routes)
