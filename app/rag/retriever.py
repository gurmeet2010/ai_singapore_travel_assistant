from langchain_core.documents import Document

from app.config import get_settings
from app.rag.vectorstore import get_vector_store


def retrieve_documents(query: str) -> list[Document]:
    settings = get_settings()
    vector_store = get_vector_store()
    return vector_store.similarity_search(query, k=settings.top_k)
