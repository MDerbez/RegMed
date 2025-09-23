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
def obtener_planes_de_cuidados(paciente_id):
    conn = get_db_connection()
    return conn.execute(
        "SELECT * FROM planes_de_cuidados WHERE users_id = ? AND status != 'Cancelado' ORDER BY fecha DESC",
        (paciente_id,)
    ).fetchall()

def get_db_connection():
    # Usar la base de datos correcta
    db_path = os.path.join(os.path.dirname(__file__), "pacientes.db")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    """Inicializar base de datos SQLite si no existe"""
    db_path = os.path.join(os.path.dirname(__file__), "pacientes.db")
    
    # Si la base de datos no existe, crearla con las tablas básicas
    if not os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
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
        
        # Crear tabla pacientes
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Pacientes (
                UsersId INTEGER PRIMARY KEY,
                NombreCompleto TEXT,
                Nombre TEXT,
                PrimerApellido TEXT,
                SegundoApellido TEXT,
                FechaNacimiento TEXT,
                EntidadDeNacimiento TEXT,
                SexoBiologico TEXT,
                Genero TEXT,
                CURP TEXT,
                Domicilio TEXT,
                eMailPaciente TEXT,
                TelefonoPaciente TEXT,
                WhatsAppPaciente TEXT,
                PacienteActivo INTEGER DEFAULT 1,
                FechaUltimoMovimiento TEXT,
                FOREIGN KEY (UsersId) REFERENCES users (id)
            )
        ''')
        
        # Crear otras tablas necesarias
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
        conn.close()
        print("Base de datos inicializada correctamente")
    else:
        print("La base de datos ya existe")

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
        conn = get_db_connection()
        user = conn.execute("SELECT username FROM users WHERE id = ?", (session["user_id"],)).fetchone()
        conn.close()
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
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE id = ?", (session["user_id"],)).fetchone()
    rol = session.get("rol", "").lower()
    paciente = None
    planes_de_cuidados = []
    sintomas = []
    eventos = []
    somatometria = []
    autorizaciones = []
    documentos = []
    prescripciones = []
    somatometria_registros = []  # ← Inicializar aquí
 
    if user["rol"] == "supervisor":
        # Mostrar todos los planes de cuidados pendientes
        planes = conn.execute("""
            SELECT p.*, pa.NombreCompleto
            FROM planes_de_cuidados p
            JOIN Pacientes pa ON p.users_id = pa.usersId
            WHERE p.status = 'Pendiente de revisión'
            ORDER BY p.fecha DESC
        """).fetchall()
        selected_id = request.form.get("expediente_paciente_id")
        if selected_id:
            paciente = conn.execute("SELECT * FROM Pacientes WHERE usersId = ?", (selected_id,)).fetchone()
            sintomas = conn.execute("SELECT * FROM sintomas WHERE users_id = ? ORDER BY date DESC", (selected_id,)).fetchall()
            eventos = conn.execute("SELECT * FROM eventos WHERE users_id = ? ORDER BY date DESC", (selected_id,)).fetchall()
            somatometria = conn.execute("SELECT * FROM somatometria WHERE users_id = ? ORDER BY fecha DESC", (selected_id,)).fetchall()
            documentos = conn.execute("SELECT * FROM documentos WHERE users_id = ? ORDER BY fecha DESC", (selected_id,)).fetchall()
            prescripciones = conn.execute("SELECT * FROM prescripciones WHERE users_id = ? AND vigente != 'No' ORDER BY desde DESC", (selected_id,)).fetchall()
            autorizaciones = conn.execute("SELECT * FROM eventos WHERE users_id = ? AND tipo = 2 ORDER BY date DESC",(selected_id,)).fetchall()
        somatometria_registros = somatometria
        conn.close()
        return render_template(
            "index.html",
            username=user["username"],
            rol=user["rol"],
            paciente=paciente,
            plan_de_cuidados=planes,  # ← CORREGIDO
            ultimo_plan=planes[0] if planes else None,  # ← CORREGIDO
            sintomas=sintomas,
            eventos=eventos,
            documentos=documentos,
            autorizaciones=autorizaciones,
            somatometria=somatometria_registros,
            prescripciones=prescripciones,
            )

    elif user["rol"] == "enfermeria" and session.get("paciente_id"):
        paciente_id = session["paciente_id"]
        planes_de_cuidados = conn.execute(
            "SELECT * FROM planes_de_cuidados WHERE users_id = ? AND status != 'Baja' ORDER BY fecha DESC",
            (paciente_id,)
        ).fetchall()
        sintomas = conn.execute("SELECT * FROM sintomas WHERE users_id = ?", (paciente_id,)).fetchall()
        eventos = conn.execute("SELECT * FROM eventos WHERE users_id = ?", (paciente_id,)).fetchall()
        somatometria = conn.execute("SELECT * FROM somatometria WHERE users_id = ?", (paciente_id,)).fetchall()
        autorizaciones = conn.execute("SELECT * FROM eventos WHERE users_id = ? AND tipo = 2", (paciente_id,)).fetchall()
        documentos = conn.execute("SELECT * FROM documentos WHERE users_id = ?", (paciente_id,)).fetchall()
        prescripciones = conn.execute("SELECT * FROM prescripciones WHERE users_id = ?", (paciente_id,)).fetchall()
        paciente = conn.execute("SELECT * FROM Pacientes WHERE usersId = ?", (paciente_id,)).fetchone()
        somatometria_registros = somatometria
        conn.close()
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
        paciente = conn.execute("SELECT * FROM Pacientes WHERE usersId = ?", (session["user_id"],)).fetchone()
        planes_de_cuidados = conn.execute("SELECT * FROM planes_de_cuidados WHERE users_id = ?", (session["user_id"],)).fetchall()
        sintomas = conn.execute("SELECT * FROM sintomas WHERE users_id = ? ORDER BY date DESC", (session["user_id"],)).fetchall()
        eventos = conn.execute("SELECT * FROM eventos WHERE users_id = ?", (session["user_id"],)).fetchall()
        somatometria = conn.execute("SELECT * FROM somatometria WHERE users_id = ? ORDER BY fecha DESC", (session["user_id"],)).fetchall()
        autorizaciones = conn.execute("SELECT * FROM eventos WHERE users_id = ? AND tipo = 2 ORDER BY date DESC", (session["user_id"],)).fetchall()
        documentos = conn.execute("SELECT * FROM documentos WHERE users_id = ? ORDER BY fecha DESC", (session["user_id"],)).fetchall()
        prescripciones = conn.execute("SELECT * FROM prescripciones WHERE users_id = ? and vigente !='No' ORDER BY desde DESC", (session["user_id"],)).fetchall()
        somatometria_registros = somatometria
        conn.close()

        # Ordenamiento seguro
        planes_de_cuidados = sorted(planes_de_cuidados, key=lambda r: r['fecha'], reverse=True)
        sintomas = sorted(sintomas, key=lambda s: s['date'], reverse=True)
        somatometria = sorted(somatometria, key=lambda s: s['fecha'], reverse=True)
        eventos = sorted(eventos, key=lambda e: e['date'], reverse=True)
        autorizaciones = sorted(autorizaciones, key=lambda a: a['date'], reverse=True)
        documentos = sorted(documentos, key=lambda d: d['fecha'], reverse=True)
        prescripciones = sorted(prescripciones, key=lambda p: p['desde'], reverse=True)

    # Render final
    return render_template(
        "index.html",
        username=user["username"],
        rol=rol,
        paciente=paciente,
        plan_de_cuidados=planes_de_cuidados,  # ← CORREGIDO: usar planes_de_cuidados
        ultimo_plan=planes_de_cuidados[0] if planes_de_cuidados else None,  # ← CORREGIDO
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
    conn = get_db_connection()
    paciente = conn.execute(
        "SELECT * FROM Pacientes WHERE usersId = ?", (session["user_id"],)
    ).fetchone()

    if request.method == "POST":
        nombre = request.form.get("Nombre")
        primer_apellido = request.form.get("PrimerApellido")
        segundo_apellido = request.form.get("SegundoApellido")
        nombre_completo = f"{nombre} {primer_apellido} {segundo_apellido}".strip()
        curp = request.form.get("CURP")
        entidad_de_nacimiento = curp[11:13] if curp and len(curp) >= 13 else None

        # Si ya existe, actualiza
        if paciente:
            conn.execute(
                """UPDATE Pacientes SET
                    NombreCompleto = ?, Nombre = ?, PrimerApellido = ?, SegundoApellido = ?, FechaNacimiento = ?,
                    EntidadDeNacimiento = ?, SexoBiologico = ?, Genero = ?, CURP = ?, Domicilio = ?, eMailPaciente = ?,
                    TelefonoPaciente = ?, WhatsAppPaciente = ?
                WHERE UsersId = ?""",
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
            conn.execute(
                """INSERT INTO Pacientes (
                    UsersId, NombreCompleto, Nombre, PrimerApellido, SegundoApellido, FechaNacimiento,
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
        conn.commit()
        conn.close()
        return redirect("/")

    # GET: mostrar formulario con datos si existen
    datos = dict(paciente) if paciente else {}
    conn.close()
    return render_template("datospersonales.html", datos=datos)

@app.route("/autacceso", methods=["GET", "POST"])
@login_required
def autacceso():
    conn = get_db_connection()

    # POST: guardar autorización
    if request.method == "POST":
        correo = request.form.get("correo")
        if not correo:
            return apology("Debe ingresar un correo válido", 400)

        # Guardar en tabla eventos como tipo 2 (autorización)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS eventos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                users_id INTEGER NOT NULL,
                tipo INTEGER NOT NULL,
                evento TEXT NOT NULL,
                type INTEGER NOT NULL
            )
        """)
        conn.execute(
            "INSERT INTO eventos (date, users_id, tipo, evento, type) VALUES (?, ?, ?, ?, ?)",
            (datetime.now(), session["user_id"], 2, f"Autorización para {correo}", 0)
        )
        conn.commit()
        return redirect("/autacceso")  # redirige al mismo formulario para mostrar lista

    # GET: mostrar formulario y lista de autorizaciones
    autorizaciones = conn.execute(
        "SELECT * FROM eventos WHERE users_id = ? AND tipo = 2",
        (session["user_id"],)
    ).fetchall()
    conn.close()

    autorizaciones = [dict(row) for row in autorizaciones]
    return render_template("autacceso.html", autorizaciones=autorizaciones)

@app.route("/editar_ultimo_enfermeria", methods=["POST"])
@login_required
def editar_ultimo_enfermeria():
    plan_id = request.form.get("plan_id")
    acciones = request.form.get("acciones")
    detecciones = request.form.get("detecciones")
    estado_mental = request.form.get("estado_mental")
    riesgo_caidas = request.form.get("riesgo_caidas")
    riesgo_ulceras = request.form.get("riesgo_ulceras")
    riesgo_pie_diabetico = request.form.get("riesgo_pie_diabetico")
    heridas = request.form.get("heridas")
    estomas = request.form.get("estomas")
    aseo = request.form.get("aseo")
    medidas_posturales = request.form.get("medidas_posturales")
    balance_liquidos = request.form.get("balance_liquidos")
    dispositivos = request.form.get("dispositivos")
    cuidados_via_aerea = request.form.get("cuidados_via_aerea")
    comentario_nuevo = request.form.get("comentario_nuevo")
    conn = get_db_connection()
    conn.execute("""
        UPDATE planes_de_cuidados SET
            acciones = ?,
            detecciones = ?,
            estado_mental = ?,
            riesgo_caidas = ?,
            riesgo_ulceras = ?,
            riesgo_pie_diabetico = ?,
            heridas = ?,
            estomas = ?,
            aseo = ?,
            medidas_posturales = ?,
            balance_liquidos = ?,
            dispositivos = ?,
            cuidados_via_aerea = ?,
            comentarios = COALESCE(comentarios, '') || '\n' || ?
        WHERE id = ?
    """, (
        acciones, detecciones, estado_mental, riesgo_caidas, riesgo_ulceras,
        riesgo_pie_diabetico, heridas, estomas, aseo, medidas_posturales,
        balance_liquidos, dispositivos, cuidados_via_aerea, comentario_nuevo, plan_id
    ))
    conn.commit()
    conn.close()
    return redirect("/")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        conn.close()
        if user and check_password_hash(user["hash"], password):
            session["user_id"] = user["id"]
            session["rol"] = user["rol"]
            return redirect(url_for("index"))
        else:
            flash("Usuario o contraseña incorrectos", "danger")
    return render_template("login.html")

@app.route("/password", methods=["GET", "POST"])
@login_required
def password():
    if request.method == "POST":
        old_password = request.form.get("old_password")
        new_password = request.form.get("new_password")
        confirm_password = request.form.get("confirm_password")
        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE id = ?", (session["user_id"],)).fetchone()
        if not user or not check_password_hash(user["hash"], old_password):
            flash("La contraseña actual es incorrecta.", "danger")
        elif new_password != confirm_password:
            flash("Las contraseñas nuevas no coinciden.", "danger")
        else:
            conn.execute("UPDATE users SET hash = ? WHERE id = ?", (generate_password_hash(new_password), session["user_id"]))
            conn.commit()
            flash("Contraseña actualizada correctamente.", "success")
        conn.close()
    return render_template("password.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        rol = request.form.get("rol")
        # Solo crea el usuario
        conn = get_db_connection()
        conn.execute("INSERT INTO users (username, hash, rol) VALUES (?, ?, ?)", (username, generate_password_hash(password), rol))
        user_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
        conn.commit()
        conn.close()
        # Login automático y redirección
        session["user_id"] = user_id
        session["rol"] = rol
        if rol == "paciente":
            return redirect(url_for("datospersonales"))
        else:
            flash("Cuenta creada correctamente.", "success")
            return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/registro_enfermeria", methods=["GET", "POST"])
@login_required
def registro_enfermeria():
    if session.get("rol") == "enfermeria" and not session.get("paciente_id"):
        return redirect(url_for("seleccionar_paciente"))
    paciente_id = session.get("paciente_id")
    rol = session.get("rol")  # ← agrega esto
    if not paciente_id:
        return redirect(url_for("seleccionar_paciente"))
    conn = get_db_connection()
    if request.method == "POST":
        # Recoge los datos del formulario
        acciones = request.form.get("acciones")
        detecciones = request.form.get("detecciones")
        estado_mental = request.form.get("estado_mental")
        riesgo_caidas = request.form.get("riesgo_caidas")
        riesgo_ulceras = request.form.get("riesgo_ulceras")
        riesgo_pie_diabetico = request.form.get("riesgo_pie_diabetico")
        heridas = request.form.get("heridas")
        estomas = request.form.get("estomas")
        aseo = request.form.get("aseo")
        medidas_posturales = request.form.get("medidas_posturales")
        balance_liquidos = request.form.get("balance_liquidos")
        dispositivos = request.form.get("dispositivos")
        cuidados_via_aerea = request.form.get("cuidados_via_aerea")
        comentarios = request.form.get("comentarios")
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M")
        # Guarda el nuevo plan
        conn.execute("""
            INSERT INTO planes_de_cuidados (
                users_id, fecha, acciones, detecciones, estado_mental, riesgo_caidas, riesgo_ulceras,
                riesgo_pie_diabetico, heridas, estomas, aseo, medidas_posturales, balance_liquidos,
                dispositivos, cuidados_via_aerea, comentarios
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            paciente_id, fecha, acciones, detecciones, estado_mental, riesgo_caidas, riesgo_ulceras,
            riesgo_pie_diabetico, heridas, estomas, aseo, medidas_posturales, balance_liquidos,
            dispositivos, cuidados_via_aerea, comentarios
        ))
        conn.commit()
        conn.close()
        return redirect(url_for("index"))
    conn.close()
    return render_template("registro_enfermeria.html", paciente_id=paciente_id, rol=rol)

@app.route("/seleccionar_paciente", methods=["GET", "POST"])
@login_required
def seleccionar_paciente():
    conn = get_db_connection()
    pacientes = conn.execute("SELECT usersid, NombreCompleto FROM pacientes").fetchall()
    conn.close()
    if request.method == "POST":
        paciente_id = request.form.get("paciente_id")
        session["paciente_id"] = paciente_id
        return redirect(url_for("index"))
    return render_template("seleccionar_paciente.html", pacientes=pacientes)

@app.route("/sintomas", methods=["GET", "POST"])
@login_required
def sintomas():
    if session.get("rol") != "paciente":
        return apology("Acceso restringido", 403)
    conn = get_db_connection()
    if request.method == "POST":
        tipo = request.form.get("tipo")
        descripcion = request.form.get("descripcion")
        conn.execute("INSERT INTO sintomas (date, users_id, tipo, descripcion) VALUES (?, ?, ?, ?)",
                     (datetime.now(), session["user_id"], tipo, descripcion))
        conn.commit()
    sintomas = conn.execute("SELECT * FROM sintomas WHERE users_id = ?", (session["user_id"],)).fetchall()
    conn.close()
    return render_template("sintomas.html", sintomas=sintomas)

@app.route("/evento", methods=["GET", "POST"])
@login_required
def evento():
    if session.get("rol") != "paciente":
        return apology("Acceso restringido", 403)
    conn = get_db_connection()
    if request.method == "POST":
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M")
        evento = request.form.get("evento")
        fecha = request.form.get("fecha")  # ← usa "fecha" como en tu input
        tipo = request.form.get("tipo")   # ← recoge el tipo del formulario
        type_value = 1 if tipo == "evento" else 2 if tipo == "autorizacion" else 0
        if not fecha:
            fecha = datetime.now().strftime('%Y-%m-%dT%H:%M')
        conn.execute("INSERT INTO eventos (users_id, evento, date, tipo, type) VALUES (?, ?, ?, ?, ?)",
                     (session["user_id"], evento, fecha, tipo, type_value))
        conn.commit()
    eventos = conn.execute("SELECT * FROM eventos WHERE users_id = ?", (session["user_id"],)).fetchall()
    conn.close()
    fecha_hoy = datetime.now().strftime('%Y-%m-%dT%H:%M')
    return render_template("evento.html", eventos=eventos, fecha_hoy=fecha_hoy)

@app.route("/somatometria", methods=["GET", "POST"])
@login_required
def somatometria():
    if session.get("rol") not in ["paciente", "enfermeria"]:
        return apology("Acceso restringido", 403)
    fecha_hoy = datetime.now().strftime('%Y-%m-%dT%H:%M')
    conn = get_db_connection()
    if session.get("rol") == "enfermeria":
        paciente_id = session.get("paciente_id")
    else:
        paciente_id = session["user_id"]
    if request.method == "POST":
        peso = request.form.get("peso")
        talla = request.form.get("talla")
        fecha = request.form.get("fecha")
        circ_abdominal = request.form.get("circ_abdominal")
        temp = request.form.get("temp")
        sistolica = request.form.get("sistolica")
        diastolica = request.form.get("diastolica")
        fcard = request.form.get("fcard")
        fresp = request.form.get("fresp")
        o2 = request.form.get("o2")
        glucemia = request.form.get("glucemia")
        try:
            imc = round(float(peso) / (float(talla) / 100) ** 2, 2) if peso and talla else None
        except Exception:
            imc = None
        conn.execute("""INSERT INTO somatometria 
            (users_id, fecha, peso, talla, circ_abdominal, temp, sistolica, diastolica, fcard, fresp, o2, glucemia, registrado_por) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (paciente_id, fecha, peso, talla, circ_abdominal, temp, sistolica, diastolica, fcard, fresp, o2, glucemia, session["user_id"]))
        conn.commit()
    registros = conn.execute("SELECT * FROM somatometria WHERE users_id = ?  ORDER BY fecha DESC", (session["user_id"],)).fetchall()
    conn.close()
    return render_template("somatometria.html", registros=registros, fecha_hoy=fecha_hoy)

@app.route("/documentos", methods=["GET", "POST"])
@login_required
def documentos():
    if session.get("rol") != "paciente":
        return apology("Acceso restringido", 403)
    conn = get_db_connection()
    if request.method == "POST":
        fecha = request.form.get("fecha")
        tipo = request.form.get("tipo")
        tema = request.form.get("tema")
        comentarios = request.form.get("comentarios")
        archivo = request.files.get("archivo")
        if archivo and tema and fecha and tipo:
            filename = secure_filename(archivo.filename)
            archivo.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            conn.execute(
                "INSERT INTO documentos (users_id, fecha, tema, tipo, comentarios, filename) VALUES (?, ?, ?, ?, ?, ?)",
                (session["user_id"], datetime.now().strftime("%Y-%m-%d %H:%M"), tema, tipo, comentarios, filename)
            )
            conn.commit()
        else:
            flash("Por favor, completa todos los campos requeridos.", "danger")
    documentos = conn.execute("SELECT * FROM documentos WHERE users_id = ?", (session["user_id"],)).fetchall()
    conn.close()
    return render_template("documentos.html", documentos=documentos)

@app.route("/prescripciones", methods=["GET", "POST"])
@login_required
def prescripciones():
    if session.get("rol") not in ["paciente", "enfermeria"]:
        return apology("Acceso restringido", 403)
    conn = get_db_connection()
    if request.method == "POST":
        if session.get("rol") == "enfermeria":
            usuario_id = session.get("paciente_id")
        else:
            usuario_id = session["user_id"]
        medicamento = request.form.get("medicamento")
        dosis = request.form.get("dosis")
        cantidad = request.form.get("cantidad")
        via = request.form.get("via")
        cada_cantidad = request.form.get("cada_cantidad")
        cada_unidad = request.form.get("cada_unidad")
        unidad_medida = request.form.get("unidad_medida")
        desde = request.form.get("desde")
        durante_cantidad = request.form.get("durante_cantidad")
        durante_unidad = request.form.get("durante_unidad")
        conn.execute(
            "INSERT INTO prescripciones (users_id, medicamento, dosis, cantidad, via, cada_cantidad, cada_unidad, unidad_medida, desde, durante_cantidad, durante_unidad, vigente) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (usuario_id, medicamento, dosis, cantidad, via, cada_cantidad, cada_unidad, unidad_medida, desde, durante_cantidad, durante_unidad, "Si")
        )
        conn.commit()
    prescripciones = conn.execute(
        "SELECT * FROM prescripciones WHERE users_id = ?", (session["user_id"],)
    ).fetchall()
    conn.close()
    return render_template("prescripciones.html", prescripciones=prescripciones, now=datetime.now())


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/validar_ultimo", methods=["POST"])
@login_required
def validar_ultimo():
    plan_id = request.form.get("ultimo_id")
    comentario = request.form.get("comentario")
    status = request.form.get("status")
    accion = request.form.get("accion")
    conn = get_db_connection()
    if accion == "cancelar":
        # Da de baja el plan (puedes cambiar el status o eliminar el registro)
        conn.execute("UPDATE planes_de_cuidados SET status = ? WHERE id = ?", ("Baja", plan_id))
        flash("El plan fue dado de baja.", "danger")
    else:
        conn.execute(
            "UPDATE planes_de_cuidados SET comentarios = COALESCE(comentarios, '') || '\n' || ?, status = ? WHERE id = ?",
            (comentario, status, plan_id)
        )
        flash("Cambios guardados correctamente.", "success")
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

def registrar_usuario(username, password, rol, nombre_completo):
    conn = get_db_connection()
    # Insertar en users
    conn.execute(
        "INSERT INTO users (username, hash, rol) VALUES (?, ?, ?)",
        (username, password, rol)
    )
    user_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    # Si es paciente, insertar en pacientes
    if rol == "paciente":
        conn.execute(
            "INSERT INTO pacientes (usersid, NombreCompleto) VALUES (?, ?)",
            (user_id, nombre_completo)
        )
    conn.commit()
    conn.close()

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
    app.run(host='0.0.0.0', port=port)
