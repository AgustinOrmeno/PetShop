from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from models.venta import crear_venta, obtener_venta, obtener_historial
from models.producto import obtener_todos, obtener_por_id

ventas_bp = Blueprint('ventas', __name__)

@ventas_bp.route('/ventas/nueva', methods=['GET', 'POST'])
def nueva():
    productos = obtener_todos()

    if request.method == 'POST':
        cliente = request.form.get('cliente', 'Consumidor Final')

        productos_ids  = request.form.getlist('producto_id[]')
        tipos          = request.form.getlist('tipo_venta[]')
        cantidades     = request.form.getlist('cantidad[]')

        if not productos_ids:
            flash('Agregá al menos un producto a la venta', 'danger')
            return redirect(url_for('ventas.nueva'))

        items = []
        for i in range(len(productos_ids)):
            prod = obtener_por_id(int(productos_ids[i]))
            tipo = tipos[i]
            cantidad = float(cantidades[i])

            # Validación de stock
            kg_necesarios = cantidad if tipo == 'kg' else prod['peso_bolson_kg'] * cantidad

            if kg_necesarios > prod['stock_kg']:
                flash(
                    f'Stock insuficiente para "{prod["nombre"]}". '
                    f'Disponible: {prod["stock_kg"]} kg — Necesario: {round(kg_necesarios, 2)} kg',
                    'danger'
                )
                return redirect(url_for('ventas.nueva'))

            precio_unitario = prod['precio_kg'] if tipo == 'kg' else prod['precio_bolson']

            items.append({
                'producto_id':     int(productos_ids[i]),
                'tipo_venta':      tipo,
                'cantidad':        cantidad,
                'precio_unitario': precio_unitario,
            })

        venta_id = crear_venta(cliente, items)
        flash('Venta registrada correctamente', 'success')
        return redirect(url_for('ventas.detalle', id=venta_id))

    return render_template('ventas/nueva.html', productos=productos)


@ventas_bp.route('/ventas/<int:id>')
def detalle(id):
    venta, detalle = obtener_venta(id)
    return render_template('ventas/detalle.html', venta=venta, detalle=detalle)


@ventas_bp.route('/historial')
def historial():
    ventas = obtener_historial()
    return render_template('historial/lista.html', ventas=ventas)


@ventas_bp.route('/api/precio/<int:id>/<tipo>')
def precio(id, tipo):
    """Devuelve el precio según el tipo elegido — lo usa el JS de la pantalla"""
    prod = obtener_por_id(id)
    if tipo == 'kg':
        return jsonify({'precio': prod['precio_kg']})
    else:
        return jsonify({'precio': prod['precio_bolson']})