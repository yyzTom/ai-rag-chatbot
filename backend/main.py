"""
FastAPI backend

Provides REST API endpoints for chat functionality with database integration.
"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from openai import OpenAI, APIError
from dotenv import load_dotenv
from pathlib import Path
import os

from crud import create_chat_message
from database import engine, SessionLocal

load_dotenv(Path(__file__).parent.parent / ".env")

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
        
client: OpenAI | None = None
LLM_MODEL: str | None = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global client, LLM_MODEL
    # Startup
    llm_api_key = os.getenv("LLM_API_KEY")
    llm_base_url = os.getenv("LLM_BASE_URL")
    LLM_MODEL = os.getenv("LLM_MODEL")
    
    if llm_api_key and llm_base_url and LLM_MODEL:
        client = OpenAI(
            api_key=llm_api_key,
            base_url=llm_base_url
        )
    yield
    # Shutdown
    client = None

app = FastAPI(lifespan=lifespan)

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
    Chat endpoint that processes user messages, calls configurable LLM and persists chat history.

    Args:
        req: ChatRequest containing the user's message
        db: Database session dependency

    Returns:
        dict: Contains the AI response, saved message ID, and model name
    """
    if not client or not LLM_MODEL:
        raise HTTPException(status_code=503, detail="LLM Environment variables not configured. Check .env file")
    
    try:
        completion = client.chat.completions.create(
            model= LLM_MODEL,
            messages=[{"role": "user", "content": req.message}]
        )
        ai_reply = completion.choices[0].message.content or ""
    
    except APIError as e:
        raise HTTPException(status_code=500, detail=f"LLM provider error: {str(e)}")
    
    
    saved_msg = await create_chat_message(db=db, user_message=req.message, ai_response=ai_reply)
    
    return {"response": ai_reply, "saved_id": saved_msg.id, "model_used": LLM_MODEL}