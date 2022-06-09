from flask_socketio import SocketIO, join_room, emit
from flask import session
from flask_login import current_user
import datetime
from server import db

from server.models.Participation import Participation
from server.models.Message import Message


# establishes websocket connection
# allows for low latency realtime communication necessary in chat application
# emits events to clients about new incoming messages, chats and info about reading their messages by their recipients
socket = SocketIO()


@socket.on("connected")
def on_connected():
    """
    connect acknowledgment, required for joining rooms
    joins room equal to active chat's id - for sending new messages and info about reading messages
    join room equal to user[signed in user's id] - for new chats
    """
    join_room(session["room"])
    join_room(f"user{current_user.id}")


@socket.on("read message from client")
def read_message_signal():
    """
    read message from client event
    info, that message was read by its recipient
    updates Participation details
    sends read message from server to second chat participant
    """
    participation = Participation.query.filter_by(chat_id=int(session["room"]), user_id=current_user.id).first()
    messages = Message.query.filter_by(chat_id=int(session["room"])).all()
    participation.read_message_id = messages[-1].id
    participation.read_time = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    db.session.commit()
    emit("read message from server", namespace="/", to=int(session["room"]))
