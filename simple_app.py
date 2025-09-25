"""
Aplicación Flask ultra-simple para Render
Sin base de datos, sin sesiones complejas, solo para verificar que funciona
"""
import os
from flask import Flask

# Configure application
app = Flask(__name__)

@app.route("/")
def index():
    """Página principal simple"""
    return '''
    <!DOCTYPE html>
    <html>
    <head><title>RegMed - Simple</title></head>
    <body>
        <h1>RegMed funcionando en Render</h1>
        <p>Esta es una versión simplificada para verificar el despliegue.</p>
        <p>Tiempo: {}
        <a href="/health">Health Check</a>
    </body>
    </html>
    '''.format(os.environ.get('TZ', 'UTC'))

@app.route("/health")
def health():
    """Health check"""
    return {
        "status": "OK", 
        "message": "RegMed Simple funcionando correctamente",
        "environment": "Render"
    }

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)