from sqlalchemy.ext.asyncio import AsyncSession
from models import ChatMessage
from datetime import datetime, UTC

async def create_chat_message(
    db: AsyncSession,
    user_message: str,
    ai_response: str
):
    db_message = ChatMessage(
        user_message = user_message,
        ai_message = ai_response,
        timestamp = datetime.now(UTC)
    )
    
    db.add(db_message)
    await db.commit()
    await db.refresh(db_message)
    return db_message