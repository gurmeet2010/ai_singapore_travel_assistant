from langchain_huggingface import HuggingFaceEmbeddings
from app.config import get_settings

def get_embedding_model() -> HuggingFaceEmbeddings:
    settings = get_settings()
    return HuggingFaceEmbeddings(
        model_name= settings.huggingface_embedding_model,
        encode_kwargs={"normalize_embeddings": True},
    )
