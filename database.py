import sqlite3

def conectar():
    return sqlite3.connect('petshop.db')

def inicializar_db():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre      TEXT NOT NULL,
            descripcion TEXT,
            precio_kg       REAL,
            precio_bolson   REAL,
            peso_bolson_kg  REAL DEFAULT 0,
            stock_kg        REAL DEFAULT 0,
            stock_minimo_kg REAL DEFAULT 5,
            activo      INTEGER DEFAULT 1
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ventas (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha       TEXT NOT NULL,
            total       REAL NOT NULL,
            cliente     TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS detalle_venta (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            venta_id        INTEGER NOT NULL,
            producto_id     INTEGER NOT NULL,
            tipo_venta      TEXT NOT NULL,
            cantidad        REAL NOT NULL,
            precio_unitario REAL NOT NULL,
            subtotal        REAL NOT NULL,
            FOREIGN KEY (venta_id) REFERENCES ventas(id),
            FOREIGN KEY (producto_id) REFERENCES productos(id)
        )
    ''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    inicializar_db()
    print('Base de datos creada ✅')