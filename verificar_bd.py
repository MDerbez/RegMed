import pyodbc

def verificar_base_datos():
    try:
        # Conectar al servidor sin especificar base de datos
        connection_string = (
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=LENOVO-MDP\\SQLEXPRESS;"
            "Trusted_Connection=yes"
        )
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()
        
        # Verificar si existe la base de datos Jomquer
        cursor.execute("SELECT name FROM sys.databases WHERE name = 'Jomquer'")
        db = cursor.fetchone()
        
        if db:
            print("✅ La base de datos 'Jomquer' ya existe")
            return True
        else:
            print("❌ La base de datos 'Jomquer' no existe")
            print("Creando la base de datos 'Jomquer'...")
            
            # Crear la base de datos
            cursor.execute("CREATE DATABASE Jomquer")
            cursor.commit()
            print("✅ Base de datos 'Jomquer' creada exitosamente")
            return True
            
    except Exception as e:
        print(f"Error: {e}")
        return False
    finally:
        if 'conn' in locals():
            conn.close()

def verificar_tablas():
    try:
        # Conectar a la base de datos Jomquer
        connection_string = (
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=LENOVO-MDP\\SQLEXPRESS;"
            "DATABASE=Jomquer;"
            "Trusted_Connection=yes"
        )
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()
        
        # Verificar tablas existentes
        cursor.execute("""
            SELECT TABLE_NAME 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_TYPE = 'BASE TABLE'
        """)
        
        tablas = [row[0] for row in cursor.fetchall()]
        
        if tablas:
            print("📋 Tablas existentes en la base de datos 'Jomquer':")
            for tabla in tablas:
                print(f"   - {tabla}")
        else:
            print("⚠️ No hay tablas en la base de datos 'Jomquer'")
            print("💡 Debes ejecutar el script SQL de migración: export_jomquer_corrected_20250924_105118.sql")
        
        return tablas
        
    except Exception as e:
        print(f"Error verificando tablas: {e}")
        return []
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    print("🔍 Verificando configuración de SQL Server...")
    if verificar_base_datos():
        verificar_tablas()