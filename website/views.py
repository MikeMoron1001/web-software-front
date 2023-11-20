from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from . import db
from .models import Product, User
import datetime

views = Blueprint('views', __name__)

@views.route('/add_product', methods=['GET', 'POST'])
@login_required
def add_product():
    
    product = request.form.get('product')
    price = request.form.get('price')
    
    if not product:
        flash('Agregue un producto', category='error')
    elif not price:
        flash('Agregue un precio', category='error')
    else:
        product_q = Product.query.filter_by(product_name=product).first()
        if product_q:
            flash('El producto ya existe.', category='error')
        else:
            new_product = Product(product_name=product.upper(), price=price)
            db.session.add(new_product)
            db.session.commit()
            flash('Producto agregado!', category='success')

    return render_template('admin.html', user=current_user)

@views.route('/production', methods=['GET', 'POST'])
@login_required
def production():
    products = Product.query.all()
    added_product = None
    
    if request.method == 'POST':
        product = request.form.get('product')

        if not product:
            flash('Registre un producto', category='error')
        else:

            user_q = User.query.filter_by(user=current_user.user).first()
            product_q = Product.query.filter_by(id=product).first()

            added_product = {
                'product_name': product_q.product_name,
                'price': product_q.price,
                'date': datetime.datetime.now(),
                'rol': user_q.role,
            }
            
            flash(f"Usuario: {user_q.user}; Fecha: {datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')}; Producto: {product_q.product_name} # 1; Rol: {user_q.role.capitalize()}; Precio: {product_q.price}", 
                  category='success')

    return render_template('production.html', user=current_user, products=products)
    
 


