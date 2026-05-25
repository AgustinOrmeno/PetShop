from flask import Flask, render_template, redirect, request
import webbrowser
import threading
import sqlite3
import os
from datetime import date
from database import inicializar_db, conectar
from routes.productos import productos_bp
from routes.ventas import ventas_bp
from licencia import primera_ejecucion, verificar_licencia, activar_licencia, obtener_fecha_instalacion

app = Flask(__name__)
app.secret_key = 'petshop2024'

app.register_blueprint(productos_bp)
app.register_blueprint(ventas_bp)

@app.before_request
def chequear_licencia():
    rutas_libres = ['/activar', '/licencia-vencida']
    if request.path not in rutas_libres:
        if not verificar_licencia():
            return redirect('/licencia-vencida')

@app.route('/licencia-vencida')
def licencia_vencida():
    return render_template('licencia_vencida.html',
        fecha_instalacion=str(obtener_fecha_instalacion()),
        error=None
    )

@app.route('/activar', methods=['POST'])
def activar():
    clave = request.form.get('clave', '')
    if activar_licencia(clave):
        return redirect('/')
    return render_template('licencia_vencida.html',
        fecha_instalacion=str(obtener_fecha_instalacion()),
        error='Clave incorrecta. Verificá e intentá de nuevo.'
    )

@app.route('/')
def inicio():
    conn = conectar()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    total_productos = cursor.execute(
        "SELECT COUNT(*) FROM productos WHERE activo = 1"
    ).fetchone()[0]

    ventas_hoy = cursor.execute(
        "SELECT COALESCE(SUM(total), 0) FROM ventas WHERE fecha = ?",
        (str(date.today()),)
    ).fetchone()[0]

    productos_alerta = cursor.execute(
        "SELECT * FROM productos WHERE stock_kg <= stock_minimo_kg AND activo = 1"
    ).fetchall()

    conn.close()

    return render_template('index.html',
        total_productos=total_productos,
        ventas_hoy=round(ventas_hoy, 2),
        stock_bajo=len(productos_alerta),
        productos_alerta=productos_alerta
    )

def abrir_navegador():
    webbrowser.open('http://localhost:5000')

if __name__ == '__main__':
    primera_ejecucion()
    inicializar_db()
    if os.environ.get('WERKZEUG_RUN_MAIN') != 'true':
        threading.Timer(1, abrir_navegador).start()
    app.run(debug=True)
