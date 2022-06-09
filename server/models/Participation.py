from server import db, ma


class Participation(db.Model):
    """
    Participation entity, resolved participations table
    Relationship class between users and chats, that contains additional information about
    how and when users follow chat and read messages
    Attributes:
        chat_id - chat_identifier, part of composite key
        user_id - user identifier, part of composite key
        read_message_id - identifier of message, that was latest read be user
        read_time - time, when latest read message was read by user
    """
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
    """
    ParticipationSchema contains metadata about Participation attributes,
    that should be included by Marshmallow in serialized JSON
    """
    class Meta:
        fields = ["chat_id", "user_id", "read_message_id", "read_time"]


# single Participation json schema
participation_schema = ParticipationSchema(strict=True)
# multiple Participations json schema
participations_schema = ParticipationSchema(strict=True, many=True)
