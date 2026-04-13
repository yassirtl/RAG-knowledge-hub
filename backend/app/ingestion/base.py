import hashlib
import uuid
from abc import ABC, abstractmethod

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.config import get_settings
from app.schemas.ingest import SourceType


def generate_source_id(content_key: str) -> str:
    """Derive a deterministic source ID from a content key (e.g. URL or filename)."""
    digest = hashlib.sha256(content_key.encode()).hexdigest()[:16]
    return str(uuid.UUID(hex=digest.ljust(32, "0")))


def build_splitter() -> RecursiveCharacterTextSplitter:
    settings = get_settings()
    return RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""],
    )


class BaseLoader(ABC):
    """Abstract base class for all document loaders."""

    source_type: SourceType

    def load_and_split(
        self,
        source_key: str,
        label: str,
        **kwargs,
    ) -> tuple[str, list[Document]]:
        """
        Load a source, split it into chunks, and attach metadata.

        Returns:
            (source_id, list[Document])
        """
        raw_docs = self._load(source_key, **kwargs)
        splitter = build_splitter()
        chunks = splitter.split_documents(raw_docs)

        source_id = generate_source_id(source_key)
        for chunk in chunks:
            chunk.metadata.update(
                {
                    "source_id": source_id,
                    "source_type": self.source_type.value,
                    "label": label,
                }
            )

        return source_id, chunks

    @abstractmethod
    def _load(self, source_key: str, **kwargs) -> list[Document]:
        """Load raw documents from the given source key."""
