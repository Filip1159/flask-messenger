from flask import Blueprint, jsonify, request, render_template, flash, redirect, url_for, Response, session
from flask_login import login_required, current_user
from .models import *
from server import socket
from flask_socketio import send, emit, join_room
from .jinja_utils import *

routes = Blueprint("routes", __name__)


@routes.route("/message", methods=["POST"])
@login_required
def post_message():
    chat_id = int(request.json["chatId"])
    user_id = current_user.id
    content = request.json["content"]
    time = request.json["time"]
    new_message = Message(chat_id=chat_id, user_id=user_id, content=content, time=time)
    db.session.add(new_message)
    db.session.commit()
    participation = Participation.query.filter_by(chat_id=chat_id, user_id=user_id).first()
    participation.read_message_id = new_message.id
    db.session.commit()
    msg_json = {"chat_id": chat_id, "user_id": user_id, "content": content, "time": time, "sender": current_user.username}
    emit("Post message", msg_json, namespace="/", to=session["room"])


@routes.route("/chats/<chat_id>", methods=["GET"])
@login_required
def chats(chat_id):
    session["room"] = int(chat_id)
    all_current_user_participations = Participation.query.filter_by(user_id=current_user.id).all()
    all_chats_current_user_participates = []
    for p in all_current_user_participations:
        chat = Chat.query.get(p.chat_id)
        chat.recipient = get_recipient_user_details(chat.id)
        chat.messages = Message.query.filter_by(chat_id=p.chat_id).all()
        chat.description = create_chat_description(last_msg_in_chat=chat.messages[-1],
                                                   recipient_name=chat.recipient.name)
        all_chats_current_user_participates.append(chat)
    messages = Message.query.filter_by(chat_id=chat_id).all()
    recipient_participation = get_recipient_participation_details(chat_id)
    recipient = User.query.get(recipient_participation.user_id)
    recipient.read_message_id = recipient_participation.read_message_id
    emit("Read message", namespace="/", to=session["room"])
    return render_template("app.html", chats=all_chats_current_user_participates, messages=messages, current_user=current_user, recipient=recipient)


@routes.route("/user/<text>")
def get_users_by_query(text):
    users_by_name = User.query.filter_by(User.name.startswith(text))
    users_by_surname = User.query.filter_by(User.surname.startswith(text))
    users_by_username = User.query.filter_by(User.username.startswith(text))
