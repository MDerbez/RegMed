import sqlite3
import os

def analyze_sqlite_structure():
    """Analiza la estructura real de la base de datos SQLite"""
    
    db_path = os.path.join(os.path.dirname(__file__), "pacientes.db")
    if not os.path.exists(db_path):
        print("No se encontró la base de datos pacientes.db")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Obtener lista de tablas
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    
    print("=== ESTRUCTURA DE BASE DE DATOS SQLITE ===\n")
    
    for table_name in tables:
        table_name = table_name[0]
        print(f"TABLA: {table_name}")
        print("-" * 50)
        
        # Obtener estructura de la tabla
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        
        print("Columnas:")
        for col in columns:
            cid, name, type_name, notnull, default_value, pk = col
            print(f"  {name} ({type_name}) - PK: {bool(pk)} - NOT NULL: {bool(notnull)}")
        
        # Contar registros
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        print(f"Registros: {count}")
        
        # Mostrar algunos datos de ejemplo si hay registros
        if count > 0:
            cursor.execute(f"SELECT * FROM {table_name} LIMIT 3")
            sample_data = cursor.fetchall()
            print("Datos de ejemplo:")
            for i, row in enumerate(sample_data, 1):
                print(f"  Registro {i}: {row}")
        
        print("\n")
    
    conn.close()

if __name__ == "__main__":
    analyze_sqlite_structure()