import logging

from langchain_core.messages import AIMessage, HumanMessage
from langchain_openai import ChatOpenAI

from app.config import get_settings
from app.core.retriever import retrieve
from app.rag.prompts import rag_prompt
from app.schemas.query import ChatMessage, QueryRequest, QueryResponse, SourceReference

logger = logging.getLogger(__name__)


def _build_context(results: list) -> str:
    """Format retrieved documents into a numbered context block."""
    if not results:
        return "No relevant context found."

    parts: list[str] = []
    for i, (doc, _score) in enumerate(results, start=1):
        label = doc.metadata.get("label", "Unknown")
        parts.append(f"[{i}] {label}\n{doc.page_content.strip()}")
    return "\n\n---\n\n".join(parts)


def _convert_history(history: list[ChatMessage]) -> list[HumanMessage | AIMessage]:
    """Convert Pydantic chat history into LangChain message objects."""
    messages: list[HumanMessage | AIMessage] = []
    for msg in history:
        if msg.role == "user":
            messages.append(HumanMessage(content=msg.content))
        else:
            messages.append(AIMessage(content=msg.content))
    return messages


def answer(request: QueryRequest) -> QueryResponse:
    """
    Run the RAG pipeline for a given query request.

    1. Retrieve relevant chunks from the vectorstore.
    2. Build a grounded context string.
    3. Invoke the LLM with the prompt.
    4. Return the answer with cited sources.
    """
    settings = get_settings()

    results = retrieve(request.question, source_ids=request.source_ids)
    context = _build_context(results)

    llm = ChatOpenAI(
        model=settings.openai_chat_model,
        temperature=0.2,
        openai_api_key=settings.openai_api_key,
    )
    chain = rag_prompt | llm

    response = chain.invoke(
        {
            "context": context,
            "history": _convert_history(request.history),
            "question": request.question,
        }
    )

    seen_source_ids: set[str] = set()
    sources: list[SourceReference] = []
    for doc, score in results:
        sid = doc.metadata.get("source_id", "")
        if sid in seen_source_ids:
            continue
        seen_source_ids.add(sid)
        sources.append(
            SourceReference(
                source_id=sid,
                label=doc.metadata.get("label", "Unknown"),
                source_type=doc.metadata.get("source_type", ""),
                excerpt=doc.page_content[:300].strip(),
                score=round(score, 4),
            )
        )

    logger.info(
        "Answered query with %d source(s). Model: %s",
        len(sources),
        settings.openai_chat_model,
    )

    return QueryResponse(answer=response.content, sources=sources)
