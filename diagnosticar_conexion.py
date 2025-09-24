import pyodbc

def diagnosticar_conexion():
    try:
        # Conectar a la base de datos Jomquer (como lo hace tu app)
        connection_string = (
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=LENOVO-MDP\\SQLEXPRESS;"
            "DATABASE=Jomquer;"
            "Trusted_Connection=yes"
        )
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()
        
        print("🔍 DIAGNÓSTICO DE CONEXIÓN")
        print("=" * 50)
        
        # Mostrar base de datos actual
        cursor.execute("SELECT DB_NAME()")
        db_actual = cursor.fetchone()[0]
        print(f"📊 Base de datos actual: {db_actual}")
        
        # Mostrar tablas en esta BD
        cursor.execute("""
            SELECT TABLE_NAME, 
                   (SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = t.TABLE_NAME) as COLUMNAS
            FROM INFORMATION_SCHEMA.TABLES t
            WHERE TABLE_TYPE = 'BASE TABLE'
            ORDER BY TABLE_NAME
        """)
        
        tablas = cursor.fetchall()
        print(f"\n📋 Tablas en base de datos '{db_actual}':")
        for tabla in tablas:
            nombre, columnas = tabla
            print(f"   - {nombre} ({columnas} columnas)")
        
        # Contar registros en tabla users
        try:
            cursor.execute("SELECT COUNT(*) FROM users")
            count_users = cursor.fetchone()[0]
            print(f"\n👥 Registros en tabla 'users': {count_users}")
            
            if count_users > 0:
                cursor.execute("SELECT id, username, rol FROM users")
                usuarios = cursor.fetchall()
                print("   Usuarios:")
                for user in usuarios:
                    print(f"     - ID {user[0]}: {user[1]} ({user[2]})")
        except Exception as e:
            print(f"❌ Error accediendo tabla users: {e}")
        
        # Contar registros en tabla Pacientes
        try:
            cursor.execute("SELECT COUNT(*) FROM Pacientes")
            count_pacientes = cursor.fetchone()[0]
            print(f"\n🏥 Registros en tabla 'Pacientes': {count_pacientes}")
            
            if count_pacientes > 0:
                cursor.execute("SELECT usersId, NombreCompleto FROM Pacientes")
                pacientes = cursor.fetchall()
                print("   Pacientes:")
                for paciente in pacientes:
                    print(f"     - ID {paciente[0]}: {paciente[1] or 'Sin nombre'}")
        except Exception as e:
            print(f"❌ Error accediendo tabla Pacientes: {e}")
            
        conn.close()
        
        # Ahora verificar otras bases de datos
        print(f"\n🔍 VERIFICANDO OTRAS BASES DE DATOS")
        print("=" * 50)
        
        # Conectar sin especificar BD
        connection_string_master = (
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=LENOVO-MDP\\SQLEXPRESS;"
            "Trusted_Connection=yes"
        )
        conn = pyodbc.connect(connection_string_master)
        cursor = conn.cursor()
        
        # Listar todas las bases de datos
        cursor.execute("""
            SELECT name FROM sys.databases 
            WHERE name NOT IN ('master', 'tempdb', 'model', 'msdb')
            ORDER BY name
        """)
        
        bases_datos = cursor.fetchall()
        print("📊 Bases de datos disponibles:")
        for bd in bases_datos:
            print(f"   - {bd[0]}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error en diagnóstico: {e}")

if __name__ == "__main__":
    diagnosticar_conexion()