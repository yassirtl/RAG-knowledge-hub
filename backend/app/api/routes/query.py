import logging

from fastapi import APIRouter, HTTPException, status

from app.rag.chain import answer
from app.schemas.query import QueryRequest, QueryResponse

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/query", tags=["Query"])


@router.post("/", response_model=QueryResponse)
async def query_knowledge_base(payload: QueryRequest) -> QueryResponse:
    """
    Answer a question using the knowledge base via RAG.

    Optionally restrict retrieval to a subset of source IDs.
    """
    try:
        return answer(payload)
    except Exception as exc:
        logger.exception("Query failed: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while processing your query.",
        ) from exc
