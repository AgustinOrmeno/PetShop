from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.producto import obtener_todos, obtener_por_id, crear, actualizar, eliminar

productos_bp = Blueprint('productos', __name__)

@productos_bp.route('/productos')
def lista():
    productos = obtener_todos()
    return render_template('productos/lista.html', productos=productos)

@productos_bp.route('/productos/nuevo', methods=['GET', 'POST'])
def nuevo():
    if request.method == 'POST':
        nombre          = request.form['nombre']
        descripcion     = request.form.get('descripcion', '')
        precio_kg       = float(request.form.get('precio_kg') or 0)
        precio_bolson   = float(request.form.get('precio_bolson') or 0)
        peso_bolson_kg  = float(request.form.get('peso_bolson_kg') or 0)
        stock_kg        = float(request.form.get('stock_kg') or 0)
        stock_minimo_kg = float(request.form.get('stock_minimo_kg') or 5)

        crear(nombre, descripcion, precio_kg, precio_bolson, peso_bolson_kg, stock_kg, stock_minimo_kg)
        flash('Producto agregado correctamente', 'success')
        return redirect(url_for('productos.lista'))

    return render_template('productos/formulario.html', producto=None)

@productos_bp.route('/productos/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    producto = obtener_por_id(id)

    if request.method == 'POST':
        nombre          = request.form['nombre']
        descripcion     = request.form.get('descripcion', '')
        precio_kg       = float(request.form.get('precio_kg') or 0)
        precio_bolson   = float(request.form.get('precio_bolson') or 0)
        peso_bolson_kg  = float(request.form.get('peso_bolson_kg') or 0)
        stock_kg        = float(request.form.get('stock_kg') or 0)
        stock_minimo_kg = float(request.form.get('stock_minimo_kg') or 5)

        actualizar(id, nombre, descripcion, precio_kg, precio_bolson, peso_bolson_kg, stock_kg, stock_minimo_kg)
        flash('Producto actualizado correctamente', 'success')
        return redirect(url_for('productos.lista'))

    return render_template('productos/formulario.html', producto=producto)

@productos_bp.route('/productos/eliminar/<int:id>')
def borrar(id):
    eliminar(id)
    flash('Producto eliminado', 'warning')
    return redirect(url_for('productos.lista'))