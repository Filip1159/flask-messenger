from server import db, ma


class Chat(db.Model):
    """
    Chat entity, resolved chats table
    Contains information about chats from the whole app
    Attributes:
        id - unique integer identifier
    Relationships:
        messages - messages within this chat
        participations - users and their reading statuses
    """
    __tablename__ = "chats"
    id = db.Column(db.Integer, unique=True, primary_key=True)
    messages = db.relationship("Message", lazy=True)
    participations = db.relationship("Participation", lazy=True)

    def __str__(self):
        return str(self.id)


class ChatSchema(ma.Schema):
    """
    ChatSchema contains metadata about Chat attributes,
    that should be included by Marshmallow in serialized JSON
    """
    class Meta:
        fields = ["id"]


# single Chat json schema
chat_schema = ChatSchema(strict=True)
# multiple Chats json schema
chats_schema = ChatSchema(strict=True, many=True)
