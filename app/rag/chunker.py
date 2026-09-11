from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_documents(documents: list[Document]) -> list[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1200,
        chunk_overlap=200,
        separators=["\n## ", "\n### ", "\n\n", "\n", " ", ""],
    )
    return splitter.split_documents(documents)
