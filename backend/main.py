from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic: create tables before app runs
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)

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
def chat_endpoint(message: str):
    return {"response": f"Received message: {message}"}