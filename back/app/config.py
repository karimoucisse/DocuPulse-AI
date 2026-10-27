from functools import lru_cache
from pathlib import Path

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    chunk_size: int = Field(default=500, ge=100, le=800)
    chunk_overlap: int = Field(default=100, ge=0)
    top_k: int = Field(default=3, ge=1)
    temperature: float = Field(default=0.0, ge=0.0, le=1.0)
    embedding_model: str = Field(default="nomic-embed-text")
    chat_model: str = "llama3.2:3b"
    vector_store_name: str = "rag_collection"
    vector_store_path: Path = "data/rag_chroma_db"
    cors_origins: list[str] = ["http://localhost:3000"]

    model_config = SettingsConfigDict(env_file=".env", env_prefix="RAG_")

    @model_validator(mode="after")
    def check_overlap_lt_chunk_size(self) -> "Settings":
        if self.chunk_overlap >= self.chunk_size:
            raise ValueError(
                f"chunk_overlap ({self.chunk_overlap}) has to be "
                f"lower than chunk_size ({self.chunk_size})"
            )
        return self


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    return settings
