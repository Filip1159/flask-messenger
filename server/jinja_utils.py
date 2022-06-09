from flask_login import current_user
from .models import Message, User, Participation


def create_chat_description(last_msg_in_chat: Message, recipient_name: str) -> str:
    result = "You: " if current_user.id == last_msg_in_chat.user_id else f"{recipient_name}: "
    if last_msg_in_chat.type == "text":
        result += last_msg_in_chat.content[0:35]
    else:
        result += "Send image"
    result += "..." if len(last_msg_in_chat.content) > 35 else ""
    return result


def get_all_users_that_participates_in_chat(chat_id: int) -> list:
    participations = Participation.query.filter_by(chat_id=chat_id).all()
    return [User.query.get(p.user_id) for p in participations]


def get_recipient_participation_details(chat_id: int):
    participations = Participation.query.filter_by(chat_id=chat_id).all()
    recipient_index = 0 if participations[0].user_id != current_user.id else 1
    return participations[recipient_index]


def get_recipient_user_details(chat_id: int):
    recipient_participation = get_recipient_participation_details(chat_id)
    return User.query.get(recipient_participation.user_id)
