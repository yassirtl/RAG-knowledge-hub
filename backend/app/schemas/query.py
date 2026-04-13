from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    role: str = Field(..., pattern="^(user|assistant)$")
    content: str


class QueryRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=2000)
    history: list[ChatMessage] = Field(
        default_factory=list,
        description="Conversation history for multi-turn context",
    )
    source_ids: list[str] | None = Field(
        None,
        description="Restrict retrieval to specific source IDs. None means all sources.",
    )


class SourceReference(BaseModel):
    source_id: str
    label: str
    source_type: str
    excerpt: str = Field(..., description="Relevant excerpt from this source")
    score: float = Field(..., description="Relevance score [0, 1]")


class QueryResponse(BaseModel):
    answer: str
    sources: list[SourceReference] = Field(
        default_factory=list,
        description="Sources used to generate the answer",
    )
