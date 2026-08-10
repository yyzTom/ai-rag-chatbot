# AI RAG Chatbot

> Full-stack Retrieval-Augmented Generation AI assistant portfolio project.

## Features

- **Modern Interactive Chat Interface**: Vue 3 + TypeScript frontend with chat input, message history panel, and clean component-based UI styling
- **FastAPI Backend**: Standards-compliant RESTful API paired with PostgreSQL for permanent, persistent chat history storage
- **Database Migration Management**: Alembic for version-controlled database schema management and migrations
- **AI-Powered Chat Responses**: Native OpenAI LLM API integration to generate intelligent, natural language replies to user prompts
- **Custom Document Upload Pipeline**: PDF and plain text file upload support, powered by LangChain for automated text splitting and chunk processing
- **Semantic Vector Search (RAG)**: PostgreSQL pgvector extension enabling embedding-based similarity search, delivering context-aware AI answers grounded in your private uploaded documents

## Architecture
```
  User → Frontend (Vue 3) → Backend (FastAPI) → PostgreSQL
   ↓
 OpenAI LLM
```

The frontend sends chat messages to the FastAPI backend, which queries the database for chat history and calls OpenAI for AI responses. Document uploads are processed through LangChain and stored as vectors in pgvector for retrieval.



## Tech Stack

| Component | Technology |
|-----------|------------|
| Frontend  | Vue 3 + TypeScript + Vite + Element Plus + Pinia + Axios |
| Backend   | FastAPI + PostgreSQL + SQLAlchemy + Alembic |
| LLM       | OpenAI API |
| RAG       | LangChain + pgvector |


## Setup

### Prerequisites
- Node.js 18+ and npm
- Python 3.10+
- PostgreSQL 15+ (for chat history and vector storage)

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

### Database Prep
1. Create an empty PostgreSQL database (via pgAdmin or psql).
2. Create backend/.env and populate DATABASE_URL with your database credentials.
3. Apply Alembic migrations to create all database tables:
```bash
alembic upgrade head
```
> When SQLAlchemy models are modified, generate new migration:
> ```
> alembic revision --autogenerate -m "describe change (#issue‑number)"
> # Review generated file in alembic/versions before applying
> alembic upgrade head
> ```

### Start Backend Server
```bash
uvicorn main:app --reload
```


## Usage
Follow these steps to run the application locally:
1. Create empty PostgreSQL database and configure backend `.env` with database credentials and LLM API key
2. Apply database migrations: `alembic upgrade head`
3. Start the FastAPI backend server
4. Start the Vue 3 frontend development server
5. Open `http://localhost:5173` in your web browser to access the chat interface