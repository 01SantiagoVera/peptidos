import pyodbc

server = 'localhost'
database = 'peptidos'
user = 'root'
password = '<PASSWORD>'
def connect_to_database():
    # Configura la cadena de conexión
    connection_string = (
        "DRIVER={ODBC Driver 17 for SQL Server};"  # Asegúrate de que el controlador esté instalado
        "SERVER=tu_servidor;"  # Por ejemplo: "localhost" o "127.0.0.1"
        "DATABASE=tu_base_de_datos;"  # El nombre de tu base de datos
        "UID=tu_usuario;"  # Tu nombre de usuario
        "PWD=tu_contraseña;"  # Tu contraseña
    )

    # Intenta establecer la conexión
    try:
        connection = pyodbc.connect(connection_string)
        print("Conexión exitosa a la base de datos")
        return connection
    except Exception as e:
        print("Error al conectar a la base de datos:", e)
        return None
