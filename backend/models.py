"""
Defines SQLAlchemy ORM models for chat message storage and management.
"""

from sqlalchemy import Column, Integer, String, DateTime, Text, Index, func
from sqlalchemy.dialects.postgresql import UUID
from pgvector.sqlalchemy import Vector
from database import Base
import uuid

class ChatMessage(Base):
    """
    Chat message model for storing conversation history.

    Represents a single chat message with user input and AI response.
    """
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    user_message = Column(String, nullable=False)
    ai_message = Column(String, nullable=False)
    timestamp = Column(DateTime(timezone=True), nullable=False)
    
class Document(Base):
    """
    Document model for storing uploaded files with vector embeddings for RAG.
    Each row = one chunk of an uploaded file.
    Zhipu embedding-2: embedding dimension = 1024
    OpenAI text-embedding-ada-002: dimension = 1536
    """
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String, nullable=False, index=True)
    file_type = Column(String, nullable=False)
    file_size = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
    chunk_index = Column(Integer, nullable=False)
    total_chunks = Column(Integer, nullable=False)
    document_id = Column(UUID(as_uuid=True), nullable=False, default=lambda: uuid.uuid4, index=True)
    
    embedding = Column(Vector(1024), nullable=False)
    
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    
    __table_args__ = (
        Index('ix_document_document_chunk', 'document_id', 'chunk_index'),
        Index('ix_document_file_name', 'file_name'),
        Index(
            'ix_documents_embedding',
            'embedding',
            postgresql_using='hnsw',
            postgresql_ops={'embedding': 'vector_l2_ops'}
        )
    )