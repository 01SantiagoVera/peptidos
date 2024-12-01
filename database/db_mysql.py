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


def save_query(sequence, predictions, user_ip):
    """
    Guarda cada secuencia y predicción individualmente en la base de datos.

    :param sequence: Secuencia completa proporcionada por el usuario (string).
    :param predictions: Lista de predicciones para cada secuencia (list of dicts).
    :param user_ip: Dirección IP del usuario que realiza la consulta (string).
    """
    connection = connect_to_database()
    if connection is None:
        return  # Salir si no hay conexión

    cursor = connection.cursor()

    # Query de inserción ajustada para múltiples secuencias
    query = "INSERT INTO consultas (sequence, prediction, user_ip, timestamp) VALUES (?, ?, ?, GETDATE())"

    try:
        for prediction in predictions:
            # Obtener la secuencia individual y la predicción correspondiente
            individual_sequence = prediction.get("input_sequence", "N/A")
            prediction_str = str(prediction)

            # Valores a insertar
            values = (individual_sequence, prediction_str, user_ip)

            # Ejecutar la consulta
            cursor.execute(query, values)

        # Confirmar los cambios
        connection.commit()
        print("Consultas guardadas correctamente")
    except Exception as e:
        print("Error al guardar las consultas:", e)
        connection.rollback()
    finally:
        cursor.close()
        connection.close()
