from pathlib import Path

from langchain_text_splitters import RecursiveCharacterTextSplitter

from backend.app.core.settings import Settings
from backend.app.db.vector_store import VectorStoreFactory
from backend.app.utils.file_loader import load_document


class IngestionService:
    def __init__(self, settings: Settings, vector_factory: VectorStoreFactory) -> None:
        self.settings = settings
        self.vector_factory = vector_factory
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.max_chunk_size,
            chunk_overlap=settings.chunk_overlap,
        )

    def ingest(self, file_paths: list[Path]) -> tuple[int, int]:
        all_chunks = []
        files_processed = 0

        for path in file_paths:
            docs = load_document(path)
            chunks = self.splitter.split_documents(docs)
            all_chunks.extend(chunks)
            files_processed += 1

        if not all_chunks:
            return files_processed, 0

        if self.settings.vector_db_provider == "faiss":
            try:
                store = self.vector_factory.load()
                self.vector_factory.add_documents(store, all_chunks)
            except FileNotFoundError:
                self.vector_factory.create_faiss(all_chunks)
            return files_processed, len(all_chunks)

        store = self.vector_factory.load()
        self.vector_factory.add_documents(store, all_chunks)
        return files_processed, len(all_chunks)
