from server import db, ma


class Message(db.Model):
    __tablename__ = "messages"
    id = db.Column(db.Integer, unique=True, primary_key=True)
    chat_id = db.Column(db.Integer, db.ForeignKey("chats.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    content = db.Column(db.String(1000))
    time = db.Column(db.DateTime)
    type = db.Column(db.String(5))

    def __init__(self, chat_id, user_id, content, time, type):
        self.chat_id = chat_id
        self.user_id = user_id
        self.content = content
        self.time = time
        self.type = type

    def __str__(self):
        return f"{self.id}, {self.chat_id}, {self.user_id}, {self.content}, {self.time}"


class MessageSchema(ma.Schema):
    class Meta:
        fields = ["id", "chat_id", "user_id", "content", "time", "type"]


message_schema = MessageSchema(strict=True)
messages_schema = MessageSchema(strict=True, many=True)
