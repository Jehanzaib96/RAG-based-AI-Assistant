# RAG-based AI Assistant

A production-oriented, modular Retrieval-Augmented Generation (RAG) assistant built with:

- **FastAPI** for backend APIs
- **Streamlit** for user interface
- **LangChain + OpenAI** for orchestration and generation
- **FAISS or Chroma** for vector search

## Architecture

```text
RAG-based-AI-Assistant/
├── backend/
│   └── app/
│       ├── api/v1/endpoints/      # HTTP route handlers
│       ├── core/                  # settings and logging
│       ├── db/                    # vector db adapters
│       ├── schemas/               # request/response models
│       ├── services/              # ingestion + retrieval logic
│       ├── utils/                 # file helpers
│       ├── dependencies.py        # DI container points
│       └── main.py                # FastAPI app entrypoint
├── frontend/
│   └── streamlit_app.py           # Streamlit UI
├── data/
│   ├── uploads/                   # uploaded source docs
│   └── vector_store/              # persisted vectors
├── tests/
└── .env.example
```

## Key Features

- Upload and index **PDF/TXT/MD/DOCX** documents
- Ask questions over indexed data
- Switch vector backend via config: `faiss` or `chroma`
- Clean module boundaries (API, Services, DB adapters, Schemas)
- Health endpoint and typed API contracts

## Quick Start

### 1) Install dependencies

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

### 2) Configure environment

```bash
cp .env.example .env
```

Set your `OPENAI_API_KEY` in `.env`.

### 3) Run backend

```bash
uvicorn backend.app.main:app --reload --port 8000
```

### 4) Run frontend

```bash
streamlit run frontend/streamlit_app.py
```

## API Summary

- `GET /api/v1/health` → service status
- `POST /api/v1/ingest` → upload files and index
- `POST /api/v1/query` → ask question against indexed docs

## Production Notes

- Configure CORS origins in `APP_CORS_ORIGINS`
- Persist vector store in mounted durable storage
- Use a process manager for API (e.g., Gunicorn/Uvicorn workers)
- Add tracing/metrics (OpenTelemetry, Prometheus) as needed
- Consider async queue for heavy ingestion workloads
