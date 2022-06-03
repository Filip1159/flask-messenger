from flask import Flask, session
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_socketio import SocketIO, join_room
from flask_session import Session


db = SQLAlchemy()
ma = Marshmallow()
socket = SocketIO()


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:admin@localhost:3306/connectmessenger"
    app.config["SECRET_KEY"] = "secret!"
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)

    db.init_app(app)
    ma.init_app(app)
    socket.init_app(app)

    @socket.on("my event")
    def handle_message(data):
        print("received " + str(data))
        join_room(1)

    @socket.on("new message")
    def handle_message(data):
        print("received " + str(data))

    from .auth import auth
    from .routes import routes
    app.register_blueprint(auth)
    app.register_blueprint(routes)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app
