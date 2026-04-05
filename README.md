# Business Idea Evaluator 

Ai system that helps founders evaluate startup ideas from multiple expert perspectives.

We will employee 2 key techniques.
1. Parallelization
2. human-in-the-loop

---

## Working

1. the syetem will talk with user directly. it will ask clearifying questions till it gets enough information to evaluate the idea. keeping human in the loop to steer the process.
2. Once the idea is well defined, the application will distribute the work into several specialized  Aiagents.
3. Each agent will evaluate the idea from its own perspective.
4. Finally, the application will compile the reports from all agents and present them to the user.

---

## Reference Project Example

One example AI project in this repository is an **AI Trading Chatbot (PDF-Based RAG)**.

It is an **AI chatbot API** that answers questions **only from uploaded financial PDFs** using a **Retrieval-Augmented Generation (RAG)** pipeline.

### What this example project does

- Upload multiple PDFs as a knowledge base
- Ask questions through an API
- Generate answers grounded only in uploaded documents
- Optionally maintain chat memory using `session_id`

---

## Tech Stack

- **Python**
- **FastAPI**
- **pdfplumber** with **Docling fallback**
- **sentence-transformers**
- **ChromaDB**
- **BM25 + Dense Retrieval + RRF**
- **Groq Chat Completions**
- **Poetry** for dependency management

---

## Project Structure

```text
ai-trading-chatbot/
├── .venv/                 # Poetry in-project virtual environment
├── app/
├── routers/               # Contain Schemasa for Endpoint
│     ├── heartbeat.py     # Template function.
│   ├── main.py            # FastAPI entry point + routes
├── schemas/               # Contain Schemasa for Endpoint
├── data/
│   └── pdfs/              # Local PDFs
│   example/               # Excel for Endpoint with example inputs
├── .env                   # Environment variables
├── .envtemplate           # Example env file
├── pyproject.toml         # Poetry config
├── poetry.lock            # Locked dependencies
└── README.md
```

---

## Environment Versions

This project is being run with:

- **Poetry version:** `2.3.2`
- **Python version:** `3.12.3`

---

## Application Name Setup

Inside poetry.toml file replace

- name
- description
- version

---

## Setup Instructions

### 1) Prerequisites

Make sure the following are installed on your system:

- **Python 3.14.2**
- **Poetry 2.3.2**

### 2) Configure Poetry

Use an in-project virtual environment so the `.venv/` folder is created inside the project:

```bash
poetry config virtualenvs.in-project true
```

### 3) Install Dependencies

If your `pyproject.toml` already exists, install dependencies using:

```bash
poetry install
```

If starting from scratch, initialize first and then install:

```bash
poetry init
poetry install
```

To add packages later:

```bash
poetry add <package-name>
```

### 4) Configure Environment Variables

Create a `.env` file, or copy from `.envtemplate`.

Example:

```env
APP_NAME="AI Trading Chatbot API"
APP_DESCRIPTION="API for PDF upload and RAG-based QA"
APP_VERSION="0.1.0"
PORT=8032
```
For every new variable add a variable in app/settings.py 

### How configuration is loaded

- `app/settings.py` uses settings from `.env`
- `app/main.py` uses those settings for application metadata and docs configuration

---

## How to Run the Project

This project expects a launcher file named `run.py`.

Run it using:

```
poetry run python -m app.main
```

After starting the server, open the Swagger docs at:

```text
http://localhost:8032/api/docs/
```

---

## Summary

This repository is not just for one project.  
It is the **general main branch** for multiple **AI-based projects**.

Each branch created from this repository should be treated as:

- an independent project
- AI-focused
- built using the shared setup and standards from the main branch
