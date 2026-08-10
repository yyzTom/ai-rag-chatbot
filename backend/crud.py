"""
Provides async functions for creating and managing chat messages in the database.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from models import ChatMessage
from datetime import datetime, UTC

async def create_chat_message(
    db: AsyncSession,
    user_message: str,
    ai_response: str
):
    """
    Create a new chat message and save it to the database.

    Args:
        db: Async database session
        user_message: The message sent by the user
        ai_response: The AI's response to the user message

    Returns:
        The created ChatMessage object with database ID
    """
    db_message = ChatMessage(
        user_message = user_message,
        ai_message = ai_response,
        timestamp = datetime.now(UTC)
    )

    db.add(db_message)
    await db.commit()
    await db.refresh(db_message)
    return db_message