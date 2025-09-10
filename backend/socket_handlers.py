from app import socketio
from flask import request
from flask_socketio import join_room, leave_room
from utils import auth_from_socket


@socketio.on("connect")
def on_connect():
    user = auth_from_socket(request)
    if not user:
        return False  # reject connection
    # Optionally track user online status


@socketio.on("join_conversation")
def on_join(data):
    conv_id = data.get("conversation_id")
    join_room(f"conversation_{conv_id}")


@socketio.on("leave_conversation")
def on_leave(data):
    conv_id = data.get("conversation_id")
    leave_room(f"conversation_{conv_id}")


# Clients may also send messages directly via socket; if so, persist and broadcast
@socketio.on("send_message_socket")
def on_send_socket(data):
    # data: {conversation_id, content}
    from database import SessionLocal
    from models import Message

    db = SessionLocal()
    user = auth_from_socket(request)
    if not user:
        return
    msg = Message(
        conversation_id=data["conversation_id"],
        sender_id=user["id"],
        content=data.get("content"),
    )
    db.add(msg)
    db.commit()
    db.refresh(msg)
    payload = {
        "id": msg.id,
        "conversation_id": msg.conversation_id,
        "sender_id": msg.sender_id,
        "content": msg.content,
        "created_at": str(msg.created_at),
    }
    socketio.emit(
        "new_message", payload, room=f"conversation_{data['conversation_id']}"
    )
