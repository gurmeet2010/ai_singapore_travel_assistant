from langchain_chroma import Chroma
from langchain_core.documents import Document

from app.config import get_settings
from app.rag.embeddings import get_embedding_model


COLLECTION_NAME = "singapore_travel"


def create_vector_store(documents: list[Document]) -> Chroma:
    settings = get_settings()
    return Chroma.from_documents(
        documents=documents,
        embedding=get_embedding_model(),
        collection_name=COLLECTION_NAME,
        persist_directory=settings.chroma_persist_directory,
    )


def get_vector_store() -> Chroma:
    settings = get_settings()
    return Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=get_embedding_model(),
        persist_directory=settings.chroma_persist_directory,
    )
