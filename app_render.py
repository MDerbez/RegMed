import os
import sqlite3
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime

from helpers import apology, login_required, mxn, valida

# Configure application
app = Flask(__name__)

# Configuración para producción
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')

# Detectar entorno (Render vs Local)
IS_RENDER = os.environ.get('RENDER') is not None
USE_SQL_SERVER = os.environ.get('USE_SQL_SERVER', 'false').lower() == 'true'

def get_db_connection():
    """Obtiene conexión según el entorno"""
    if USE_SQL_SERVER and not IS_RENDER:
        # SQL Server local
        import pyodbc
        try:
            connection_string = (
                "DRIVER={ODBC Driver 17 for SQL Server};"
                "SERVER=LENOVO-MDP\\SQLEXPRESS;"
                "DATABASE=Jomquer;"
                "Trusted_Connection=yes"
            )
            conn = pyodbc.connect(connection_string)
            print("🔗 Conectado a SQL Server local")
            return conn, True
        except Exception as e:
            print(f"❌ Error SQL Server: {e}")
            print("🔄 Usando SQLite como fallback...")
    
    # SQLite (default para Render y fallback)
    db_path = os.path.join(os.path.dirname(__file__), "pacientes.db")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    print("🔗 Conectado a SQLite")
    return conn, False

def execute_query(query, params=None, fetch_one=False, fetch_all=False):
    """Ejecuta consultas adaptando sintaxis"""
    conn, is_sql_server = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(query, params or ())
        
        if fetch_one:
            result = cursor.fetchone()
            if result and not is_sql_server:
                return dict(result)
            elif result and is_sql_server:
                columns = [column[0] for column in cursor.description]
                return dict(zip(columns, result))
            return result
        
        elif fetch_all:
            results = cursor.fetchall()
            if not is_sql_server:
                return [dict(row) for row in results]
            else:
                columns = [column[0] for column in cursor.description]
                return [dict(zip(columns, row)) for row in results]
        
        else:
            if not query.strip().upper().startswith('SELECT'):
                conn.commit()
            return cursor.rowcount
    finally:
        conn.close()

def init_database():
    """Inicializar base de datos según entorno"""
    if IS_RENDER:
        print("🌐 Inicializando en Render (SQLite)")
        # Código de inicialización SQLite
        conn, _ = get_db_connection()
        cursor = conn.cursor()
        
        # Crear tabla users
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                hash TEXT NOT NULL,
                rol TEXT NOT NULL
            )
        ''')
        
        # Crear tabla Pacientes con estructura completa
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Pacientes (
                usersId INTEGER PRIMARY KEY,
                Usuario TEXT,
                Contrasena TEXT,
                NombreCompleto TEXT,
                Expediente TEXT,
                Nombre TEXT,
                PrimerApellido TEXT,
                SegundoApellido TEXT,
                FechaNacimiento TEXT,
                EntidadDeNacimiento TEXT,
                SexoCURP INTEGER,
                SexoBiologico INTEGER,
                Genero TEXT,
                CURP TEXT,
                EstadoMental TEXT,
                GrupoRH TEXT,
                DiagnosticoPrimario TEXT,
                CIEPrimario TEXT,
                SegundoDiagnostico TEXT,
                SegundoCIE TEXT,
                TercerDiagnostico TEXT,
                TercerCIE TEXT,
                Domicilio TEXT,
                eMailPaciente TEXT,
                TelefonoPaciente TEXT,
                WhatsAppPaciente TEXT,
                NombreContactoTutor TEXT,
                ParentescoContactoTutor TEXT,
                TelefonoContactoTutor TEXT,
                WhatsAppContactoTutor TEXT,
                PrimerContacto INTEGER,
                PacienteActivo INTEGER DEFAULT 1,
                FechaUltimoMovimiento TEXT,
                Alergico INTEGER DEFAULT 0,
                RiesgoCaidas INTEGER DEFAULT 0,
                RiesgoUlceras INTEGER DEFAULT 0,
                FOREIGN KEY (usersId) REFERENCES users (id)
            )
        ''')
        
        # Crear otras tablas...
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS planes_de_cuidados (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                users_id INTEGER,
                fecha TEXT,
                riesgo_caidas TEXT,
                estado_mental TEXT,
                riesgo_ulceras TEXT,
                riesgo_pie_diabetico TEXT,
                heridas TEXT,
                estomas TEXT,
                aseo TEXT,
                medidas_posturales TEXT,
                balance_liquidos TEXT,
                dispositivos TEXT,
                cuidados_via_aerea TEXT,
                status TEXT DEFAULT 'Activo',
                comentarios TEXT,
                dieta TEXT,
                rehabilitacion TEXT,
                alergico TEXT,
                detecciones TEXT,
                acciones TEXT,
                FOREIGN KEY (users_id) REFERENCES users (id)
            )
        ''')
        
        # Agregar más tablas según necesites...
        conn.commit()
        conn.close()
        print("✅ Base de datos SQLite inicializada")
    
    elif USE_SQL_SERVER:
        print("🖥️ Usando SQL Server local - tablas deben existir")
    else:
        print("🔧 Entorno de desarrollo - inicializando SQLite")
        # Mismo código que Render
        conn, _ = get_db_connection()
        # ... código de inicialización ...
        conn.close()

# Custom filter
app.jinja_env.filters["mxn"] = mxn

# Configure session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

app.config["UPLOAD_FOLDER"] = os.path.join("static", "uploads")
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# Inicializar base de datos
init_database()

# Resto de tu aplicación (rutas, etc.) sigue igual...
@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    if session.get("rol") == "enfermeria" and not session.get("paciente_id"):
        return redirect(url_for("seleccionar_paciente"))
    
    user = execute_query("SELECT * FROM users WHERE id = ?", (session["user_id"],), fetch_one=True)
    # ... resto del código igual ...
    return render_template("index.html")

# ... resto de rutas ...

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug_mode = not IS_RENDER  # Debug solo en local
    app.run(host='0.0.0.0', port=port, debug=debug_mode)