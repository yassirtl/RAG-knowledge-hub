from unittest.mock import MagicMock, patch

import pytest
from langchain_core.documents import Document
from langchain_core.messages import AIMessage

from app.rag.chain import _build_context, _convert_history, answer
from app.schemas.query import ChatMessage, QueryRequest


class TestBuildContext:
    def test_empty_results(self):
        assert _build_context([]) == "No relevant context found."

    def test_single_result(self):
        doc = Document(
            page_content="This is the content.",
            metadata={"label": "My Source"},
        )
        ctx = _build_context([(doc, 0.9)])
        assert "[1] My Source" in ctx
        assert "This is the content." in ctx

    def test_multiple_results_are_separated(self):
        docs = [
            (Document(page_content=f"Content {i}", metadata={"label": f"S{i}"}), 0.8)
            for i in range(3)
        ]
        ctx = _build_context(docs)
        assert ctx.count("---") == 2


class TestConvertHistory:
    def test_empty_history(self):
        assert _convert_history([]) == []

    def test_converts_roles(self):
        from langchain_core.messages import AIMessage, HumanMessage

        history = [
            ChatMessage(role="user", content="Hello"),
            ChatMessage(role="assistant", content="Hi there"),
        ]
        result = _convert_history(history)
        assert isinstance(result[0], HumanMessage)
        assert isinstance(result[1], AIMessage)


class TestAnswer:
    @patch("app.rag.chain.retrieve")
    @patch("app.rag.chain.ChatOpenAI")
    def test_returns_query_response(self, mock_llm_cls, mock_retrieve):
        doc = Document(
            page_content="Paris is the capital of France.",
            metadata={
                "source_id": "abc123",
                "label": "Geography",
                "source_type": "pdf",
            },
        )
        mock_retrieve.return_value = [(doc, 0.95)]

        mock_chain_response = MagicMock()
        mock_chain_response.content = "Paris is the capital of France."
        mock_llm_instance = MagicMock()
        mock_llm_cls.return_value = mock_llm_instance
        mock_llm_instance.__or__ = MagicMock(return_value=MagicMock())

        with patch("app.rag.chain.rag_prompt") as mock_prompt:
            mock_full_chain = MagicMock()
            mock_full_chain.invoke.return_value = mock_chain_response
            mock_prompt.__or__ = MagicMock(return_value=mock_full_chain)

            request = QueryRequest(question="What is the capital of France?")
            response = answer(request)

        assert response.answer == "Paris is the capital of France."
        assert len(response.sources) == 1
        assert response.sources[0].source_id == "abc123"

    @patch("app.rag.chain.retrieve")
    @patch("app.rag.chain.ChatOpenAI")
    def test_deduplicates_sources(self, mock_llm_cls, mock_retrieve):
        doc = Document(
            page_content="Repeated chunk.",
            metadata={"source_id": "same-id", "label": "Doc", "source_type": "web"},
        )
        mock_retrieve.return_value = [(doc, 0.9), (doc, 0.85)]

        mock_chain_response = MagicMock()
        mock_chain_response.content = "Answer."
        mock_llm_instance = MagicMock()
        mock_llm_cls.return_value = mock_llm_instance

        with patch("app.rag.chain.rag_prompt") as mock_prompt:
            mock_full_chain = MagicMock()
            mock_full_chain.invoke.return_value = mock_chain_response
            mock_prompt.__or__ = MagicMock(return_value=mock_full_chain)

            request = QueryRequest(question="Test?")
            response = answer(request)

        assert len(response.sources) == 1
