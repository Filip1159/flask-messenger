from flask import Blueprint, jsonify, request, render_template, flash, redirect, url_for, Response, session
from flask_login import login_required, current_user
from .models import *
from server import socket
from flask_socketio import send, emit


routes = Blueprint("routes", __name__)


@routes.route("/message/<message_id>", methods=["GET"])
@login_required
def get_message(message_id):
    message = Message.query.get(message_id)
    return message_schema.jsonify(message)


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
    print(new_message.id)
    print(chat_id)
    msg_json = {"chat_id": chat_id, "user_id": user_id, "content": content, "time": time, "sender": current_user.username}
    emit("Post message", msg_json, namespace="/", to=session["room"])
    return message_schema.jsonify(new_message), 201


@routes.route("/chats/<chat_id>", methods=["GET"])
@login_required
def chats(chat_id):
    session["room"] = int(chat_id)
    participantions = Participation.query.filter_by(user_id=current_user.id).all()
    participant_chats = []
    for p in participantions:
        chat = Chat.query.get(p.chat_id)
        chat_participants = Participation.query.filter_by(chat_id=p.chat_id).all()
        print("Participants")
        for pa in chat_participants:
            print(pa)
        users = []
        for pa in chat_participants:
            users.append(User.query.get(pa.user_id))
        chat.users = users
        chat.second_user = chat.users[0] if chat.users[0].id != current_user.id else chat.users[1]
        chat.messages = Message.query.filter_by(chat_id=p.chat_id).all()
        last_message = chat.messages[-1]
        chat.description = "Ty: " if current_user.id == last_message.user_id else f"{chat.second_user.name}: "
        chat.description += last_message.content[0:35]
        chat.description += "..." if len(last_message.content) > 35 else ""
        chat.name_surname = chat.second_user.name + " " + chat.second_user.surname
        participant_chats.append(chat)
    print(participant_chats)
    for chat in participant_chats:
        for u in chat.users:
            print(u)
        for m in chat.messages:
            print(m)
    if chat_id is None:
        chat_id = participant_chats[0].id
    messages = Message.query.filter_by(chat_id=chat_id)
    participations = Participation.query.filter_by(chat_id=chat_id).all()
    second_user_index = 0 if participations[0].user_id != current_user.id else 1
    second_user = User.query.get(participations[second_user_index].user_id)
    second_user_read_message_id = participations[second_user_index].read_message_id
    for message in messages:
        message.my = True if message.user_id == current_user.id else False
        message.read_by_second_user = True if message.id == second_user_read_message_id else False
    messages.username = second_user.username
    user_details = {"name_surname": f"{current_user.name} {current_user.surname}", "username": current_user.username}
    emit("Read message", namespace="/", to=session["room"])
    return render_template("messages.html", chats=participant_chats, messages=messages, user_details=user_details)


@routes.route("/chats/chat/<chat_id>")
def get_chat_by_id(chat_id):
    chat = Chat.query.get(chat_id)
    return chat_schema.jsonify(chat)


@routes.route("/status", methods=["PUT"])
def update_status():
    chat_id = request.json["chat_id"]
    user_id = request.json["user_id"]
    message_id = request.json["message_id"]
    time = request.json["time"]
    status = Participation.query.filter_by(chat_id=chat_id, user_id=user_id).first()
    if status is None:
        return Response(f'{{"message": "Product with id {id} not found"}}', status=404, mimetype="application/json")
    status.message_id = message_id
    status.time = time
    db.session.commit()
    return participation_schema.jsonify(status)


@routes.route("/user/<text>")
def get_users_by_query(text):
    users_by_name = User.query.filter_by(User.name.startswith(text))
    users_by_surname = User.query.filter_by(User.surname.startswith(text))
    users_by_username = User.query.filter_by(User.username.startswith(text))
