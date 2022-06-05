import datetime

from flask import Flask, session
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_socketio import SocketIO, join_room, emit
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

    from .models import Participation, Message

    @socket.on("Read message signal")
    def read_message_signal():
        participation = Participation.query.filter_by(chat_id=int(session["room"]), user_id=current_user.id).first()
        messages = Message.query.filter_by(chat_id=int(session["room"])).all()
        participation.read_message_id = messages[-1].id
        participation.read_time = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        db.session.commit()
        print("Inside read_message_signal")
        emit("Read message", namespace="/", to=int(session["room"]))

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
