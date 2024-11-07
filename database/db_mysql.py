import pyodbc
from dotenv import load_dotenv
import os

# Cargar las variables de entorno del archivo .env
load_dotenv()

def connect_to_database():
    connection_string = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={os.getenv('DB_SERVER')};"
        f"DATABASE={os.getenv('DB_DATABASE')};"
        f"UID={os.getenv('DB_USER')};"
        f"PWD={os.getenv('DB_PASSWORD')};"
    )

    # Intenta establecer la conexión
    try:
        connection = pyodbc.connect(connection_string)
        print("Conexión exitosa a la base de datos")
        return connection
    except pyodbc.InterfaceError:
        print("Error de conexión: el controlador o servidor podría ser incorrecto.")
        return None
    except pyodbc.Error as e:
        print("Error al conectar a la base de datos:", e)
        return None

def save_query(sequence, prediction, user_ip):
    connection = connect_to_database()
    if connection is None:
        return  # Salir si no hay conexión

    cursor = connection.cursor()

    # Consulta SQL para insertar datos
    query = "INSERT INTO consultas (sequence, prediction, user_ip, timestamp) VALUES (?, ?, ?, GETDATE())"
    values = (sequence, prediction, user_ip)

    try:
        cursor.execute(query, values)
        connection.commit()
        print("Consulta guardada correctamente")
    except Exception as e:
        print("Error al guardar la consulta:", e)
    finally:
        cursor.close()
        connection.close()