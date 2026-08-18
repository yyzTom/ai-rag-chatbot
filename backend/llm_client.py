"""
LLM and embedding API client wrapper
"""
from dotenv import load_dotenv
import os
import httpx

load_dotenv(dotenv_path="../.env")

LLM_BASE_URL = os.getenv("LLM_BASE_URL")
LLM_API_KEY = os.getenv("LLM_API_KEY")
EMBEDDING_MODEL = "embedding-2"

async def get_embedding(text: str) -> list[float]:
    '''Call embedding-2, return 1024-dimensional float vector list'''
    if not LLM_API_KEY or not LLM_BASE_URL:
        raise RuntimeError("LLM_API_KEY or LLM_BASE_URL not set in .env")
    
    headers = {
        "Authorization": f"Bearer {LLM_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": EMBEDDING_MODEL,
        "input": text
    }
    
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{LLM_BASE_URL}/embeddings",
            json=payload,
            headers=headers,
            timeout=30
        )
        resp.raise_for_status()
        data = resp.json()
        return data["data"][0]["embedding"]