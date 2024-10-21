from flask import Flask
from .routes.web import web_bp
from .routes.api import api_bp


def create_app():
    app = Flask(__name__)

    # Cargar configuración
    app.config.from_pyfile('../config/config.py')

    # Registrar rutas
    app.register_blueprint(web_bp)
    app.register_blueprint(api_bp, url_prefix='/api')

    return app
