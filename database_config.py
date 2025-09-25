import os
import pyodbc
from contextlib import contextmanager

class DatabaseConfig:
    # Configuración para SQL Server
    SQL_SERVER_CONFIG = {
        'server': r'LENOVO-MDP\SQLEXPRESS',
        'database': 'Jomquer',  # Cambiar a 'Jomquer' como solicitas
        'driver': '{ODBC Driver 17 for SQL Server}',
        'trusted_connection': 'yes'
    }
    
    # Configuración para SQLite (fallback)
    SQLITE_PATH = os.path.join(os.path.dirname(__file__), "pacientes.db")

def get_sql_server_connection_string():
    """Construye la cadena de conexión para SQL Server"""
    config = DatabaseConfig.SQL_SERVER_CONFIG
    return (
        f"DRIVER={config['driver']};"
        f"SERVER={config['server']};"
        f"DATABASE={config['database']};"
        f"Trusted_Connection={config['trusted_connection']}"
    )

@contextmanager
def get_db_connection():
    """Context manager para conexiones de base de datos"""
    conn = None
    try:
        # Intentar conectar a SQL Server primero
        connection_string = get_sql_server_connection_string()
        conn = pyodbc.connect(connection_string)
        conn.autocommit = False  # Para manejar transacciones manualmente
        yield conn
    except Exception as sql_error:
        print(f"Error conectando a SQL Server: {sql_error}")
        print("Fallback a SQLite...")
        
        # Fallback a SQLite
        import sqlite3
        try:
            conn = sqlite3.connect(DatabaseConfig.SQLITE_PATH)
            conn.row_factory = sqlite3.Row
            yield conn
        except Exception as sqlite_error:
            print(f"Error conectando a SQLite: {sqlite_error}")
            raise
    finally:
        if conn:
            conn.close()

def test_sql_server_connection():
    """Prueba la conexión a SQL Server"""
    try:
        connection_string = get_sql_server_connection_string()
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()
        cursor.execute("SELECT @@VERSION")
        version = cursor.fetchone()[0]
        print(f"Conexión exitosa a SQL Server: {version}")
        conn.close()
        return True
    except Exception as e:
        print(f"Error conectando a SQL Server: {e}")
        return False

if __name__ == "__main__":
    # Probar la conexión
    test_sql_server_connection()