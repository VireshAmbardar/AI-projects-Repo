# Smart_Diagnosis_API_with_AI_Integration

**Smart Diagnosis API with AI Integration** is a backend system designed to analyze user-provided symptoms and generate possible medical conditions along with actionable recommendations. The system combines structured backend development practices with AI capabilities to deliver meaningful, consistent, and user-friendly diagnostic insights.

The API exposes a `/diagnose` endpoint that accepts symptom input and returns 2–3 probable conditions, each accompanied by a probability score and suggested next steps such as recommended medical tests or specialist consultations. AI integration is used to enhance the quality, clarity, and consistency of responses, either through external AI APIs or a hybrid rule-based approach.

Additionally, the system includes a history tracking feature powered by MongoDB, enabling storage and retrieval of past diagnosis requests via a `/history` endpoint. This ensures traceability and supports future enhancements such as analytics or personalization.

The project follows a clean and modular backend architecture, including proper separation of routes, controllers, and models, along with basic error handling and scalability considerations. It is designed to simulate a real-world production-ready service with optional deployment support.

---

## Purpose of this Repository

This main branch is intended to:

- serve as a **base branch** for multiple AI projects
- keep a common development structure
- allow each branch to become an independent AI project
- provide a reusable setup for future AI-based applications

> **Main branch = common base**  
> **Each branch = its own AI project**

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
