from pathlib import Path

from langchain_community.vectorstores import Chroma, FAISS
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings

from backend.app.core.settings import Settings


class VectorStoreFactory:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.embeddings = OpenAIEmbeddings(
            model=settings.embedding_model,
            api_key=settings.openai_api_key,
        )
        Path(settings.vector_db_path).mkdir(parents=True, exist_ok=True)

    def load(self):
        if self.settings.vector_db_provider == "chroma":
            return Chroma(
                collection_name=self.settings.collection_name,
                persist_directory=self.settings.vector_db_path,
                embedding_function=self.embeddings,
            )

        faiss_path = Path(self.settings.vector_db_path) / "faiss_index"
        if not faiss_path.exists():
            raise FileNotFoundError("FAISS index not found. Ingest documents first.")

        return FAISS.load_local(
            folder_path=str(faiss_path),
            embeddings=self.embeddings,
            allow_dangerous_deserialization=True,
        )

    def save(self, store) -> None:
        if self.settings.vector_db_provider == "chroma":
            store.persist()
            return

        faiss_path = Path(self.settings.vector_db_path) / "faiss_index"
        store.save_local(str(faiss_path))

    def add_documents(self, store, docs: list[Document]):
        if not docs:
            return store

        if self.settings.vector_db_provider == "chroma":
            store.add_documents(docs)
            store.persist()
            return store

        store.add_documents(docs)
        self.save(store)
        return store

    def create_faiss(self, docs: list[Document]):
        store = FAISS.from_documents(documents=docs, embedding=self.embeddings)
        self.save(store)
        return store
