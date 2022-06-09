import datetime
import os
from flask import Blueprint, request, render_template, session, redirect
from flask_login import login_required
from .models import *
from .filename_utils import *
from flask_socketio import send, emit, join_room
from .jinja_utils import *

routes = Blueprint("routes", __name__)


@routes.route("/message/<chat_id>", methods=["POST"])
@login_required
def post_message(chat_id):
    chat_id = int(chat_id)
    user_id = current_user.id
    if request.files["message_img"].filename != "":
        content = ""
        msg_type = "img"
    else:
        content = request.form["content"]
        msg_type = "text"
    time = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    new_message = Message(chat_id=chat_id, user_id=user_id, content=content, time=time, type=msg_type)
    db.session.add(new_message)
    db.session.commit()
    if msg_type == "img":
        file = request.files["message_img"]
        file.save(f"./server/static/img/messages/{chat_id}_{new_message.id}.{get_extension(file.filename)}")
        new_message.content = f"{chat_id}_{new_message.id}.{get_extension(file.filename)}"
        db.session.commit()
    participation = Participation.query.filter_by(chat_id=chat_id, user_id=user_id).first()
    participation.read_message_id = new_message.id
    db.session.commit()
    msg_json = {"chat_id": chat_id, "user_id": user_id, "content": new_message.content, "time": time, "type": msg_type,
                "sender": current_user.username}
    emit("new message from server", msg_json, namespace="/", to=session["room"])
    return message_schema.jsonify(new_message), 201


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
        if chat.messages:
            chat.description = create_chat_description(last_msg_in_chat=chat.messages[-1],
                                                       recipient_name=chat.recipient.name)
        else:
            chat.description = "Empty chat"
        all_chats_current_user_participates.append(chat)
    messages = Message.query.filter_by(chat_id=chat_id).all()
    recipient_participation = get_recipient_participation_details(chat_id)
    recipient = User.query.get(recipient_participation.user_id)
    recipient.read_message_id = recipient_participation.read_message_id
    emit("read message from server", namespace="/", to=session["room"])
    return render_template("app.html", chats=all_chats_current_user_participates, messages=messages,
                           current_user=current_user, recipient=recipient)


@routes.route("/chats", methods=["GET"])
@login_required
def empty_chats():
    optional_first_user_participation = Participation.query.filter_by(user_id=current_user.id).first()
    if optional_first_user_participation:
        return redirect(f"/chats/{optional_first_user_participation.chat_id}")
    return render_template("app.html", chats=[], current_user=current_user)


@routes.route("/user/<text>")
def get_users_by_query(text):
    result_set = set()
    result_set.update(User.query.filter(User.name.startswith(text)).all())
    result_set.update(User.query.filter(User.surname.startswith(text)).all())
    result_set.update(User.query.filter(User.username.startswith(text)).all())
    return users_schema.jsonify(result_set)


@routes.route("/chat/<recipient_id>", methods=["POST"])
def create_chat(recipient_id):
    new_chat = Chat()
    db.session.add(new_chat)
    db.session.commit()
    new_recipient_participation = Participation(chat_id=new_chat.id, user_id=recipient_id, read_message_id=-1,
                                                read_time=None)
    db.session.add(new_recipient_participation)
    new_current_user_participation = Participation(chat_id=new_chat.id, user_id=int(current_user.id),
                                                   read_message_id=-1, read_time=None)
    db.session.add(new_current_user_participation)
    db.session.commit()
    my_dto = {"id": current_user.id,
              "name": current_user.name,
              "surname": current_user.surname,
              "username": current_user.username,
              "avatar_img": current_user.avatar_img}
    emit("new chat", {"recipient": my_dto, "chat_id": new_chat.id}, namespace="/", to=f"user{recipient_id}")
    return chat_schema.jsonify(new_chat)
