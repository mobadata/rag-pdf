from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    openai_api_key: str = ""
    embedding_model: str = "text-embedding-ada-002"
    chat_model: str = "gpt-4o-mini"
    supabase_url: str = ""
    supabase_key: str = ""
    supabase_service_key: str = ""
    chunk_size: int = 1000
    chunk_overlap: int = 150
    search_top_k: int = 5

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
