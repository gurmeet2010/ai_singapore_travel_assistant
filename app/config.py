from functools import lru_cache
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict
import os

# Load variables from .env
load_dotenv()

class Settings(BaseSettings):
    app_name: str = os.getenv("APP_NAME", "")
    app_env: str = os.getenv("APP_ENV", "")

    ## LLM model:- GenAI
    gemini_api_key:str= os.getenv("GEMINI_API_KEY", "")
    gemini_chat_model:str="gemini-3.7-flash"
    

    # LLM model :- HuggingFace embedding model
    huggingface_embedding_model:str = "sentence-transformers/all-mpnet-base-v2"

    chroma_persist_directory: str = "./chroma_db"

    top_k: int = 5
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )





@lru_cache
def get_settings() -> Settings:
    return Settings()