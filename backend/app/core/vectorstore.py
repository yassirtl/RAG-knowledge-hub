import logging
from functools import lru_cache

import chromadb
from chromadb.config import Settings as ChromaSettings
from langchain_chroma import Chroma
from langchain_core.documents import Document

from app.config import get_settings
from app.core.embeddings import get_embeddings

logger = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def get_chroma_client() -> chromadb.PersistentClient:
    """Return a cached persistent ChromaDB client."""
    settings = get_settings()
    return chromadb.PersistentClient(
        path=str(settings.chroma_persist_dir),
        settings=ChromaSettings(anonymized_telemetry=False),
    )


@lru_cache(maxsize=1)
def get_vectorstore() -> Chroma:
    """Return a cached LangChain Chroma vectorstore."""
    settings = get_settings()
    return Chroma(
        client=get_chroma_client(),
        collection_name=settings.chroma_collection_name,
        embedding_function=get_embeddings(),
    )


def add_documents(documents: list[Document]) -> list[str]:
    """Upsert documents into the vectorstore and return their IDs."""
    vectorstore = get_vectorstore()
    ids = vectorstore.add_documents(documents)
    logger.info("Added %d chunks to the vectorstore.", len(ids))
    return ids


def delete_by_source_id(source_id: str) -> None:
    """Remove all chunks associated with a given source ID."""
    vectorstore = get_vectorstore()
    vectorstore.delete(where={"source_id": source_id})
    logger.info("Deleted all chunks for source_id=%s.", source_id)


def get_chunk_count_by_source(source_id: str) -> int:
    """Return the number of stored chunks for a given source."""
    client = get_chroma_client()
    settings = get_settings()
    collection = client.get_collection(settings.chroma_collection_name)
    result = collection.get(where={"source_id": source_id}, include=[])
    return len(result["ids"])
