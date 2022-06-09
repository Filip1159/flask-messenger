import re
from flask import Blueprint, request, render_template, redirect, url_for, session
from flask_login import login_user, login_required, logout_user, current_user
from flask_socketio import leave_room
from werkzeug.security import generate_password_hash, check_password_hash

from server.models.User import User
from server.models.Participation import Participation
from .filename_utils import *
from server import db


auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["POST"])
def login():
    """
    login route
    verifies username and password with those stored in database
    if they are incorrect renders login template with error message
    else redirects to app route
    """
    username = request.form.get("username")
    password = request.form.get("password")
    user = User.query.filter_by(username=username).first()
    if not user:
        return render_template("login.html", error=True)
    if not check_password_hash(user.password, password):
        return render_template("login.html", error=True)
    login_user(user)
    first_participation = Participation.query.filter_by(user_id=user.id).first()
    if first_participation:
        return redirect(f"/chats/{first_participation.chat_id}")
    else:
        return redirect(f"/chats")


@auth.route("/login", methods=["GET"])
def login_template():
    """
    renders login template
    """
    return render_template("login.html")


@auth.route("/logout", methods=["GET"])
@login_required
def logout():
    """
    logout route
    makes current user leave all its rooms
    removes user session
    redirects to login route
    """
    leave_room(session["room"], namespace="/", sid=session["room"])
    leave_room(f"user{current_user.id}", namespace="/", sid=session["room"])
    logout_user()
    return redirect(url_for("auth.login"))


@auth.route("/sign-up", methods=["GET"])
def sign_up_template():
    """
    renders signup template
    """
    return render_template("sign_up.html")


@auth.route("/sign-up", methods=["POST"])
def sign_up():
    """
    signup route
    verifies provided new user details
    if user avatar is not provided, saves user with default one
    saves user to database
    """
    letters_and_digits_regex = "^[0-9a-zA-ZąćęłńóśźżĄĘŁŃÓŚŹŻ]+$"
    only_letters_regex = "^[a-zA-ZąćęłńóśźżĄĘŁŃÓŚŹŻ]+$"
    username = request.form["username"]
    if len(username) < 3:
        return render_template("sign_up.html", error_message="Username must be at least 3 letters long!")
    if not re.match(letters_and_digits_regex, username):
        return render_template("sign_up.html", error_message="Username may contain only letters and digits!")
    user = User.query.filter_by(username=username).first()
    if user:
        return render_template("sign_up.html", error_message="Username is taken!")
    name = request.form["name"]
    name = name.capitalize()
    if not re.match(only_letters_regex, name):
        return render_template("sign_up.html", error_message="Name cannot be blank!")
    surname = request.form["surname"]
    surname = surname.capitalize()
    if not re.match(only_letters_regex, surname):
        return render_template("sign_up.html", error_message="Surname cannot be blank!")
    password = request.form["password"]
    result = validate_password(password)
    if result != "":
        return render_template("sign_up.html", error_message=result)
    password = generate_password_hash(password, method='sha256')
    avatar = request.files["avatar"]
    if avatar.filename == "":
        avatar.filename = "default_avatar.jpg"
    else:
        avatar.filename = f"{username}.{get_extension(avatar.filename)}"
        avatar.save(f"./server/static/img/avatars/{avatar.filename}")
    new_user = User(name=name, surname=surname, username=username, password=password, avatar_img=avatar.filename)
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for("auth.login"))


def validate_password(password: str) -> str:
    """
    password validator
    between 8 and 20 characters long
    contains at least one digit
    """
    if len(password) < 8 or len(password) > 20:
        return "Password length must be between 8 and 20 characters inclusive!"
    if not any(char.isdigit() for char in password):
        return "Password must contains at least one digit!"
    return ""
