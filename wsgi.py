"""
WSGI entry point para Render con aplicación simplificada
"""

try:
    from render_app import app
    print("✅ Cargando render_app.py - aplicación simplificada para Render")
except ImportError as e:
    print(f"❌ Error importando render_app: {e}")
    try:
        from app_sqlserver import app
        print("✅ Cargando app_sqlserver.py para Render")
    except ImportError as e2:
        print(f"❌ Error importando app_sqlserver: {e2}")
        # Fallback a app.py si es necesario (no debería pasar)
        from app import app
        print("⚠️ Fallback a app.py")

if __name__ == "__main__":
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)