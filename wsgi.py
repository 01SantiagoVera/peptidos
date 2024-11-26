from flask import Flask
from app.routes.web import web_bp
from app.routes.api import api_bp

# Crear la aplicación Flask y especificar la ruta de las plantillas
app = Flask(__name__, template_folder='resources/views')



# Registrar las rutas web y API
app.register_blueprint(web_bp)
app.register_blueprint(api_bp, url_prefix='/api')
if __name__ == '__main__':
    app.run(debug=True)