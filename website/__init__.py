from dotenv import load_dotenv
load_dotenv() #Load environment variable
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import DevelopmentConfig, TestingConfig, ProductionConfig


db = SQLAlchemy()
DB_NAME = 'database.db'

def create_app():
    app = Flask(__name__)

    flask_env = os.getenv('FLASK_ENV', 'development')  # Default to 'development' if not set as it should be.


    if flask_env == 'development': #app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}, app.secret_key = 'BigJohn191 ## config info for dev
        app.config.from_object(DevelopmentConfig)
    elif flask_env == 'testing':
        app.config.from_object(TestingConfig)
    elif flask_env == 'production':
        app.config.from_object(ProductionConfig)
    else:
        # Default configuration
        app.config.from_object(Config)


    db.init_app(app) #initialise db, or utilise it if already there.

    from .views import views
    from .auth import auth

    #migrate = Migrate(app, db) <- SCALING
    #Linking app components/blueprints
    app.register_blueprint(views, url_prefix='/') #
    app.register_blueprint(auth, url_prefix='/')

    #linking model layer to control layer
    from .models import Users, Footprint, Test
    with app.app_context():
        db.create_all()

    #Help with access controls and session management
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.signin'

    @login_manager.user_loader
    def load_user(id):
        return Users.query.get(int(id))

    return app
