import pyodbc
from database.db_mysql import connect_to_database

def create_consultas_table():
    connection = connect_to_database()
    if connection is None:
        print("No se pudo conectar a la base de datos")
        return

    cursor = connection.cursor()

    create_table_query = """
    CREATE TABLE consultas (
        id BIGINT IDENTITY(1,1) PRIMARY KEY, -- Clave primaria con incremento automático
        sequence VARCHAR(255) NOT NULL,      -- Secuencia de texto
        prediction NVARCHAR(MAX) NOT NULL,   -- Resultado de predicción (tipo texto)
        user_ip VARCHAR(45) NOT NULL,        -- Dirección IP del usuario
        timestamp DATETIME DEFAULT GETDATE() -- Fecha y hora por defecto
    );
    """

    try:
        cursor.execute(create_table_query)
        connection.commit()
        print("Tabla 'consultas' creada correctamente")
    except Exception as e:
        print("Error al crear la tabla:", e)
    finally:
        cursor.close()
        connection.close()

if __name__ == "__main__":
    create_consultas_table()
