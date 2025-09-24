import os
import sqlite3
import pyodbc
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
from contextlib import contextmanager

from helpers import apology, login_required, mxn, valida

# Configure application
app = Flask(__name__)

# Configuración para producción
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')

# Configuración de base de datos
class DatabaseConfig:
    SQL_SERVER_CONFIG = {
        'server': r'LENOVO-MDP\SQLEXPRESS',
        'database': 'Jomquer',
        'driver': '{ODBC Driver 17 for SQL Server}',
        'trusted_connection': 'yes'
    }
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
    """Context manager para conexiones de base de datos con fallback a SQLite"""
    conn = None
    is_sql_server = False
    try:
        # Intentar conectar a SQL Server primero
        connection_string = get_sql_server_connection_string()
        conn = pyodbc.connect(connection_string)
        is_sql_server = True
        yield conn, is_sql_server
    except Exception as sql_error:
        print(f"Error conectando a SQL Server: {sql_error}")
        print("Usando SQLite como fallback...")
        
        # Fallback a SQLite
        try:
            conn = sqlite3.connect(DatabaseConfig.SQLITE_PATH)
            conn.row_factory = sqlite3.Row
            is_sql_server = False
            yield conn, is_sql_server
        except Exception as sqlite_error:
            print(f"Error conectando a SQLite: {sqlite_error}")
            raise
    finally:
        if conn:
            conn.close()

def execute_query(query, params=None, fetch_one=False, fetch_all=False):
    """Ejecuta una consulta adaptando la sintaxis según la base de datos"""
    with get_db_connection() as (conn, is_sql_server):
        cursor = conn.cursor()
        
        # Adaptar consulta para SQL Server vs SQLite
        if is_sql_server:
            # Convertir ? a ? (ya están bien para SQL Server con pyodbc)
            adapted_query = query
        else:
            adapted_query = query
            
        cursor.execute(adapted_query, params or ())
        
        if fetch_one:
            result = cursor.fetchone()
            return dict(result) if result and not is_sql_server else result
        elif fetch_all:
            results = cursor.fetchall()
            if not is_sql_server:
                return [dict(row) for row in results]
            else:
                # Para SQL Server, convertir a diccionario
                columns = [column[0] for column in cursor.description]
                return [dict(zip(columns, row)) for row in results]
        else:
            if not query.strip().upper().startswith('SELECT'):
                conn.commit()
            return cursor.rowcount

def obtener_planes_de_cuidados(paciente_id):
    return execute_query(
        "SELECT * FROM planes_de_cuidados WHERE users_id = ? AND status != 'Cancelado' ORDER BY fecha DESC",
        (paciente_id,), fetch_all=True
    )

def init_database():
    """Inicializar base de datos si no existe"""
    try:
        with get_db_connection() as (conn, is_sql_server):
            cursor = conn.cursor()
            
            if is_sql_server:
                print("Usando SQL Server - asumiendo que las tablas ya existen")
                # Para SQL Server, asumimos que las tablas ya están creadas
                # mediante el script de migración
            else:
                print("Inicializando SQLite...")
                # Código de inicialización SQLite existente
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        hash TEXT NOT NULL,
                        rol TEXT NOT NULL
                    )
                ''')
                
                # Resto de las tablas SQLite...
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS Pacientes (
                        usersId INTEGER PRIMARY KEY,
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
                        Domicilio NVARCHAR(500),
                        eMailPaciente NVARCHAR(255),
                        TelefonoPaciente NVARCHAR(20),
                        WhatsAppPaciente NVARCHAR(20),
                        PacienteActivo INTEGER DEFAULT 1,
                        FechaUltimoMovimiento NVARCHAR(50),
                        FOREIGN KEY (usersId) REFERENCES users (id)
                    )
                ''')
                
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS planes_de_cuidados (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        users_id INTEGER,
                        fecha TEXT,
                        acciones TEXT,
                        detecciones TEXT,
                        estado_mental TEXT,
                        riesgo_caidas TEXT,
                        riesgo_ulceras TEXT,
                        riesgo_pie_diabetico TEXT,
                        heridas TEXT,
                        estomas TEXT,
                        aseo TEXT,
                        medidas_posturales TEXT,
                        balance_liquidos TEXT,
                        dispositivos TEXT,
                        cuidados_via_aerea TEXT,
                        comentarios TEXT,
                        status TEXT DEFAULT 'Activo',
                        FOREIGN KEY (users_id) REFERENCES users (id)
                    )
                ''')
                
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS sintomas (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        date TEXT,
                        users_id INTEGER,
                        tipo TEXT,
                        descripcion TEXT,
                        FOREIGN KEY (users_id) REFERENCES users (id)
                    )
                ''')
                
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS eventos (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        date TEXT,
                        users_id INTEGER,
                        tipo INTEGER,
                        evento TEXT,
                        type INTEGER,
                        FOREIGN KEY (users_id) REFERENCES users (id)
                    )
                ''')
                
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS somatometria (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        users_id INTEGER,
                        fecha TEXT,
                        peso REAL,
                        talla REAL,
                        circ_abdominal REAL,
                        temp REAL,
                        sistolica INTEGER,
                        diastolica INTEGER,
                        fcard INTEGER,
                        fresp INTEGER,
                        o2 REAL,
                        glucemia REAL,
                        registrado_por INTEGER,
                        FOREIGN KEY (users_id) REFERENCES users (id),
                        FOREIGN KEY (registrado_por) REFERENCES users (id)
                    )
                ''')
                
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS documentos (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        users_id INTEGER,
                        fecha TEXT,
                        tema TEXT,
                        tipo TEXT,
                        comentarios TEXT,
                        filename TEXT,
                        FOREIGN KEY (users_id) REFERENCES users (id)
                    )
                ''')
                
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS prescripciones (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        users_id INTEGER,
                        medicamento TEXT,
                        dosis TEXT,
                        cantidad TEXT,
                        via TEXT,
                        cada_cantidad TEXT,
                        cada_unidad TEXT,
                        unidad_medida TEXT,
                        desde TEXT,
                        durante_cantidad TEXT,
                        durante_unidad TEXT,
                        vigente TEXT DEFAULT 'Si',
                        FOREIGN KEY (users_id) REFERENCES users (id)
                    )
                ''')
                
                conn.commit()
            
            print("Base de datos inicializada correctamente")
            
    except Exception as e:
        print(f"Error al inicializar base de datos: {e}")

# Custom filter
app.jinja_env.filters["mxn"] = mxn

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

app.config["UPLOAD_FOLDER"] = os.path.join("static", "uploads")
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# Inicializar base de datos al arrancar la aplicación
init_database()

@app.context_processor
def inject_username():
    if "user_id" in session:
        user = execute_query("SELECT username FROM users WHERE id = ?", (session["user_id"],), fetch_one=True)
        if user:
            return {"username": user["username"]}
    return {}

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    if session.get("rol") == "enfermeria" and not session.get("paciente_id"):
        return redirect(url_for("seleccionar_paciente"))
    
    user = execute_query("SELECT * FROM users WHERE id = ?", (session["user_id"],), fetch_one=True)
    rol = session.get("rol", "").lower()
    paciente = None
    planes_de_cuidados = []
    sintomas = []
    eventos = []
    somatometria = []
    autorizaciones = []
    documentos = []
    prescripciones = []
    somatometria_registros = []
 
    if user["rol"] == "supervisor":
        # Mostrar todos los planes de cuidados pendientes
        planes = execute_query("""
            SELECT p.*, pa.NombreCompleto
            FROM planes_de_cuidados p
            JOIN Pacientes pa ON p.users_id = pa.usersId
            WHERE p.status = 'Pendiente de revisión'
            ORDER BY p.fecha DESC
        """, fetch_all=True)
        
        selected_id = request.form.get("expediente_paciente_id")
        if selected_id:
            paciente = execute_query("SELECT * FROM Pacientes WHERE usersId = ?", (selected_id,), fetch_one=True)
            sintomas = execute_query("SELECT * FROM sintomas WHERE users_id = ? ORDER BY date DESC", (selected_id,), fetch_all=True)
            eventos = execute_query("SELECT * FROM eventos WHERE users_id = ? ORDER BY date DESC", (selected_id,), fetch_all=True)
            somatometria = execute_query("SELECT * FROM somatometria WHERE users_id = ? ORDER BY fecha DESC", (selected_id,), fetch_all=True)
            documentos = execute_query("SELECT * FROM documentos WHERE users_id = ? ORDER BY fecha DESC", (selected_id,), fetch_all=True)
            prescripciones = execute_query("SELECT * FROM prescripciones WHERE users_id = ? AND vigente != 'No' ORDER BY desde DESC", (selected_id,), fetch_all=True)
            autorizaciones = execute_query("SELECT * FROM eventos WHERE users_id = ? AND tipo = 2 ORDER BY date DESC", (selected_id,), fetch_all=True)
        
        somatometria_registros = somatometria
        
        return render_template(
            "index.html",
            username=user["username"],
            rol=user["rol"],
            paciente=paciente,
            plan_de_cuidados=planes,
            ultimo_plan=planes[0] if planes else None,
            sintomas=sintomas,
            eventos=eventos,
            documentos=documentos,
            autorizaciones=autorizaciones,
            somatometria=somatometria_registros,
            prescripciones=prescripciones,
        )

    elif user["rol"] == "enfermeria" and session.get("paciente_id"):
        paciente_id = session["paciente_id"]
        planes_de_cuidados = execute_query(
            "SELECT * FROM planes_de_cuidados WHERE users_id = ? AND status != 'Baja' ORDER BY fecha DESC",
            (paciente_id,), fetch_all=True
        )
        sintomas = execute_query("SELECT * FROM sintomas WHERE users_id = ?", (paciente_id,), fetch_all=True)
        eventos = execute_query("SELECT * FROM eventos WHERE users_id = ?", (paciente_id,), fetch_all=True)
        somatometria = execute_query("SELECT * FROM somatometria WHERE users_id = ?", (paciente_id,), fetch_all=True)
        autorizaciones = execute_query("SELECT * FROM eventos WHERE users_id = ? AND tipo = 2", (paciente_id,), fetch_all=True)
        documentos = execute_query("SELECT * FROM documentos WHERE users_id = ?", (paciente_id,), fetch_all=True)
        prescripciones = execute_query("SELECT * FROM prescripciones WHERE users_id = ?", (paciente_id,), fetch_all=True)
        paciente = execute_query("SELECT * FROM Pacientes WHERE usersId = ?", (paciente_id,), fetch_one=True)
        somatometria_registros = somatometria
        
        return render_template(
            "index.html",
            username=user["username"],
            rol=user["rol"],
            paciente=paciente,
            plan_de_cuidados=planes_de_cuidados,
            ultimo_plan=planes_de_cuidados[0] if planes_de_cuidados else None,
            sintomas=sintomas,
            eventos=eventos,
            documentos=documentos,
            autorizaciones=autorizaciones,
            somatometria=somatometria_registros,
            prescripciones=prescripciones
        )

    else:
        paciente = execute_query("SELECT * FROM Pacientes WHERE usersId = ?", (session["user_id"],), fetch_one=True)
        planes_de_cuidados = execute_query("SELECT * FROM planes_de_cuidados WHERE users_id = ?", (session["user_id"],), fetch_all=True)
        sintomas = execute_query("SELECT * FROM sintomas WHERE users_id = ? ORDER BY date DESC", (session["user_id"],), fetch_all=True)
        eventos = execute_query("SELECT * FROM eventos WHERE users_id = ?", (session["user_id"],), fetch_all=True)
        somatometria = execute_query("SELECT * FROM somatometria WHERE users_id = ? ORDER BY fecha DESC", (session["user_id"],), fetch_all=True)
        autorizaciones = execute_query("SELECT * FROM eventos WHERE users_id = ? AND tipo = 2 ORDER BY date DESC", (session["user_id"],), fetch_all=True)
        documentos = execute_query("SELECT * FROM documentos WHERE users_id = ? ORDER BY fecha DESC", (session["user_id"],), fetch_all=True)
        prescripciones = execute_query("SELECT * FROM prescripciones WHERE users_id = ? and vigente !='No' ORDER BY desde DESC", (session["user_id"],), fetch_all=True)
        somatometria_registros = somatometria

        # Ordenamiento seguro (las listas ya vienen como diccionarios)
        if planes_de_cuidados:
            planes_de_cuidados = sorted(planes_de_cuidados, key=lambda r: r['fecha'], reverse=True)
        if sintomas:
            sintomas = sorted(sintomas, key=lambda s: s['date'], reverse=True)
        if somatometria:
            somatometria = sorted(somatometria, key=lambda s: s['fecha'], reverse=True)
        if eventos:
            eventos = sorted(eventos, key=lambda e: e['date'], reverse=True)
        if autorizaciones:
            autorizaciones = sorted(autorizaciones, key=lambda a: a['date'], reverse=True)
        if documentos:
            documentos = sorted(documentos, key=lambda d: d['fecha'], reverse=True)
        if prescripciones:
            prescripciones = sorted(prescripciones, key=lambda p: p['desde'], reverse=True)

    # Render final
    return render_template(
        "index.html",
        username=user["username"],
        rol=rol,
        paciente=paciente,
        plan_de_cuidados=planes_de_cuidados,
        ultimo_plan=planes_de_cuidados[0] if planes_de_cuidados else None,
        sintomas=sintomas,
        eventos=eventos,
        somatometria=somatometria_registros,
        autorizaciones=autorizaciones,
        documentos=documentos,
        prescripciones=prescripciones
    )

@app.route("/datospersonales", methods=["GET", "POST"])
@login_required
def datospersonales():
    paciente = execute_query("SELECT * FROM Pacientes WHERE usersId = ?", (session["user_id"],), fetch_one=True)

    if request.method == "POST":
        nombre = request.form.get("Nombre")
        primer_apellido = request.form.get("PrimerApellido")
        segundo_apellido = request.form.get("SegundoApellido")
        nombre_completo = f"{nombre} {primer_apellido} {segundo_apellido}".strip()
        curp = request.form.get("CURP")
        entidad_de_nacimiento = curp[11:13] if curp and len(curp) >= 13 else None

        # Si ya existe, actualiza
        if paciente:
            execute_query(
                """UPDATE Pacientes SET
                    NombreCompleto = ?, Nombre = ?, PrimerApellido = ?, SegundoApellido = ?, FechaNacimiento = ?,
                    EntidadDeNacimiento = ?, SexoBiologico = ?, Genero = ?, CURP = ?, Domicilio = ?, eMailPaciente = ?,
                    TelefonoPaciente = ?, WhatsAppPaciente = ?
                WHERE usersId = ?""",
                (
                    nombre_completo, nombre, primer_apellido, segundo_apellido, request.form.get("FechaNacimiento"),
                    entidad_de_nacimiento, request.form.get("SexoBiologico"), request.form.get("Genero"), curp,
                    request.form.get("Domicilio"), request.form.get("eMailPaciente"),
                    request.form.get("TelefonoPaciente"), request.form.get("WhatsAppPaciente"),
                    session["user_id"]
                )
            )
        # Si no existe, inserta
        else:
            execute_query(
                """INSERT INTO Pacientes (
                    usersId, NombreCompleto, Nombre, PrimerApellido, SegundoApellido, FechaNacimiento,
                    EntidadDeNacimiento, SexoBiologico, Genero, CURP, Domicilio, eMailPaciente,
                    TelefonoPaciente, WhatsAppPaciente, PacienteActivo, FechaUltimoMovimiento
                ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (
                    session["user_id"], nombre_completo, nombre, primer_apellido, segundo_apellido,
                    request.form.get("FechaNacimiento"), entidad_de_nacimiento, request.form.get("SexoBiologico"),
                    request.form.get("Genero"), curp, request.form.get("Domicilio"),
                    request.form.get("eMailPaciente"), request.form.get("TelefonoPaciente"),
                    request.form.get("WhatsAppPaciente"), 1, datetime.now().strftime("%Y-%m-%dT%H:%M")
                )
            )
        return redirect("/")

    # GET: mostrar formulario con datos si existen
    datos = dict(paciente) if paciente else {}
    return render_template("datospersonales.html", datos=datos)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = execute_query("SELECT * FROM users WHERE username = ?", (username,), fetch_one=True)
        
        if user and check_password_hash(user["hash"], password):
            session["user_id"] = user["id"]
            session["rol"] = user["rol"]
            return redirect(url_for("index"))
        else:
            flash("Usuario o contraseña incorrectos", "danger")
    return render_template("login.html")

# Resto de las rutas seguirían el mismo patrón...
# Por brevedad, incluyo solo las más importantes

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/init-database")
def init_database_route():
    """Ruta para inicializar la base de datos manualmente"""
    try:
        init_database()
        return "Base de datos inicializada correctamente", 200
    except Exception as e:
        return f"Error al inicializar base de datos: {str(e)}", 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)