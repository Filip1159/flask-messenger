from server import db, ma


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
        fields = ["chat_id", "user_id", "read_message_id", "read_time"]
