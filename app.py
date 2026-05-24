from flask import Flask, render_template
import webbrowser
import threading
import sqlite3
from datetime import date
from database import inicializar_db, conectar
from routes.productos import productos_bp
from routes.ventas import ventas_bp

app = Flask(__name__)
app.secret_key = 'petshop2024'

app.register_blueprint(productos_bp)
app.register_blueprint(ventas_bp)

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
    inicializar_db()
    threading.Timer(1, abrir_navegador).start()
    app.run(debug=True)