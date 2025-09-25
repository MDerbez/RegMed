"""
Aplicación Flask simplificada para Render con SQLite
"""
import os
import sqlite3
from flask import Flask, render_template, redirect, session, request, url_for, flash
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
from datetime import datetime

# Configure application
app = Flask(__name__)

# Configuración para producción
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

def login_required(f):
    """Decorate routes to require login."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def get_db_connection():
    """Conectar a base de datos SQLite"""
    db_path = os.path.join(os.path.dirname(__file__), "pacientes.db")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    """Inicializar base de datos SQLite"""
    db_path = os.path.join(os.path.dirname(__file__), "pacientes.db")
    
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
        
        # Insertar usuario de prueba
        cursor.execute('''
            INSERT OR IGNORE INTO users (username, hash, rol) 
            VALUES (?, ?, ?)
        ''', ('demo', generate_password_hash('demo123'), 'paciente'))
        
        conn.commit()
        conn.close()
        print("Base de datos SQLite inicializada")
    else:
        print("Base de datos SQLite ya existe")

# Inicializar base de datos
init_database()

@app.route("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "OK", "message": "RegMed running on SQLite"}, 200

@app.route("/")
def index():
    """Página principal"""
    if "user_id" not in session:
        return redirect("/login")
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head><title>RegMed</title></head>
    <body>
        <h1>Bienvenido a RegMed</h1>
        <p>Aplicación funcionando correctamente en Render</p>
        <p>Usuario: {{ username }}</p>
        <a href="/logout">Cerrar sesión</a>
    </body>
    </html>
    ''', username=session.get("username", "Usuario"))

@app.route("/login", methods=["GET", "POST"])
def login():
    """Login de usuarios"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        if not username or not password:
            flash("Debe ingresar usuario y contraseña")
            return redirect("/login")
        
        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        conn.close()
        
        if user and check_password_hash(user["hash"], password):
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            session["rol"] = user["rol"]
            return redirect("/")
        else:
            flash("Usuario o contraseña incorrectos")
    
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head><title>Login - RegMed</title></head>
    <body>
        <h1>Iniciar Sesión</h1>
        {% with messages = get_flashed_messages() %}
            {% if messages %}
                {% for message in messages %}
                    <div style="color: red;">{{ message }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        <form method="post">
            <div>
                <label>Usuario:</label>
                <input type="text" name="username" required>
            </div>
            <div>
                <label>Contraseña:</label>
                <input type="password" name="password" required>
            </div>
            <div>
                <button type="submit">Ingresar</button>
            </div>
        </form>
        <p><small>Usuario de prueba: demo / demo123</small></p>
    </body>
    </html>
    ''')

@app.route("/logout")
def logout():
    """Cerrar sesión"""
    session.clear()
    return redirect("/login")

def render_template_string(template_string, **context):
    """Renderizar template desde string"""
    from jinja2 import Template
    template = Template(template_string)
    return template.render(**context)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)