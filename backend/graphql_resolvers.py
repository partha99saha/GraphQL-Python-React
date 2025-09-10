from ariadne import QueryType, MutationType
from database import SessionLocal
from models import User, Conversation, Message, ConversationParticipant
from utils import create_jwt, get_user_from_token
from azure_blob import upload_file_stream
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash


query = QueryType()
mutation = MutationType()


# ----------------------
# Query Resolvers
# ----------------------


@query.field("me")
def resolve_me(_, info):
    user = info.context.get("user")
    if not user:
        return None
    db = SessionLocal()
    return db.query(User).filter(User.id == user["id"]).first()


@query.field("conversations")
def resolve_conversations(_, info):
    user = info.context.get("user")
    if not user:
        return []
    db = SessionLocal()
    convs = (
        db.query(Conversation)
        .join(ConversationParticipant)
        .filter(ConversationParticipant.user_id == user["id"])
        .all()
    )
    return convs


# ----------------------
# Mutation Resolvers
# ----------------------


@mutation.field("register")
def resolve_register(_, info, username, display_name, password):
    db = SessionLocal()
    if db.query(User).filter(User.username == username).first():
        return {"success": False, "token": None, "user": None}

    hashed = generate_password_hash(password)
    user = User(username=username, display_name=display_name, password=hashed)
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_jwt(user)
    return {"success": True, "token": token, "user": user}


@mutation.field("login")
def resolve_login(_, info, username, password):
    db = SessionLocal()
    user = db.query(User).filter(User.username == username).first()
    if not user or not check_password_hash(user.password, password):
        return {"success": False, "token": None, "user": None}

    token = create_jwt(user)
    return {"success": True, "token": token, "user": user}


@mutation.field("createConversation")
def resolve_create_conversation(_, info, title, participant_ids):
    db = SessionLocal()
    user = info.context.get("user")
    if not user:
        return None

    conv = Conversation(title=title, is_group=(len(participant_ids) > 1))
    db.add(conv)
    db.commit()
    db.refresh(conv)

    # Add participants
    db.add(ConversationParticipant(user_id=user["id"], conversation_id=conv.id))
    for pid in participant_ids:
        db.add(ConversationParticipant(user_id=int(pid), conversation_id=conv.id))
    db.commit()

    return conv


@mutation.field("sendMessage")
def resolve_send_message(_, info, input):
    db = SessionLocal()
    user = info.context.get("user")
    if not user:
        return {"success": False, "message": None}

    conv_id = int(input["conversation_id"])
    content = input.get("content")
    attachment_filename = input.get("attachment_filename")
    attachment_url = None

    # File upload (if passed via multipart)
    if attachment_filename and info.context.get("files"):
        f = info.context["files"].get(attachment_filename)
        if f:
            attachment_url = upload_file_stream(
                f.stream, f.filename, content_type=f.content_type
            )

    message = Message(
        conversation_id=conv_id,
        sender_id=user["id"],
        content=content,
        attachment_url=attachment_url,
    )
    db.add(message)
    db.commit()
    db.refresh(message)

    # Emit via socketio
    payload = {
        "id": message.id,
        "conversation_id": message.conversation_id,
        "sender_id": message.sender_id,
        "content": message.content,
        "attachment_url": message.attachment_url,
        "created_at": str(message.created_at),
    }
    socketio = current_app.extensions["socketio"]
    socketio.emit("new_message", payload, room=f"conversation_{conv_id}")

    return {"success": True, "message": message}


# ----------------------
# Schema
# ----------------------

from ariadne import make_executable_schema, load_schema_from_path

type_defs = load_schema_from_path("graphql_schema.graphql")

schema = make_executable_schema(
    type_defs,
    query,
    mutation,
)
