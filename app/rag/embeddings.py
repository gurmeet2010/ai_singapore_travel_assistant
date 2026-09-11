#from langchain_openai import OpenAIEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings

from app.config import get_settings


# def get_embedding_model() -> OpenAIEmbeddings:
#     settings = get_settings()
#     return OpenAIEmbeddings(
#         model=settings.openai_embedding_model,
#         api_key=settings.openai_api_key,
#     )

def get_embedding_model() -> HuggingFaceEmbeddings:
    settings = get_settings()
    return HuggingFaceEmbeddings(
        model_name= settings.huggingface_embedding_model,
        encode_kwargs={"normalize_embeddings": True},
    )
