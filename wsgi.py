"""
WSGI entry point para Render
Este archivo importa explícitamente app_sqlserver para evitar confusión
"""

try:
    from app_sqlserver import app
    print("✅ Cargando app_sqlserver.py para Render")
except ImportError as e:
    print(f"❌ Error importando app_sqlserver: {e}")
    # Fallback a app.py si es necesario (no debería pasar)
    from app import app
    print("⚠️ Fallback a app.py")

if __name__ == "__main__":
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)