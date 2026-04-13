from enum import StrEnum

from pydantic import BaseModel, Field, HttpUrl


class SourceType(StrEnum):
    PDF = "pdf"
    WEB = "web"
    MARKDOWN = "markdown"


class IngestUrlRequest(BaseModel):
    url: HttpUrl = Field(..., description="Web page URL to ingest")
    source_label: str | None = Field(
        None, description="Optional human-readable label for this source"
    )


class IngestResponse(BaseModel):
    source_id: str = Field(..., description="Unique identifier for the ingested source")
    source_type: SourceType
    chunk_count: int = Field(..., description="Number of chunks stored in the vector DB")
    label: str = Field(..., description="Display label for the source")


class DeleteSourceRequest(BaseModel):
    source_id: str = Field(..., description="ID of the source to delete")


class SourceInfo(BaseModel):
    source_id: str
    source_type: SourceType
    label: str
    chunk_count: int
