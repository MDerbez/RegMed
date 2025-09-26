from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return '<h1>Jomquer funcionando!</h1><p>Aplicación desplegada correctamente en Render</p>'

@app.route('/health')
def health():
    return {'status': 'OK', 'message': 'Todo funciona'}

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
