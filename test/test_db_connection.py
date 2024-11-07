import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.db_mysql import save_query
# Prueba la conexión y guarda una consulta
if __name__ == "__main__":
    save_query("FGTH", "Predicción simulada", "192.168.1.1")
