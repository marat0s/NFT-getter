from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'jeofejafoiaejfoihjof'
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:qwerty@localhost:4444"
    app.config['SQLALCHEMY_BINDS'] = {
        "nft": "postgresql://postgres:qwerty@localhost:4444/nft",
        "auth": "postgresql://postgres:qwerty@localhost:4444/auth"
    }
    db.init_app(app)


    from .routes import routes
    from .auth import auth
    from .nft import nft

    app.register_blueprint(nft, url_prefix='/')
    app.register_blueprint(routes, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Nft

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

