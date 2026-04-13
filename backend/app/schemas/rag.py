from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str = "ok"
    service: str


class QueryRequest(BaseModel):
    question: str = Field(..., min_length=2, max_length=3000)


class SourceChunk(BaseModel):
    content: str
    metadata: dict


class QueryResponse(BaseModel):
    answer: str
    sources: list[SourceChunk]


class IngestResponse(BaseModel):
    files_processed: int
    chunks_indexed: int
    vector_store: str
