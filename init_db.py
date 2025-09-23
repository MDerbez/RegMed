#!/usr/bin/env python3
"""
Script para inicializar la base de datos en Render
"""
import sqlite3
import os

def init_database():
    """Inicializar base de datos SQLite"""
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

if __name__ == "__main__":
    init_database()