import sqlite3
import os
from datetime import datetime

def export_sqlite_to_sql():
    """Exporta datos de SQLite a script SQL para SQL Server"""
    
    # Conectar a la base de datos SQLite
    db_path = os.path.join(os.path.dirname(__file__), "pacientes.db")
    if not os.path.exists(db_path):
        print("No se encontró la base de datos pacientes.db")
        return
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Crear archivo SQL de salida
    output_file = f"export_regmed_{datetime.now().strftime('%Y%m%d_%H%M%S')}.sql"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("-- Script de migración de RegMed SQLite a SQL Server\n")
        f.write(f"-- Generado el: {datetime.now()}\n\n")
        
        # Crear estructura de tablas para SQL Server
        f.write("""-- Crear estructura de tablas
-- Tabla users
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='users' AND xtype='U')
CREATE TABLE users (
    id INT IDENTITY(1,1) PRIMARY KEY,
    username NVARCHAR(255) UNIQUE NOT NULL,
    hash NVARCHAR(255) NOT NULL,
    rol NVARCHAR(50) NOT NULL
);

-- Tabla Pacientes
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
);

-- Tabla planes_de_cuidados
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
);

-- Tabla sintomas
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='sintomas' AND xtype='U')
CREATE TABLE sintomas (
    id INT IDENTITY(1,1) PRIMARY KEY,
    date NVARCHAR(50),
    users_id INT,
    tipo NVARCHAR(100),
    descripcion NVARCHAR(MAX),
    FOREIGN KEY (users_id) REFERENCES users (id)
);

-- Tabla eventos
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='eventos' AND xtype='U')
CREATE TABLE eventos (
    id INT IDENTITY(1,1) PRIMARY KEY,
    date NVARCHAR(50),
    users_id INT,
    tipo INT,
    evento NVARCHAR(MAX),
    type INT,
    FOREIGN KEY (users_id) REFERENCES users (id)
);

-- Tabla somatometria
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='somatometria' AND xtype='U')
CREATE TABLE somatometria (
    id INT IDENTITY(1,1) PRIMARY KEY,
    users_id INT,
    fecha NVARCHAR(50),
    peso FLOAT,
    talla FLOAT,
    circ_abdominal FLOAT,
    temp FLOAT,
    sistolica INT,
    diastolica INT,
    fcard INT,
    fresp INT,
    o2 FLOAT,
    glucemia FLOAT,
    registrado_por INT,
    FOREIGN KEY (users_id) REFERENCES users (id),
    FOREIGN KEY (registrado_por) REFERENCES users (id)
);

-- Tabla documentos
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='documentos' AND xtype='U')
CREATE TABLE documentos (
    id INT IDENTITY(1,1) PRIMARY KEY,
    users_id INT,
    fecha NVARCHAR(50),
    tema NVARCHAR(255),
    tipo NVARCHAR(100),
    comentarios NVARCHAR(MAX),
    filename NVARCHAR(255),
    FOREIGN KEY (users_id) REFERENCES users (id)
);

-- Tabla prescripciones
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='prescripciones' AND xtype='U')
CREATE TABLE prescripciones (
    id INT IDENTITY(1,1) PRIMARY KEY,
    users_id INT,
    medicamento NVARCHAR(255),
    dosis NVARCHAR(100),
    cantidad NVARCHAR(100),
    via NVARCHAR(100),
    cada_cantidad NVARCHAR(100),
    cada_unidad NVARCHAR(100),
    unidad_medida NVARCHAR(100),
    desde NVARCHAR(50),
    durante_cantidad NVARCHAR(100),
    durante_unidad NVARCHAR(100),
    vigente NVARCHAR(10) DEFAULT 'Si',
    FOREIGN KEY (users_id) REFERENCES users (id)
);

-- Insertar datos
""")
        
        # Exportar datos de cada tabla
        tables = [
            'users', 'Pacientes', 'planes_de_cuidados', 'sintomas', 
            'eventos', 'somatometria', 'documentos', 'prescripciones'
        ]
        
        for table in tables:
            try:
                cursor.execute(f"SELECT * FROM {table}")
                rows = cursor.fetchall()
                
                if rows:
                    f.write(f"\n-- Datos de tabla {table}\n")
                    
                    # Obtener nombres de columnas
                    columns = [description[0] for description in cursor.description]
                    columns_str = ', '.join(columns)
                    
                    for row in rows:
                        values = []
                        for value in row:
                            if value is None:
                                values.append('NULL')
                            elif isinstance(value, str):
                                # Escapar comillas simples
                                escaped_value = value.replace("'", "''")
                                values.append(f"'{escaped_value}'")
                            else:
                                values.append(str(value))
                        
                        values_str = ', '.join(values)
                        
                        # Para users, usar SET IDENTITY_INSERT
                        if table == 'users':
                            f.write(f"SET IDENTITY_INSERT {table} ON;\n")
                            f.write(f"INSERT INTO {table} ({columns_str}) VALUES ({values_str});\n")
                            f.write(f"SET IDENTITY_INSERT {table} OFF;\n")
                        elif table in ['planes_de_cuidados', 'sintomas', 'eventos', 'somatometria', 'documentos', 'prescripciones']:
                            # Para tablas con IDENTITY, excluir la columna id del INSERT
                            columns_no_id = [col for col in columns if col != 'id']
                            values_no_id = [val for i, val in enumerate(values) if columns[i] != 'id']
                            
                            if columns_no_id:
                                columns_str_no_id = ', '.join(columns_no_id)
                                values_str_no_id = ', '.join(values_no_id)
                                f.write(f"INSERT INTO {table} ({columns_str_no_id}) VALUES ({values_str_no_id});\n")
                        else:
                            f.write(f"INSERT INTO {table} ({columns_str}) VALUES ({values_str});\n")
                    
                    f.write(f"-- Fin datos {table}\n\n")
                else:
                    f.write(f"-- No hay datos en tabla {table}\n\n")
                    
            except sqlite3.Error as e:
                f.write(f"-- Error al exportar tabla {table}: {e}\n\n")
    
    conn.close()
    print(f"Exportación completada. Archivo generado: {output_file}")
    return output_file

if __name__ == "__main__":
    export_sqlite_to_sql()