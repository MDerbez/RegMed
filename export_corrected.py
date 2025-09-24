import sqlite3
import os
from datetime import datetime

def export_sqlite_to_sql_correct():
    """Exporta datos de SQLite a script SQL para SQL Server con estructura correcta"""
    
    # Conectar a la base de datos SQLite
    db_path = os.path.join(os.path.dirname(__file__), "pacientes.db")
    if not os.path.exists(db_path):
        print("No se encontró la base de datos pacientes.db")
        return
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Crear archivo SQL de salida
    output_file = f"export_regmed_corrected_{datetime.now().strftime('%Y%m%d_%H%M%S')}.sql"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("-- Script de migración de RegMed SQLite a SQL Server (Estructura Corregida)\n")
        f.write(f"-- Generado el: {datetime.now()}\n\n")
        
        # Crear estructura de tablas para SQL Server basada en la estructura real
        f.write("""-- Crear estructura de tablas basada en SQLite real
USE RegMed;
GO

-- Tabla users
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='users' AND xtype='U')
CREATE TABLE users (
    id INT IDENTITY(1,1) PRIMARY KEY,
    username NVARCHAR(255) UNIQUE NOT NULL,
    hash NVARCHAR(MAX) NOT NULL,
    rol NVARCHAR(50) NOT NULL
);
GO

-- Tabla Pacientes (estructura completa)
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Pacientes' AND xtype='U')
CREATE TABLE Pacientes (
    usersId INT PRIMARY KEY,
    Usuario NVARCHAR(255),
    Contrasena NVARCHAR(255),
    NombreCompleto NVARCHAR(255),
    Expediente NVARCHAR(255),
    Nombre NVARCHAR(100),
    PrimerApellido NVARCHAR(100),
    SegundoApellido NVARCHAR(100),
    FechaNacimiento NVARCHAR(50),
    EntidadDeNacimiento NVARCHAR(10),
    SexoCURP INT,
    SexoBiologico INT,
    Genero NVARCHAR(50),
    CURP NVARCHAR(18),
    EstadoMental NVARCHAR(255),
    GrupoRH NVARCHAR(10),
    DiagnosticoPrimario NVARCHAR(255),
    CIEPrimario NVARCHAR(50),
    SegundoDiagnostico NVARCHAR(255),
    SegundoCIE NVARCHAR(50),
    TercerDiagnostico NVARCHAR(255),
    TercerCIE NVARCHAR(50),
    Domicilio NVARCHAR(500),
    eMailPaciente NVARCHAR(255),
    TelefonoPaciente NVARCHAR(20),
    WhatsAppPaciente NVARCHAR(20),
    NombreContactoTutor NVARCHAR(255),
    ParentescoContactoTutor NVARCHAR(100),
    TelefonoContactoTutor NVARCHAR(20),
    WhatsAppContactoTutor NVARCHAR(20),
    PrimerContacto INT,
    PacienteActivo INT DEFAULT 1,
    FechaUltimoMovimiento NVARCHAR(50),
    Alergico INT DEFAULT 0,
    RiesgoCaidas INT DEFAULT 0,
    RiesgoUlceras INT DEFAULT 0,
    FOREIGN KEY (usersId) REFERENCES users (id)
);
GO

-- Tabla sintomas (estructura real)
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='sintomas' AND xtype='U')
CREATE TABLE sintomas (
    id INT IDENTITY(1,1) PRIMARY KEY,
    date NVARCHAR(50),
    users_id INT,
    tipo NVARCHAR(MAX),
    duracion NVARCHAR(255),
    intensidad NVARCHAR(255),
    descripcion NVARCHAR(MAX),
    FOREIGN KEY (users_id) REFERENCES users (id)
);
GO

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
GO

-- Tabla planes_de_cuidados (estructura completa)
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='planes_de_cuidados' AND xtype='U')
CREATE TABLE planes_de_cuidados (
    id INT IDENTITY(1,1) PRIMARY KEY,
    users_id INT,
    fecha NVARCHAR(50),
    riesgo_caidas NVARCHAR(MAX),
    estado_mental NVARCHAR(MAX),
    riesgo_ulceras NVARCHAR(MAX),
    riesgo_pie_diabetico NVARCHAR(MAX),
    heridas NVARCHAR(MAX),
    estomas NVARCHAR(MAX),
    aseo NVARCHAR(MAX),
    medidas_posturales NVARCHAR(MAX),
    balance_liquidos NVARCHAR(MAX),
    dispositivos NVARCHAR(MAX),
    cuidados_via_aerea NVARCHAR(MAX),
    status NVARCHAR(50) DEFAULT 'Activo',
    comentarios NVARCHAR(MAX),
    dieta NVARCHAR(MAX),
    rehabilitacion NVARCHAR(MAX),
    alergico NVARCHAR(MAX),
    detecciones NVARCHAR(MAX),
    acciones NVARCHAR(MAX),
    FOREIGN KEY (users_id) REFERENCES users (id)
);
GO

-- Tabla somatometria
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='somatometria' AND xtype='U')
CREATE TABLE somatometria (
    id INT IDENTITY(1,1) PRIMARY KEY,
    fecha NVARCHAR(50),
    peso FLOAT,
    talla FLOAT,
    imc FLOAT,
    circ_abdominal FLOAT,
    temp FLOAT,
    sistolica INT,
    diastolica INT,
    fcard INT,
    fresp INT,
    o2 INT,
    glucemia FLOAT,
    users_id INT,
    registrado_por INT,
    FOREIGN KEY (users_id) REFERENCES users (id),
    FOREIGN KEY (registrado_por) REFERENCES users (id)
);
GO

-- Tabla documentos
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='documentos' AND xtype='U')
CREATE TABLE documentos (
    id INT IDENTITY(1,1) PRIMARY KEY,
    users_id INT,
    fecha NVARCHAR(50),
    tipo NVARCHAR(255),
    tema NVARCHAR(255),
    comentarios NVARCHAR(MAX),
    filename NVARCHAR(255),
    FOREIGN KEY (users_id) REFERENCES users (id)
);
GO

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
    observaciones NVARCHAR(MAX),
    vigente NVARCHAR(10) DEFAULT 'Si',
    FOREIGN KEY (users_id) REFERENCES users (id)
);
GO

-- Insertar datos
""")
        
        # Exportar datos de cada tabla importante (excluyendo tablas no relevantes)
        tables_to_export = [
            'users', 'Pacientes', 'sintomas', 'eventos', 
            'planes_de_cuidados', 'somatometria', 'documentos', 'prescripciones'
        ]
        
        for table in tables_to_export:
            try:
                cursor.execute(f"SELECT * FROM {table}")
                rows = cursor.fetchall()
                
                if rows:
                    f.write(f"\n-- Datos de tabla {table}\n")
                    
                    # Obtener nombres de columnas
                    columns = [description[0] for description in cursor.description]
                    
                    for row in rows:
                        values = []
                        for value in row:
                            if value is None:
                                values.append('NULL')
                            elif isinstance(value, str):
                                # Escapar comillas simples y caracteres especiales
                                escaped_value = value.replace("'", "''").replace('\n', '\\n').replace('\r', '\\r')
                                values.append(f"N'{escaped_value}'")
                            else:
                                values.append(str(value))
                        
                        # Para users, usar SET IDENTITY_INSERT
                        if table == 'users':
                            columns_str = ', '.join(columns)
                            values_str = ', '.join(values)
                            f.write(f"SET IDENTITY_INSERT {table} ON;\n")
                            f.write(f"INSERT INTO {table} ({columns_str}) VALUES ({values_str});\n")
                            f.write(f"SET IDENTITY_INSERT {table} OFF;\n")
                        
                        elif table == 'Pacientes':
                            # Para Pacientes, usar todas las columnas
                            columns_str = ', '.join(columns)
                            values_str = ', '.join(values)
                            f.write(f"INSERT INTO {table} ({columns_str}) VALUES ({values_str});\n")
                        
                        else:
                            # Para otras tablas con IDENTITY, excluir la columna id
                            columns_no_id = [col for col in columns if col != 'id']
                            values_no_id = [val for i, val in enumerate(values) if columns[i] != 'id']
                            
                            if columns_no_id:
                                columns_str_no_id = ', '.join(columns_no_id)
                                values_str_no_id = ', '.join(values_no_id)
                                f.write(f"INSERT INTO {table} ({columns_str_no_id}) VALUES ({values_str_no_id});\n")
                    
                    f.write(f"-- Fin datos {table}\n\n")
                else:
                    f.write(f"-- No hay datos en tabla {table}\n\n")
                    
            except sqlite3.Error as e:
                f.write(f"-- Error al exportar tabla {table}: {e}\n\n")
        
        f.write("\nGO\n-- Migración completada")
    
    conn.close()
    print(f"Exportación corregida completada. Archivo generado: {output_file}")
    return output_file

if __name__ == "__main__":
    export_sqlite_to_sql_correct()