# AI RAG Chatbot

> Full-stack Retrieval-Augmented Generation AI assistant portfolio project.

## Features

- **Modern Interactive Chat Interface**: Vue 3 + TypeScript frontend with chat input, message history panel, and clean component-based UI styling
- **FastAPI Backend**: Standards-compliant RESTful API paired with PostgreSQL for permanent, persistent chat history storage
- **Database Migration Management**: Alembic for version-controlled database schema management and migrations
- **AI-Powered Chat Responses**: Configurable LLM integration supporting any OpenAI‑compatible API endpoints (Zhipu GLM, Ollama, OpenAI etc.) for natural language chat completions
- **Custom Document Upload Pipeline**: PDF and plain‑text file upload support, with document parsing and text‑chunk splitting for RAG ingestion
- **Semantic Vector Search (RAG)**: PostgreSQL pgvector extension enabling embedding-based similarity search, delivering context-aware AI answers grounded in your private uploaded documents

## Tech Stack

| Component | Technology |
|-----------|------------|
| Frontend  | Vue 3 + TypeScript + Vite + Element Plus + Pinia + Axios |
| Backend   | FastAPI + PostgreSQL + SQLAlchemy + Alembic |
| LLM       | OpenAI‑compatible APIs (Zhipu GLM, Ollama, OpenAI) |
| RAG       | LangChain + pgvector |


## Setup

### Prerequisites
- Node.js 18+ and npm
- Python 3.10+
- Docker Desktop (provides pgvector‑enabled PostgreSQL instance; native Windows PostgreSQL does **not** support pgvector extension)

### Installation

#### Frontend
```bash
cd frontend
npm install
npm run dev
```
#### Backend
```bash
cd backend
python -m venv venv

# On Windows:
venv\Scripts\activate

# On Mac/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

#### Project environment
- Open `.env`, fill database credentials, LLM provider API key, base URL and model name.

### Database Prep
1. We use `docker‑compose.yml` to spin up a pre‑configured PostgreSQL instance with pgvector extension.
```bash
docker compose up -d
```
2. Apply Alembic migrations to create database tables:
```bash
cd backend
alembic upgrade head
```
> When SQLAlchemy models are modified:
> ```
> alembic revision --autogenerate -m "describe change"
> # Review generated file in alembic/versions before applying
> alembic upgrade head
> ```

### Start Backend Server
```bash
uvicorn main:app --reload
```

## Usage
Follow these steps to run the application locally:
1. Copy `.env.example` → `.env` at project root, configure database credentials and LLM provider settings
2. Start PostgreSQL database container: `docker compose up -d`
3. Apply database migrations
4. Start the FastAPI backend server
5. Start the Vue 3 frontend development server
6. Open `http://localhost:5173` in your web browser to access the chat interface