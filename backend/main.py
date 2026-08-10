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
    message: str
    
# Async database dependency
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as db:
        yield db

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "FastAPI backend is running!"}

@app.get("/chat")
async def test_route():
    return {"status": "success", "data": "Backend connection working!"}

@app.post("/chat")
async def chat_endpoint(req: ChatRequest, db: AsyncSession = Depends(get_db)):
    
    mock_ai_reply = f"Echo: {req.message}"
    
    saved_msg = await create_chat_message(db=db, user_message=req.message, ai_response=mock_ai_reply)
    
    return {"response": mock_ai_reply, "saved_id": saved_msg.id}