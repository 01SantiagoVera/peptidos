import pyodbc

def connect_to_database():
    # Configura la cadena de conexión
    connection_string = (
        "DRIVER={ODBC Driver 17 for SQL Server};"  # Asegúrate de que el controlador esté instalado
        "SERVER=localhost;"  # Por ejemplo: "localhost" o "127.0.0.1"
        "DATABASE=peptidos;"  # El nombre de tu base de datos
        "UID=client;"  # Tu nombre de usuario
        "PWD=1234;"  # Tu contraseña
    )

    # Intenta establecer la conexión
    try:
        connection = pyodbc.connect(connection_string)
        print("Conexión exitosa a la base de datos")
        return connection
    except Exception as e:
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