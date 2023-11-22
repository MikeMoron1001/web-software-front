from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import datetime

# Modelo para la entidad Usuario
class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(150))
    contrasena = db.Column(db.String(350))
    rol = db.Column(db.String(50))

# Modelo para la entidad Producto
class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_producto = db.Column(db.String(150), unique=True)
    precio = db.Column(db.Float(precision=2))
    precio_paquete = db.Column(db.Float(precision=2))

# Modelo para la entidad Produccion
class Produccion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_producto = db.Column(db.String(150))
    precio = db.Column(db.Float(precision=2))
    contador_id = db.Column(db.Integer)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    usuario = db.Column(db.String(150))
    id_usuario = db.Column(db.Integer, nullable=False)
    rol = db.Column(db.String(50))

    
  
