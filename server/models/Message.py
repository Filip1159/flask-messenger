from server import db, ma


class Message(db.Model):
    """
    Message entity, resolved message table
    Contains information about messages from the whole app
    Attributes:
        id - unique integer identifier
        chat_id - identifies chat that message belongs to
        user_id - identifies user, who sent this message
        content - message itself, contains either a text or a filename if message itself is an image
        time - when this message was sent
        type - distinguishes text messages ("text") from images ("img")
    """
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
    """
    MessageSchema contains metadata about Message attributes,
    that should be included by Marshmallow in serialized JSON
    """
    class Meta:
        fields = ["id", "chat_id", "user_id", "content", "time", "type"]


# single Message json schema
message_schema = MessageSchema(strict=True)
# multiple Messages json schema
messages_schema = MessageSchema(strict=True, many=True)
