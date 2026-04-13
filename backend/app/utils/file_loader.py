from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader, TextLoader, UnstructuredWordDocumentLoader
from langchain_core.documents import Document


SUPPORTED_EXTENSIONS = {".pdf", ".txt", ".md", ".docx"}


def load_document(path: Path) -> list[Document]:
    ext = path.suffix.lower()
    if ext not in SUPPORTED_EXTENSIONS:
        raise ValueError(f"Unsupported file type: {ext}")

    if ext == ".pdf":
        loader = PyPDFLoader(str(path))
    elif ext == ".docx":
        loader = UnstructuredWordDocumentLoader(str(path))
    else:
        loader = TextLoader(str(path), encoding="utf-8")

    return loader.load()
