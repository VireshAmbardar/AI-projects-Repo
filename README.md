# AI Trading Chatbot (PDF‑Based RAG)

An **AI chatbot API** that answers questions **only from your financial PDFs** (no guessing, no outside knowledge).  
It uses a **Retrieval‑Augmented Generation (RAG)** pipeline: *find the most relevant PDF text → give that text to the LLM → generate an answer with citations.*

---

## What you get

- ✅ Upload multiple PDFs (your “knowledge base”)
- ✅ Ask questions via an API endpoint
- ✅ Answers are grounded in the uploaded documents
- ✅ Optional chat memory per `session_id` (simple in‑memory store)

---

## Tech stack

- **Python**
- **FastAPI** (API server)
- **PDF text extraction**: `pdfplumber` (primary) + **Docling fallback**
- **Embeddings**: `sentence-transformers`
- **Vector store**: **ChromaDB**
- **Hybrid retrieval**: dense (vectors) + BM25 (keyword) + RRF (fusion)
- **LLM**: Groq Chat Completions (used for query rewrite + final answer)

---

## Project structure

```text
ai-trading-chatbot/
├── .venv/                 # Poetry in-project virtual environment
├── app/
│   ├── main.py            # FastAPI entry point + routes
│   ├── settings.py        # Pydantic settings (.env loader)
│   ├── ingest.py          # PDF loading + chunking + ingestion
│   ├── embeddings.py      # Embedding generation
│   ├── rag.py             # Chroma helpers (store + metadata validation)
│   ├── retriver.py        # Hybrid retrieval + answer generation
│   ├── llm_call.py        # Groq calls (rewrite + response generation)
│   └── memory.py          # Simple in-memory chat history
├── schemas/
│   ├── chat.py            # chat body
├── data/
│   └── pdfs/              # local PDFs
├── .env                   # Your environment variables
├── .envtemplate           # Example env file
├── pyproject.toml         # Poetry config
├── poetry.lock            # Locked dependencies
└── README.md
```

---

## Setup instructions

### 1) Prerequisites

- **Python 3.12+**
- **Poetry** (tested with `2.1.3`)

### 2) Create the virtual environment (Poetry)

Use an in‑project virtual environment so `.venv/` lives inside the repo:

```bash
poetry config virtualenvs.in-project true
```

Initialize and install dependencies:

```bash
poetry init
poetry install
```

> Adding more packages later:
>
> ```bash
> poetry add <package-name>
> ```
>
> Your dependencies will appear under `[tool.poetry.dependencies]` in `pyproject.toml`.

### 3) Configure environment variables

Create a `.env` file (or copy from `.envtemplate`). Example:

```env
APP_NAME="AI Trading Chatbot API"
APP_DESCRIPTION="API for PDF upload and RAG-based QA"
APP_VERSION="0.1.0"
PORT=8032

# Required for LLM calls
GROQ_API_KEY="your_api_key_here"
```

**How config is loaded**
- `app/settings.py` uses `pydantic.BaseSettings` to read `.env`
- `app/main.py` uses those settings for app metadata and docs paths

### 4) Run the API server

This project expects a small launcher script `run.py` so the app can start on the port from `.env`.

Run:

```bash
# Windows
python run.py

# Linux / macOS
python3 run.py
```

Open the Swagger docs:

- `http://localhost:8032/api/docs/`

---

## How the PDFs are processed (Ingestion)

When you upload PDFs, the app converts them into searchable “chunks” and stores them in Chroma.

### Ingestion pipeline (simple view)

```text
PDF upload
  ↓
Extract text (PDFPlumber)
  ↓ (fallback if text is too small)
Extract markdown/tables (Docling)
  ↓
Split into chunks (RecursiveCharacterTextSplitter)
  ↓
Create embeddings (sentence-transformers)
  ↓
Store in Chroma (documents + embeddings + metadata)
```

### What happens inside `app/ingest.py`

1. **Read file bytes**
2. **Compute SHA‑256 hash**
   - The hash becomes a stable `file_key`
   - Prevents re‑ingesting the *same* file content
3. **Extract content**
   - Primary: `PDFPlumberLoader`
   - Fallback: Docling (useful for scanned PDFs or PDFs where extraction fails)
4. **Chunking**
   - Default: `chunk_size=1000`, `chunk_overlap=200`
5. **Embeddings**
   - Generated in `app/embeddings.py`
   - Embeddings are normalized (good for cosine similarity)
6. **Metadata cleanup**
   - `app/rag.py` ensures metadata is “Chroma‑safe” (only scalar values)
7. **Write to Chroma**
   - Stable chunk IDs like: `{file_key}_doc_{i}`
8. **Cache**
   - Writes a local JSON cache so the same PDF isn’t processed again

**Result format** (per uploaded file):

```json
{ "filename": "report.pdf", "status": "ingested" }
```

or:

```json
{ "filename": "report.pdf", "status": "skipped", "reason": "already_ingested" }
```

---

## How querying works (Retrieval + Answer)

When you ask a question, the system **retrieves** the most relevant chunks and then generates an answer **only from that context**.

### Retrieval pipeline (simple view)

```text
User question
  ↓
rewrite into a standalone search query (LLM)
  ↓
Dense search (Chroma vectors)  +  Keyword search (BM25)
  ↓
Fuse results (RRF)
  ↓
rerank (bge-reranker)
  ↓
Build "Context Excerpts" + citations [1], [2], ...
  ↓
LLM generates final answer (grounded)
```

### Chat memory (`app/memory.py`)

- The API keeps a small, **in-memory** message history per `session_id`
- It resets when the server restarts
- Default `session_id` is `"default"` unless you pass a custom one

---

## How to query the chatbot

### 1) Upload PDFs

**Endpoint:** `POST /upload-pdfs`  
**Body:** `multipart/form-data` with `files`

Example with `curl`:

```bash
curl -X POST "http://localhost:8032/upload-pdfs"   -H "accept: application/json"   -F "files=@data/pdfs/file1.pdf"   -F "files=@data/pdfs/file2.pdf"
```

### 2) Ask a question

**Endpoint:** `POST /chat`  
**Body:** JSON with your message (matches `app.schemas.chat.ChatInput`)

Example:

```bash
curl -X POST "http://localhost:8032/chat"   -H "accept: application/json"   -H "Content-Type: application/json"   -d '{
    "user_message": "What does the PDF say about risk management?"
  }'
```

Response:

```json
{ "response": "..." }
```

> **Tip (per-user memory):**  
> Currently as there is no user so we are skipping this part but if you want separate conversation history for each user, pass a `session_id` into `hybrid_retrieve()` (e.g., from request headers or a user id).

---
