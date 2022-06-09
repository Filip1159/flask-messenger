from server import db, ma
from flask_login import UserMixin


class User(UserMixin, db.Model):
    """
    User entity, resolved users table
    Contains information about users from the whole app
    Attributes:
        id - unique integer identifier
        name - user's name
        surname - user's surname
        username - user's username, unique
        password - user's password hash generated using sha256 algorithm, as storing passwords in plain text may cause law and ethical issues
        avatar_img - filename provided by user as his avatar, defaults to default_avatar.jpg
    """
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
    """
    UserSchema contains metadata about User attributes,
    that should be included by Marshmallow in serialized JSON
    (password ignored)
    """
    class Meta:
        fields = ["id", "username", "name", "surname", "avatar_img"]


# single User json schema
user_schema = UserSchema(strict=True)
# multiple Users json schema
users_schema = UserSchema(strict=True, many=True)
