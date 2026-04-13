# 🧠 Multi-Source Knowledge Hub

> A production-grade RAG application that lets you chat with your documents — PDFs, web pages, and Markdown files — with source-attributed answers.

[![CI](https://github.com/yassirtl/RAG-knowledge-hub/actions/workflows/ci.yml/badge.svg)](https://github.com/yassirtl/RAG-knowledge-hub/actions)
[![Python](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## ✨ Features

- **Multi-source ingestion** — PDFs (via PyMuPDF), web pages (via trafilatura), Markdown & plain-text files
- **Source attribution** — every answer cites which documents were used, with a relevance score
- **Multi-turn chat** — maintains conversation history for follow-up questions
- **Scoped retrieval** — optionally restrict queries to a subset of your sources
- **Clean chat UI** — React + TailwindCSS with drag-and-drop upload and collapsible source cards
- **Production-ready** — Dockerised, health-checked, structured logging, Pydantic v2 settings

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Browser (React)                          │
│  ┌──────────┐   ┌──────────────────────────────────────────┐   │
│  │ Sidebar  │   │              Chat Interface               │   │
│  │ Sources  │   │  MessageBubble + SourceCard attribution   │   │
│  │ Ingest   │   │                                          │   │
│  └──────────┘   └──────────────────────────────────────────┘   │
└──────────────────────────┬──────────────────────────────────────┘
                           │ HTTP  /api/v1/
┌──────────────────────────▼──────────────────────────────────────┐
│                    FastAPI Backend                               │
│                                                                 │
│  POST /ingest/pdf   ──► PDFLoader ──────────────┐              │
│  POST /ingest/url   ──► WebLoader ──────────────┤              │
│  POST /ingest/file  ──► MarkdownLoader ──────────┤              │
│                                                  ▼              │
│                                       RecursiveCharacterSplitter│
│                                                  │              │
│                                                  ▼              │
│  POST /query/       ──► Retriever ◄──── ChromaDB + Embeddings  │
│                              │                                  │
│                              ▼                                  │
│                         RAG Chain (LCEL)                        │
│                              │                                  │
│                              ▼                                  │
│                     OpenAI GPT-4o-mini                          │
└─────────────────────────────────────────────────────────────────┘
```

**Key design decisions:**

| Concern | Choice | Rationale |
|---|---|---|
| Embeddings | `text-embedding-3-small` | Best cost/quality ratio for retrieval |
| Vector store | ChromaDB (local) | Zero infra, persistent, easy to swap |
| Chunking | RecursiveCharacterTextSplitter | Preserves semantic boundaries |
| LLM | GPT-4o-mini | Fast, cheap, grounded responses |
| Chain | LangChain LCEL | Composable, observable pipeline |

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node 20+
- An [OpenAI API key](https://platform.openai.com/api-keys)

### 1. Clone and configure

```bash
git clone https://github.com/yassirtl/RAG-knowledge-hub.git
cd knowledge-hub
cp .env.example .env
# Edit .env and set OPENAI_API_KEY
```

### 2. Run with Docker Compose (recommended)

```bash
docker compose up --build
```

- **API** → http://localhost:8000/docs
- **UI** → http://localhost:3000

### 3. Run locally (development)

**Backend:**

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Frontend:**

```bash
cd frontend
npm install
npm run dev
```

### 4. Seed with demo data

```bash
pip install httpx
python scripts/seed_demo.py --api-url http://localhost:8000
```

---

## 📁 Project Structure

```
knowledge-hub/
├── backend/
│   ├── app/
│   │   ├── api/routes/      # ingest.py, query.py
│   │   ├── core/            # embeddings, vectorstore, retriever
│   │   ├── ingestion/       # pdf_loader, web_loader, markdown_loader
│   │   ├── rag/             # chain.py (LCEL), prompts.py
│   │   ├── schemas/         # Pydantic models
│   │   ├── config.py        # Pydantic Settings
│   │   └── main.py          # FastAPI app
│   └── tests/
├── frontend/
│   └── src/
│       ├── components/      # Chat/, Ingestion/, Layout/
│       ├── hooks/           # useChat, useIngest
│       ├── lib/             # api.ts (Axios client)
│       └── types/           # Shared TypeScript types
├── scripts/
│   └── seed_demo.py
├── .github/workflows/ci.yml
├── docker-compose.yml
└── .env.example
```

---

## 🧪 Tests

```bash
cd backend
pytest tests/ -v
```

---

## 🔧 Configuration

All configuration is via environment variables (see `.env.example`):

| Variable | Default | Description |
|---|---|---|
| `OPENAI_API_KEY` | — | **Required.** OpenAI API key |
| `OPENAI_CHAT_MODEL` | `gpt-4o-mini` | Chat completion model |
| `OPENAI_EMBEDDING_MODEL` | `text-embedding-3-small` | Embedding model |
| `CHUNK_SIZE` | `512` | Token chunk size |
| `CHUNK_OVERLAP` | `64` | Token overlap between chunks |
| `TOP_K` | `5` | Number of retrieved chunks |
| `SCORE_THRESHOLD` | `0.35` | Minimum relevance score |

---

## 📄 License

MIT © 2025
