from database import conectar
import sqlite3

def obtener_todos():
    conn = conectar()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    productos = cursor.execute(
        "SELECT * FROM productos WHERE activo = 1 ORDER BY nombre"
    ).fetchall()
    conn.close()
    return productos

def obtener_por_id(id):
    conn = conectar()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    producto = cursor.execute(
        "SELECT * FROM productos WHERE id = ?", (id,)
    ).fetchone()
    conn.close()
    return producto

def crear(nombre, descripcion, precio_kg, precio_bolson, peso_bolson_kg, stock_kg, stock_minimo_kg):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO productos (nombre, descripcion, precio_kg, precio_bolson, peso_bolson_kg, stock_kg, stock_minimo_kg)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (nombre, descripcion, precio_kg, precio_bolson, peso_bolson_kg, stock_kg, stock_minimo_kg))
    conn.commit()
    conn.close()

def actualizar(id, nombre, descripcion, precio_kg, precio_bolson, peso_bolson_kg, stock_kg, stock_minimo_kg):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE productos
        SET nombre=?, descripcion=?, precio_kg=?, precio_bolson=?, peso_bolson_kg=?, stock_kg=?, stock_minimo_kg=?
        WHERE id=?
    ''', (nombre, descripcion, precio_kg, precio_bolson, peso_bolson_kg, stock_kg, stock_minimo_kg, id))
    conn.commit()
    conn.close()

def eliminar(id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("UPDATE productos SET activo = 0 WHERE id = ?", (id,))
    conn.commit()
    conn.close()

def descontar_stock(id, cantidad_kg):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE productos SET stock_kg = stock_kg - ? WHERE id = ?",
        (cantidad_kg, id)
    )
    conn.commit()
    conn.close()