from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


db = SQLAlchemy()
DB_NAME = 'database.db'

def create_app():
    app = Flask(__name__)
    app.secret_key = 'BigJohn191'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    db.init_app(app)

    from .views import views
    from .auth import auth

    #migrate = Migrate(app, db)
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import Users, Footprint, Test
    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.signin'

    @login_manager.user_loader
    def load_user(id):
        return Users.query.get(int(id))

    return app
