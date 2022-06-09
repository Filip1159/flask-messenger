from server import db, ma


class Chat(db.Model):
    __tablename__ = "chats"
    id = db.Column(db.Integer, unique=True, primary_key=True)
    messages = db.relationship("Message", lazy=True)
    participations = db.relationship("Participation", lazy=True)

    def __str__(self):
        return str(self.id)


class ChatSchema(ma.Schema):
    class Meta:
        fields = ["id"]


chat_schema = ChatSchema(strict=True)
chats_schema = ChatSchema(strict=True, many=True)
