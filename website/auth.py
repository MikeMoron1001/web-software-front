from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form.get('user')
        password = request.form.get('password')
        role = request.form.get('role')

        user_q = User.query.filter_by(user=user).first()
        if user_q:
            if role != user_q.role:
                flash('Role incorrecto, intentelo otra vez.', category='error')
            elif check_password_hash(user_q.password, password):
                flash('Ingreso exitoso!', category='success')
                login_user(user_q, remember=True)
                if role == 'admin':
                    return redirect(url_for('views.add_product'))
                else:
                    return redirect(url_for('views.production'))
            else:
                flash('Contraseña incorrecta, intentelo otra vez.', category='error')
        else:
            flash('El usuario no existe.', category='error')
    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        
        user = request.form.get('user')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        role = request.form.get('role')
        
        user_q = User.query.filter_by(user=user).first()

        if user_q and role == user_q.role:
            flash('Usuario ya existe para este rol.', category='error')
        elif len(user) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            
            new_user = User(user=user, password=generate_password_hash(password1), role=role)
            
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True) 
            flash('Account created!', category='success')
            if role == 'admin':
                return redirect(url_for('views.add_product'))
            else:
                return redirect(url_for('views.production'))

    return render_template("sign_up.html", user=current_user)
