# Architecture Notes

## Modules

- `api`: thin controllers, validation, transport concerns.
- `services`: business logic for ingestion and question answering.
- `db`: vector store implementation abstraction.
- `schemas`: pydantic request/response contracts.
- `core`: configuration and cross-cutting concerns.

## Request flow

1. Files are uploaded via `/api/v1/ingest`.
2. Files are persisted to `UPLOAD_DIR`.
3. Documents are loaded, chunked, and embedded.
4. Chunks are saved to configured vector DB.
5. Query route retrieves top-k chunks and prompts LLM.
6. Answer + source chunks are returned to UI.
