import logging
from typing import Any

from langchain_core.documents import Document

from app.config import get_settings
from app.core.vectorstore import get_vectorstore

logger = logging.getLogger(__name__)


def build_retriever_filter(source_ids: list[str] | None) -> dict[str, Any] | None:
    """Build a ChromaDB metadata filter for the given source IDs."""
    if not source_ids:
        return None
    if len(source_ids) == 1:
        return {"source_id": source_ids[0]}
    return {"source_id": {"$in": source_ids}}


def retrieve(
    query: str,
    source_ids: list[str] | None = None,
) -> list[tuple[Document, float]]:
    """
    Perform a similarity search with relevance scores.

    Returns a list of (Document, score) tuples sorted by descending score,
    filtered to results above the configured score threshold.
    """
    settings = get_settings()
    vectorstore = get_vectorstore()
    search_kwargs: dict[str, Any] = {"k": settings.top_k}

    where_filter = build_retriever_filter(source_ids)
    if where_filter:
        search_kwargs["filter"] = where_filter

    results: list[tuple[Document, float]] = (
        vectorstore.similarity_search_with_relevance_scores(query, **search_kwargs)
    )

    filtered = [
        (doc, score)
        for doc, score in results
        if score >= settings.score_threshold
    ]

    logger.debug(
        "Retrieved %d/%d chunks above threshold %.2f for query: %.80s",
        len(filtered),
        len(results),
        settings.score_threshold,
        query,
    )
    return filtered
