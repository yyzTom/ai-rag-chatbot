"""
Defines SQLAlchemy ORM models for chat message storage and management.
"""

from sqlalchemy import Column, Integer, String, DateTime
from database import Base

class ChatMessage(Base):
    """
    Chat message model for storing conversation history.

    Represents a single chat message with user input and AI response.
    """
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    user_message = Column(String, nullable=False)
    ai_message = Column(String)
    timestamp = Column(DateTime(timezone=True), nullable=False)