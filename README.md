# AI RAG Chatbot

> Full-stack Retrieval-Augmented Generation AI assistant portfolio project.

## Features

- **Modern Interactive Chat Interface**: Vue 3 + TypeScript frontend with chat input, message history panel, and clean component-based UI styling
- **FastAPI Backend**: Standards-compliant RESTful API paired with PostgreSQL for permanent, persistent chat history storage
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
| Backend   | FastAPI + PostgreSQL + SQLAlchemy |
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
uvicorn main:app --reload
```


## Usage
Follow these steps to run the application locally:
1. Start the FastAPI backend server
2. Start the Vue 3 frontend development server
3. Open `http://localhost:5173` in your web browser to access the chat interface

## Roadmap
 - [ ] Stage 1: Project Base Setup
 - [ ] Stage 2: Vue 3 + TypeScript Frontend Base
 - [ ] Stage 3: FastAPI Backend & PostgreSQL Chat History
 - [ ] Stage 4: Basic LLM Integration (OpenAI API)
 - [ ] Stage 5: LangChain Document Upload Pipeline
 - [ ] Stage 6: pgvector RAG Vector Search Workflow