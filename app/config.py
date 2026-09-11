from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AI Travel Planning Assistant"
    app_env: str = "development"

    # LLM model:- OpenAI
    #openai_api_key: str
    #openai_chat_model: str = "gpt-4o-mini"
    #openai_embedding_model: str = "text-embedding-3-small"

    ## LLM model:- GenAI
    
    gemini_api_key:str="gemini_key"
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