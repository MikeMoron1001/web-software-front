from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

# Inicialización de la instancia de SQLAlchemy
db = SQLAlchemy()

# Nombre de la base de datos
NOMBRE_DB = "database.db"

def crear_aplicacion():
    """
    Configuración y creación de la aplicación Flask.
    """
    app = Flask(__name__)

    # Clave secreta para la aplicación Flask (debe cambiarse en un entorno de producción)
    app.config['SECRET_KEY'] = 'hjshjhdjahkjshkjdhjs'

    # Configuración de la URI de la base de datos SQLite
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{NOMBRE_DB}'
    
    # Inicialización de la instancia de SQLAlchemy con la aplicación Flask
    db.init_app(app)

    # Importación de las rutas desde los módulos views y auth
    from .views import vistas
    from .auth import auth
    
    # Registro de las blueprints (conjunto de rutas) en la aplicación
    app.register_blueprint(vistas, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    
    # Importación de los modelos de la base de datos
    from .models import Usuario, Producto, Produccion
    
    # Creación de las tablas en la base de datos
    with app.app_context():
        db.create_all()
    
    # Configuración del sistema de login
    login_manager = LoginManager()
    login_manager.login_view = 'auth.inicio_sesion'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def cargar_usuario(id):
        return Usuario.query.get(int(id))
    
    return app

def crear_base_datos(app):
    """
    Creación de la base de datos si no existe.
    """
    if not path.exists('website/' + NOMBRE_DB):
        db.create_all(app=app)
        print('Base de datos creada!')

  

