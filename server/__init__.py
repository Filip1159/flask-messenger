from flask_marshmallow import Marshmallow
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_session import Session


# init database SQLAlchemy connection, that will allow ORM
db = SQLAlchemy()
# init Marshmallow - object to json mapper
ma = Marshmallow()


def create_app():
    """
    function that creates flask app
    creates necessary config
    registers auth and routes blueprints
    DO NOT MOVE import statements, writing them outside function causes circular dependency error!
    """
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:admin@localhost:3306/connectmessenger"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # mute deprecation warning
    app.config["SECRET_KEY"] = "secret!"  # required when generating and checking password hash
    app.config["SESSION_TYPE"] = "filesystem"  # when app should store session info
    Session(app)  # create session

    db.init_app(app)
    ma.init_app(app)

    # register blueprints
    from .auth import auth
    from .routes import routes
    from .socket import socket
    app.register_blueprint(auth)
    app.register_blueprint(routes)
    socket.init_app(app)

    # configure flask_login
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from server.models.User import User

    # how flask_login should load user details
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app
