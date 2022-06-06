from Tools.scripts.make_ctype import method
from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user
from .models import *


auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    user = User.query.filter_by(username=username, password=password).first()
    if not user:
        return redirect(url_for('auth.login'))
    login_user(user)
    chat_id = Participation.query.filter_by(user_id=user.id).first().chat_id
    return redirect(f'/chats/{chat_id}')


@auth.route("/login", methods=["GET"])
def login_template():
    return render_template("login.html")


@auth.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


@auth.route("/sign-up", methods=["GET"])
def sign_up_template():
    return render_template("sign_up.html")


@auth.route("/sign-up", methods=["POST"])
def sign_up():
    username = request.form.get("username")
    if len(username) < 3:
        return render_template("sign_up.html", error_message="Username must be at least 3 letters long!")
    user = User.query.filter_by(username=username).first()
    if user:
        return redirect(url_for('auth.sign-up'))
    name = request.form["name"]
    if name == "":
        return render_template("sign_up.html", error_message="Name cannot be blank!")
    surname = request.form["surname"]
    if surname == "":
        return render_template("sign_up.html", error_message="Surname cannot be blank!")
    password = request.form.get("password")
    result = validate_password(password)
    if result != "":
        return render_template("sign_up.html", error_message=result)
    avatar = request.files["avatar"]
    print(avatar.filename)
    if avatar.filename == "":
        avatar.filename = "default_avatar.jpg"
    new_user = User(name=name, surname=surname, username=username, password=password, avatar_img=avatar.filename)
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for("auth.login"))


def validate_password(password: str) -> str:
    if len(password) < 8 or len(password) > 20:
        return "Password length must be between 8 and 20 characters inclusive!"
    if not any(char.isdigit() for char in password):
        return "Password must contains at least one digit!"
    return ""
