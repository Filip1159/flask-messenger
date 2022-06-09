from flask_marshmallow import Marshmallow
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_session import Session


db = SQLAlchemy()
ma = Marshmallow()


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:admin@localhost:3306/connectmessenger"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "secret!"
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)

    db.init_app(app)
    ma.init_app(app)

    from .auth import auth
    from .routes import routes
    from .socket import socket
    app.register_blueprint(auth)
    app.register_blueprint(routes)
    socket.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from server.models.User import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app
