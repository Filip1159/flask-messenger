from server import db, ma
from flask_login import UserMixin


class Chat(db.Model):
    __tablename__ = "chats"
    id = db.Column(db.Integer, unique=True, primary_key=True)
    messages = db.relationship("Message", lazy=True)
    participations = db.relationship("Participation", lazy=True)

    # def __init__(self):
    #     pass

    def __str__(self):
        return str(self.id)


class ChatSchema(ma.Schema):
    class Meta:
        fields = ["id"]


chat_schema = ChatSchema(strict=True)
chats_schema = ChatSchema(many=True, strict=True)


class Message(db.Model):
    __tablename__ = "messages"
    id = db.Column(db.Integer, unique=True, primary_key=True)
    chat_id = db.Column(db.Integer, db.ForeignKey("chats.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    content = db.Column(db.String(1000))
    time = db.Column(db.DateTime)

    def __init__(self, chat_id, user_id, content, time):
        self.chat_id = chat_id
        self.user_id = user_id
        self.content = content
        self.time = time

    def __str__(self):
        return f"{self.id}, {self.chat_id}, {self.user_id}, {self.content}, {self.time}"


class MessageSchema(ma.Schema):
    class Meta:
        fields = ("id", "chat_id", "user_id", "content", "time")


message_schema = MessageSchema(strict=True)
messages_schema = MessageSchema(many=True, strict=True)


class Participation(db.Model):
    __tablename__ = "participations"
    chat_id = db.Column(db.Integer, db.ForeignKey("chats.id"), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    read_message_id = db.Column(db.Integer, db.ForeignKey("messages.id"))
    read_time = db.Column(db.DateTime)

    def __init__(self, chat_id, user_id, read_message_id, read_time):
        self.chat_id = chat_id
        self.user_id = user_id
        self.read_message_id = read_message_id
        self.read_time = read_time

    def __str__(self):
        return f"{self.chat_id}, {self.user_id}, {self.read_message_id}, {self.read_time}"


class ParticipationSchema(ma.Schema):
    class Meta:
        fields = ("chat_id", "user_id", "read_message_id", "read_time")


participation_schema = ParticipationSchema(strict=True)
participations_schema = ParticipationSchema(many=True, strict=True)


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, unique=True, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(30))
    surname = db.Column(db.String(30))

    def __init__(self, login, password, name, surname):
        self.login = login
        self.password = password
        self.name = name
        self.surname = surname

    def __str__(self):
        return f"{self.id}, {self.username}"


class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "login", "password", "name", "surname")


user_schema = UserSchema(strict=True)
users_schema = UserSchema(many=True, strict=True)
