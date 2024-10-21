import sys
import os

# Añadir el directorio del proyecto al sys.path
sys.path.insert(0, os.path.dirname(__file__))

# Importar create_app para obtener la aplicación
from app import create_app

# Crear la aplicación Flask
application = create_app()
