from app.rag.chunker import split_documents
from app.rag.loader import load_markdown_documents
from app.rag.vectorstore import create_vector_store


def ingest() -> None:
    documents = load_markdown_documents()
    print(f"Loaded {len(documents)} source documents.")

    chunks = split_documents(documents)
    print(f"Created {len(chunks)} chunks.")

    create_vector_store(chunks)
    print("Knowledge base successfully stored in Chroma.")


if __name__ == "__main__":
    ingest()
