from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user
from .models import *


auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    print(username)
    print(password)
    user = User.query.filter_by(username=username, password=password).first()
    print(user)
    if not user:
        flash('Please check your login details and try again.')
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
