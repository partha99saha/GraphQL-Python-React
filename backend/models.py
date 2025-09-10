from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
import bcrypt


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, index=True, nullable=False)
    display_name = Column(String(120))
    password_hash = Column(String(256))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def set_password(self, password: str):
        self.password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    def check_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode(), self.password_hash.encode())


class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=True)
    is_group = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    participants = relationship(
        "ConversationParticipant", back_populates="conversation"
    )
    messages = relationship(
        "Message", back_populates="conversation", order_by="Message.created_at"
    )


class ConversationParticipant(Base):
    __tablename__ = "conversation_participants"
    id = Column(Integer, primary_key=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    conversation = relationship("Conversation", back_populates="participants")
    user = relationship("User")


class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"))
    sender_id = Column(Integer, ForeignKey("users.id"))
    content = Column(Text, nullable=True)
    attachment_url = Column(String(500), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    conversation = relationship("Conversation", back_populates="messages")
    sender = relationship("User")
