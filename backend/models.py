from sqlalchemy import Column, Integer, String, DateTime
from database import Base

class ChatMessage(Base):
    __tablename__ = "chat_messages"
    id = Column(Integer, primary_key=True, index=True)
    user_message = Column(String, nullable=False)
    ai_message = Column(String)
    timestamp = Column(DateTime, nullable=False)