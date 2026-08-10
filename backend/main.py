"""
FastAPI backend

Provides REST API endpoints for chat functionality with database integration.
"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from crud import create_chat_message
from database import Base, engine, SessionLocal

# Pydantic request schema for POST /chat
class ChatRequest(BaseModel):
    """
    Request model for chat messages.

    Contains the user's message to be processed.
    """
    message: str

# Async database dependency
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Database dependency that provides an async session.

    Yields:
        AsyncSession: Database session for use in route handlers
    """
    async with SessionLocal() as db:
        yield db

app = FastAPI()

# CORS configuration to allow frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    """
    Health check endpoint.

    Returns:
        dict: Basic status message
    """
    return {"message": "FastAPI backend is running!"}

@app.get("/chat")
async def test_route():
    """
    Test endpoint to verify backend connectivity.

    Returns:
        dict: Success status and connection data
    """
    return {"status": "success", "data": "Backend connection working!"}

@app.post("/chat")
async def chat_endpoint(req: ChatRequest, db: AsyncSession = Depends(get_db)):
    """
    Chat endpoint that processes user messages and returns mock AI responses.

    Args:
        req: ChatRequest containing the user's message
        db: Database session dependency

    Returns:
        dict: Contains the AI response and saved message ID
    """
    mock_ai_reply = f"Echo: {req.message}"
    saved_msg = await create_chat_message(db=db, user_message=req.message, ai_response=mock_ai_reply)
    return {"response": mock_ai_reply, "saved_id": saved_msg.id}