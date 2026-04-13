from functools import lru_cache
from pathlib import Path

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ── LLM ──────────────────────────────────────────────────────────────────
    openai_api_key: str = Field(..., description="OpenAI API key")
    openai_chat_model: str = Field("gpt-4o-mini", description="Chat completion model")
    openai_embedding_model: str = Field(
        "text-embedding-3-small", description="Embedding model"
    )

    # ── Vector Store ──────────────────────────────────────────────────────────
    chroma_persist_dir: Path = Field(
        Path("./chroma_db"), description="ChromaDB persistence directory"
    )
    chroma_collection_name: str = Field(
        "knowledge_hub", description="ChromaDB collection name"
    )

    # ── Ingestion ─────────────────────────────────────────────────────────────
    chunk_size: int = Field(512, ge=64, le=4096)
    chunk_overlap: int = Field(64, ge=0, le=512)
    max_pdf_size_mb: int = Field(20, ge=1, le=100)
    upload_dir: Path = Field(Path("./uploads"), description="Temporary upload directory")

    # ── Retrieval ─────────────────────────────────────────────────────────────
    top_k: int = Field(5, ge=1, le=20)
    score_threshold: float = Field(0.35, ge=0.0, le=1.0)

    # ── API ───────────────────────────────────────────────────────────────────
    api_host: str = Field("0.0.0.0")
    api_port: int = Field(8000)
    cors_origins: list[str] = Field(
        default=["http://localhost:5173", "http://localhost:3000"]
    )
    log_level: str = Field("INFO")

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, v: str | list[str]) -> list[str]:
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v

    @field_validator("chroma_persist_dir", "upload_dir", mode="after")
    @classmethod
    def create_dirs(cls, v: Path) -> Path:
        v.mkdir(parents=True, exist_ok=True)
        return v


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
