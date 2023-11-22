from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Usuario
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

# Creación de una Blueprint llamada 'auth'
auth = Blueprint('auth', __name__)

@auth.route('/inicio-sesion', methods=['GET', 'POST'])
def inicio_sesion():
    """
    Vista para el inicio de sesión de usuarios.
    """
    rol=None
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        contrasena = request.form.get('contrasena')
        rol = request.form.get('rol')

        # Buscar el usuario en la base de datos
        usuario_q = Usuario.query.filter_by(usuario=usuario.upper()).first()
        if usuario_q:
            if rol != usuario_q.rol:
                flash('Rol incorrecto, inténtelo de nuevo.', category='error')
            elif check_password_hash(usuario_q.contrasena, contrasena):
                flash('Inicio de sesión exitoso!', category='success')
                login_user(usuario_q, remember=True)
                # Redirigir según el rol del usuario
                if rol == 'Administrador':
                    return redirect(url_for('vistas.agregar_producto'))
                else:
                    return redirect(url_for('vistas.produccion'))
            else:
                flash('Contraseña incorrecta, inténtelo de nuevo.', category='error')
        else:
            flash('El usuario no existe.', category='error')
    return render_template("inicio_sesion.html", usuario=current_user, rol=rol)

@auth.route('/cerrar-sesion')
@login_required
def cerrar_sesion():
    """
    Vista para cerrar sesión de usuarios.
    """
    logout_user()
    return redirect(url_for('auth.inicio_sesion'))

@auth.route('/registro', methods=['GET', 'POST'])
def registro():
    """
    Vista para el registro de nuevos usuarios.
    """
    rol=None
    if request.method == 'POST':
        
        usuario = request.form.get('usuario')
        contrasena1 = request.form.get('contrasena1')
        contrasena2 = request.form.get('contrasena2')
        rol = request.form.get('rol')
        
        # Verificar si el usuario ya existe
        usuario_q = Usuario.query.filter_by(usuario=usuario.upper()).first()
        
        if usuario_q:
            flash('Este usuario.', category='error')
        elif len(usuario) < 4:
            flash('El usuario debe tener más de 3 caracteres.', category='error')
        elif contrasena1 != contrasena2:
            flash('Las contraseñas no coinciden.', category='error')
        elif len(contrasena1) < 7:
            flash('La contraseña debe tener al menos 7 caracteres.', category='error')
        else:
            
            # Crear un nuevo usuario y guardarlo en la base de datos
            nuevo_usuario = Usuario(usuario=usuario.upper(), contrasena=generate_password_hash(contrasena1), rol=rol)
            
            db.session.add(nuevo_usuario)
            db.session.commit()
            login_user(nuevo_usuario, remember=True) 
            flash('¡Cuenta creada!', category='success')
            # Redirigir según el rol del nuevo usuario
            if rol == 'Administrador':
                return redirect(url_for('vistas.agregar_producto'))
            else:
                return redirect(url_for('vistas.produccion'))

    return render_template("registro.html", usuario=current_user, rol=rol)
