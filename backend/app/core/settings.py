from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = Field(default="RAG-based AI Assistant", alias="APP_NAME")
    app_env: Literal["dev", "staging", "prod"] = Field(default="dev", alias="APP_ENV")
    app_host: str = Field(default="0.0.0.0", alias="APP_HOST")
    app_port: int = Field(default=8000, alias="APP_PORT")
    app_cors_origins: str = Field(default="http://localhost:8501", alias="APP_CORS_ORIGINS")

    openai_api_key: str = Field(default="", alias="OPENAI_API_KEY")
    openai_model: str = Field(default="gpt-4o-mini", alias="OPENAI_MODEL")
    openai_temperature: float = Field(default=0.1, alias="OPENAI_TEMPERATURE")

    vector_db_provider: Literal["faiss", "chroma"] = Field(
        default="chroma", alias="VECTOR_DB_PROVIDER"
    )
    vector_db_path: str = Field(default="./data/vector_store", alias="VECTOR_DB_PATH")
    collection_name: str = Field(default="rag_docs", alias="COLLECTION_NAME")

    embedding_model: str = Field(default="text-embedding-3-small", alias="EMBEDDING_MODEL")
    top_k: int = Field(default=4, alias="TOP_K")
    max_chunk_size: int = Field(default=1200, alias="MAX_CHUNK_SIZE")
    chunk_overlap: int = Field(default=150, alias="CHUNK_OVERLAP")

    upload_dir: str = Field(default="./data/uploads", alias="UPLOAD_DIR")

    @property
    def cors_origins(self) -> list[str]:
        return [origin.strip() for origin in self.app_cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
