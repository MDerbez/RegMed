import pyodbc
import sqlite3
import os
from datetime import datetime

class DatabaseMigrator:
    def __init__(self, sqlite_path, sql_server_connection_string):
        self.sqlite_path = sqlite_path
        self.sql_server_connection_string = sql_server_connection_string
    
    def connect_sqlite(self):
        """Conecta a SQLite"""
        conn = sqlite3.connect(self.sqlite_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def connect_sqlserver(self):
        """Conecta a SQL Server"""
        return pyodbc.connect(self.sql_server_connection_string)
    
    def create_sqlserver_tables(self, sql_conn):
        """Crea las tablas en SQL Server"""
        cursor = sql_conn.cursor()
        
        # Tabla users
        cursor.execute("""
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='users' AND xtype='U')
        CREATE TABLE users (
            id INT IDENTITY(1,1) PRIMARY KEY,
            username NVARCHAR(255) UNIQUE NOT NULL,
            hash NVARCHAR(255) NOT NULL,
            rol NVARCHAR(50) NOT NULL
        )
        """)
        
        # Tabla Pacientes
        cursor.execute("""
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Pacientes' AND xtype='U')
        CREATE TABLE Pacientes (
            UsersId INT PRIMARY KEY,
            NombreCompleto NVARCHAR(255),
            Nombre NVARCHAR(100),
            PrimerApellido NVARCHAR(100),
            SegundoApellido NVARCHAR(100),
            FechaNacimiento NVARCHAR(50),
            EntidadDeNacimiento NVARCHAR(10),
            SexoBiologico NVARCHAR(50),
            Genero NVARCHAR(50),
            CURP NVARCHAR(18),
            Domicilio NVARCHAR(500),
            eMailPaciente NVARCHAR(255),
            TelefonoPaciente NVARCHAR(20),
            WhatsAppPaciente NVARCHAR(20),
            PacienteActivo INT DEFAULT 1,
            FechaUltimoMovimiento NVARCHAR(50),
            FOREIGN KEY (UsersId) REFERENCES users (id)
        )
        """)
        
        # Resto de tablas...
        tables_sql = [
            """
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='planes_de_cuidados' AND xtype='U')
            CREATE TABLE planes_de_cuidados (
                id INT IDENTITY(1,1) PRIMARY KEY,
                users_id INT,
                fecha NVARCHAR(50),
                acciones NVARCHAR(MAX),
                detecciones NVARCHAR(MAX),
                estado_mental NVARCHAR(MAX),
                riesgo_caidas NVARCHAR(MAX),
                riesgo_ulceras NVARCHAR(MAX),
                riesgo_pie_diabetico NVARCHAR(MAX),
                heridas NVARCHAR(MAX),
                estomas NVARCHAR(MAX),
                aseo NVARCHAR(MAX),
                medidas_posturales NVARCHAR(MAX),
                balance_liquidos NVARCHAR(MAX),
                dispositivos NVARCHAR(MAX),
                cuidados_via_aerea NVARCHAR(MAX),
                comentarios NVARCHAR(MAX),
                status NVARCHAR(50) DEFAULT 'Activo',
                FOREIGN KEY (users_id) REFERENCES users (id)
            )
            """,
            # Agregar más tablas según necesites...
        ]
        
        for table_sql in tables_sql:
            cursor.execute(table_sql)
        
        sql_conn.commit()
        print("Tablas creadas en SQL Server")
    
    def migrate_table(self, table_name, sqlite_conn, sql_conn):
        """Migra una tabla específica"""
        sqlite_cursor = sqlite_conn.cursor()
        sql_cursor = sql_conn.cursor()
        
        # Obtener datos de SQLite
        sqlite_cursor.execute(f"SELECT * FROM {table_name}")
        rows = sqlite_cursor.fetchall()
        
        if not rows:
            print(f"No hay datos en tabla {table_name}")
            return
        
        # Obtener columnas
        columns = [description[0] for description in sqlite_cursor.description]
        
        # Preparar INSERT para SQL Server
        if table_name == 'users':
            # Para users, incluir IDENTITY_INSERT
            placeholders = ', '.join(['?' for _ in columns])
            columns_str = ', '.join(columns)
            
            sql_cursor.execute(f"SET IDENTITY_INSERT {table_name} ON")
            
            for row in rows:
                sql_cursor.execute(
                    f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})",
                    tuple(row)
                )
            
            sql_cursor.execute(f"SET IDENTITY_INSERT {table_name} OFF")
        
        elif table_name == 'Pacientes':
            # Para Pacientes, usar UsersId como clave
            placeholders = ', '.join(['?' for _ in columns])
            columns_str = ', '.join(columns)
            
            for row in rows:
                sql_cursor.execute(
                    f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})",
                    tuple(row)
                )
        
        sql_conn.commit()
        print(f"Migrados {len(rows)} registros de tabla {table_name}")
    
    def migrate_all(self):
        """Migra toda la base de datos"""
        sqlite_conn = self.connect_sqlite()
        sql_conn = self.connect_sqlserver()
        
        try:
            # Crear tablas en SQL Server
            self.create_sqlserver_tables(sql_conn)
            
            # Migrar datos en orden correcto (respetando foreign keys)
            tables_order = [
                'users',
                'Pacientes', 
                'planes_de_cuidados',
                'sintomas',
                'eventos',
                'somatometria',
                'documentos',
                'prescripciones'
            ]
            
            for table in tables_order:
                try:
                    self.migrate_table(table, sqlite_conn, sql_conn)
                except Exception as e:
                    print(f"Error migrando tabla {table}: {e}")
            
            print("Migración completada exitosamente!")
            
        except Exception as e:
            print(f"Error durante la migración: {e}")
        finally:
            sqlite_conn.close()
            sql_conn.close()

# Ejemplo de uso
if __name__ == "__main__":
    # Configurar conexión a SQL Server
    # Cambia estos valores por los de tu servidor SQL
    server = 'tu_servidor'
    database = 'RegMed'
    username = 'tu_usuario'  
    password = 'tu_password'
    
    # String de conexión
    connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
    
    # Ruta a SQLite
    sqlite_path = os.path.join(os.path.dirname(__file__), "pacientes.db")
    
    # Crear y ejecutar migrador
    migrator = DatabaseMigrator(sqlite_path, connection_string)
    migrator.migrate_all()