from database import conectar
import sqlite3
from datetime import date

def crear_venta(cliente, items):
    conn = conectar()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    total = sum(i['cantidad'] * i['precio_unitario'] for i in items)

    cursor.execute(
        "INSERT INTO ventas (fecha, total, cliente) VALUES (?, ?, ?)",
        (str(date.today()), total, cliente)
    )
    venta_id = cursor.lastrowid

    for item in items:
        subtotal = item['cantidad'] * item['precio_unitario']
        cursor.execute('''
            INSERT INTO detalle_venta
            (venta_id, producto_id, tipo_venta, cantidad, precio_unitario, subtotal)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (venta_id, item['producto_id'], item['tipo_venta'],
              item['cantidad'], item['precio_unitario'], subtotal))

        # Descuenta stock en la misma conexión
        if item['tipo_venta'] == 'kg':
            cursor.execute(
                "UPDATE productos SET stock_kg = stock_kg - ? WHERE id = ?",
                (item['cantidad'], item['producto_id'])
            )
        else:
            # Bolsón: descuenta el peso definido en el producto
            prod = cursor.execute(
                "SELECT peso_bolson_kg FROM productos WHERE id = ?",
                (item['producto_id'],)
            ).fetchone()
            cursor.execute(
                "UPDATE productos SET stock_kg = stock_kg - ? WHERE id = ?",
                (prod['peso_bolson_kg'] * item['cantidad'], item['producto_id'])
            )

    conn.commit()
    conn.close()
    return venta_id

def obtener_venta(id):
    conn = conectar()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    venta = cursor.execute(
        "SELECT * FROM ventas WHERE id = ?", (id,)
    ).fetchone()
    detalle = cursor.execute('''
        SELECT d.*, p.nombre
        FROM detalle_venta d
        JOIN productos p ON p.id = d.producto_id
        WHERE d.venta_id = ?
    ''', (id,)).fetchall()
    conn.close()
    return venta, detalle

def obtener_historial():
    conn = conectar()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    ventas = cursor.execute(
        "SELECT * FROM ventas ORDER BY fecha DESC, id DESC"
    ).fetchall()
    conn.close()
    return ventas