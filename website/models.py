from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import datetime

class Note (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    role = db.Column(db.String(50))
    # products = db.relationship('Product', backref='user', lazy=True)
    # productions = db.relationship('Production', backref='user', lazy=True)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(150), unique=True)
    price = db.Column(db.Float(precision=2))
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
# class Production(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
#     quantity = db.Column(db.Integer)
#     date = db.Column(db.DateTime, default=datetime.utcnow)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  
