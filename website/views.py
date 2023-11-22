from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from . import db
from .models import Producto, Usuario, Produccion
import datetime
from datetime import timedelta
from sqlalchemy import and_, func
from sqlalchemy.orm import aliased

vistas = Blueprint('vistas', __name__)

@vistas.route('/')
def inicio():
    """Ruta para la página de inicio."""
    return render_template('inicio.html', usuario=current_user)

@vistas.route('/agregar_producto', methods=['GET', 'POST'])
@login_required
def agregar_producto():
    """Ruta para agregar un nuevo producto."""
    usuario_q = Usuario.query.filter_by(usuario=current_user.usuario).first()
    producto = request.form.get('producto')
    precio = request.form.get('precio')
    precio_paquete = request.form.get('precio_paquete')

    if not producto:
        flash('Agregue un producto', category='error')
    elif not precio:
        flash('Agregue un precio', category='error')
    else:
        producto_q = Producto.query.filter_by(nombre_producto=producto).first()

        if producto_q:
            flash('El producto ya existe.', category='error')
        else:
            # Agregar producto
            nuevo_producto = Producto(nombre_producto=producto.upper(), precio=precio, precio_paquete=precio_paquete)
            db.session.add(nuevo_producto)
            db.session.commit()
            flash('Producto agregado!', category='success')

    return render_template('admin.html', usuario=current_user, rol=usuario_q.rol)

@vistas.route('/produccion', methods=['GET', 'POST'])
@login_required
def produccion():
    """Ruta para registrar la producción de productos."""
    usuario_q = Usuario.query.filter_by(usuario=current_user.usuario).first()
    productos = Producto.query.all()
    producto_agregado = None
    print(productos)
    
    if request.method == 'POST':
        producto = request.form.get('producto')

        if not producto:
            flash('Registre un producto', category='error')
        else:

            producto_q = Producto.query.filter_by(id=producto).first()

            hoy = datetime.datetime.now().date()
            
            resultados = Produccion.query.filter(
                    and_(
                        Produccion.id_usuario == current_user.id,
                        Produccion.nombre_producto == producto_q.nombre_producto,
                        Produccion.fecha > hoy.strftime('%Y-%m-%d')
                    )
                ).order_by(Produccion.fecha.desc()).first()
            # Sacar contador_id
            if resultados:
                contador_id_q = resultados.contador_id
                if contador_id_q < 12:
                    contador_id_q = contador_id_q + 1
                else:
                    contador_id_q = 1
            else:
                contador_id_q = 1

            producto_agregado = {
                'nombre_producto': producto_q.nombre_producto,
                'precio': producto_q.precio,
                'fecha': datetime.datetime.now(),
                'rol': usuario_q.rol,
            }
            # Agregar producción
            producto_add = Produccion(nombre_producto=producto_agregado['nombre_producto'], 
                                    precio=producto_agregado['precio'], 
                                    fecha=producto_agregado['fecha'],
                                    usuario=usuario_q.usuario,
                                    id_usuario=current_user.id,
                                    contador_id=contador_id_q,
                                    rol=producto_agregado['rol'])
            
            db.session.add(producto_add)
            db.session.commit()
            flash('¡Producto agregado!', category='success')
            
            flash(f"Usuario: {usuario_q.usuario}; Fecha: {datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')}; Producto: {producto_q.nombre_producto} # {contador_id_q}; Rol: {usuario_q.rol.capitalize()}; Precio: {producto_q.precio}", 
                  category='success')

    return render_template('produccion.html', usuario=current_user, productos=productos, rol=usuario_q.rol)
    
@vistas.route('/nomina', methods=['GET', 'POST'])
@login_required
def nomina():
    """Ruta para generar la nómina basada en la producción."""
    usuario_q = Usuario.query.filter_by(usuario=current_user.usuario).first()
    rol_seleccionado = request.form.get('rol')
    
    if request.method == 'POST':
        
        usuarios = Usuario.query.filter_by(rol=rol_seleccionado).all()
        
        fecha_inicio = request.form.get('fecha_inicio')
        fecha_fin = request.form.get('fecha_fin')
        fecha_fin = datetime.datetime.strptime(fecha_fin, '%Y-%m-%d') + timedelta(days=1)

        # Sacar lista de usuarios
        lista_usuarios = list(set([i.usuario for i in usuarios]))
        print(lista_usuarios)
        produccion_por_usuario = []
        pago_total_por_usuario = []

        for usuario_rol in lista_usuarios:
            producto_alias = aliased(Producto)
            
            # Sacar lista de producciones
            producciones = (
                db.session.query(
                    Produccion.nombre_producto,
                    func.count().label('cantidad'),
                    func.avg(producto_alias.precio).label('precio_producto'),
                    func.avg(producto_alias.precio_paquete).label('precio_paquete')
                )
                .join(producto_alias, Produccion.nombre_producto == producto_alias.nombre_producto)
                .filter(
                    and_(
                        (Produccion.usuario == usuario_rol),
                        (Produccion.fecha >= fecha_inicio),
                        (Produccion.fecha <= fecha_fin)
                    )
                )
                .group_by(Produccion.nombre_producto)
                .all()
            )
            
            for produccion in producciones:
                print(produccion.nombre_producto, produccion.cantidad, produccion.precio_producto, produccion.precio_paquete)
 
            for usuario_rol in lista_usuarios:
                # Procesar resultados de producción
                produccion_q = [(produccion.nombre_producto, int(produccion.cantidad // 12), int(produccion.cantidad // 12)*produccion.precio_paquete, produccion.cantidad % 12, (produccion.cantidad % 12)*produccion.precio_producto) for produccion in producciones]
                produccion_por_usuario.append((usuario_rol, produccion_q))
                # Calcular pago total por usuario
                pago_total_por_usuario.append((usuario_rol, sum([produccion[2] for produccion in produccion_q]) + sum([produccion[4] for produccion in produccion_q])))

        return render_template('admin_nomina.html', usuario=current_user, rol=usuario_q.rol, fecha_inicio=fecha_inicio, fecha_fin=(fecha_fin - timedelta(days=1)).strftime('%Y-%m-%d') , producciones=produccion_por_usuario, pago_total=pago_total_por_usuario)

    return render_template('admin_nomina.html', usuario=current_user, producciones=None, rol=usuario_q.rol)
