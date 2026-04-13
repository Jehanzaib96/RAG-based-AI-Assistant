from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from backend.app.core.settings import get_settings
from backend.app.dependencies import get_ingestion_service, get_retrieval_service
from backend.app.schemas.rag import IngestResponse, QueryRequest, QueryResponse, SourceChunk
from backend.app.services.ingestion import IngestionService
from backend.app.services.retrieval import RetrievalService

router = APIRouter(tags=["rag"])


@router.post("/ingest", response_model=IngestResponse)
async def ingest_documents(
    files: list[UploadFile] = File(...),
    ingestion_service: IngestionService = Depends(get_ingestion_service),
) -> IngestResponse:
    settings = get_settings()
    upload_dir = Path(settings.upload_dir)
    upload_dir.mkdir(parents=True, exist_ok=True)

    saved_paths: list[Path] = []
    for uploaded_file in files:
        target_path = upload_dir / uploaded_file.filename
        content = await uploaded_file.read()
        target_path.write_bytes(content)
        saved_paths.append(target_path)

    try:
        files_processed, chunks_indexed = ingestion_service.ingest(saved_paths)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return IngestResponse(
        files_processed=files_processed,
        chunks_indexed=chunks_indexed,
        vector_store=settings.vector_db_provider,
    )


@router.post("/query", response_model=QueryResponse)
def query_documents(
    request: QueryRequest,
    retrieval_service: RetrievalService = Depends(get_retrieval_service),
) -> QueryResponse:
    try:
        answer, source_docs = retrieval_service.ask(request.question)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    sources = [
        SourceChunk(content=doc.page_content[:1200], metadata=doc.metadata or {}) for doc in source_docs
    ]
    return QueryResponse(answer=answer, sources=sources)
