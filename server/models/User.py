from server import db, ma
from flask_login import UserMixin


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, unique=True, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(30))
    surname = db.Column(db.String(30))
    avatar_img = db.Column(db.String(45))

    def __init__(self, username, password, name, surname, avatar_img):
        self.username = username
        self.password = password
        self.name = name
        self.surname = surname
        self.avatar_img = avatar_img

    def __str__(self):
        return f"{self.id}, {self.username}"


class UserSchema(ma.Schema):
    class Meta:
        fields = ["id", "username", "name", "surname", "avatar_img"]


user_schema = UserSchema(strict=True)
users_schema = UserSchema(strict=True, many=True)
