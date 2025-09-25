"""
WSGI entry point para Render - versión ultra simple
"""

try:
    from simple_app import app
    print("✅ Cargando simple_app.py - versión ultra simple")
except ImportError as e:
    print(f"❌ Error importando simple_app: {e}")
    try:
        from render_app import app
        print("✅ Cargando render_app.py - aplicación simplificada para Render")
    except ImportError as e2:
        print(f"❌ Error importando render_app: {e2}")
        # Crear una app mínima si todo falla
        from flask import Flask
        app = Flask(__name__)
        
        @app.route('/')
        def hello():
            return "RegMed - Aplicación básica funcionando"
        
        @app.route('/health')
        def health():
            return {"status": "OK", "message": "Aplicación mínima"}
        
        print("⚠️ Usando aplicación Flask mínima")

if __name__ == "__main__":
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)