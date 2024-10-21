import os

class Config:
    # Configuraciones generales
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    # Configuración de la base de datos
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql://user:password@localhost/db_name'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
