from functools import lru_cache

from backend.app.core.settings import Settings, get_settings
from backend.app.db.vector_store import VectorStoreFactory
from backend.app.services.ingestion import IngestionService
from backend.app.services.retrieval import RetrievalService


@lru_cache
def get_vector_factory() -> VectorStoreFactory:
    settings: Settings = get_settings()
    return VectorStoreFactory(settings)


@lru_cache
def get_ingestion_service() -> IngestionService:
    settings: Settings = get_settings()
    return IngestionService(settings=settings, vector_factory=get_vector_factory())


@lru_cache
def get_retrieval_service() -> RetrievalService:
    settings: Settings = get_settings()
    return RetrievalService(settings=settings, vector_factory=get_vector_factory())
