import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from langchain_core.documents import Document

from app.ingestion.base import generate_source_id
from app.ingestion.markdown_loader import MarkdownLoader
from app.ingestion.web_loader import WebLoader


class TestGenerateSourceId:
    def test_deterministic(self):
        assert generate_source_id("foo") == generate_source_id("foo")

    def test_different_keys_produce_different_ids(self):
        assert generate_source_id("foo") != generate_source_id("bar")

    def test_returns_valid_uuid_string(self):
        import uuid

        result = generate_source_id("https://example.com")
        uuid.UUID(result)


class TestMarkdownLoader:
    def test_load_markdown_file(self):
        with tempfile.NamedTemporaryFile(
            suffix=".md", mode="w", delete=False, encoding="utf-8"
        ) as f:
            f.write("# Hello\n\nThis is content.\n")
            path = Path(f.name)

        try:
            loader = MarkdownLoader()
            source_id, chunks = loader.load_and_split(str(path), label="test")
            assert isinstance(source_id, str)
            assert len(chunks) > 0
            assert all(c.metadata["source_type"] == "markdown" for c in chunks)
            assert all(c.metadata["label"] == "test" for c in chunks)
        finally:
            path.unlink(missing_ok=True)

    def test_raises_on_missing_file(self):
        loader = MarkdownLoader()
        with pytest.raises(FileNotFoundError):
            loader.load_and_split("/nonexistent/path.md", label="x")

    def test_plain_text_file(self):
        with tempfile.NamedTemporaryFile(
            suffix=".txt", mode="w", delete=False, encoding="utf-8"
        ) as f:
            f.write("Plain text content for testing.\n")
            path = Path(f.name)

        try:
            loader = MarkdownLoader()
            source_id, chunks = loader.load_and_split(str(path), label="plain")
            assert len(chunks) > 0
        finally:
            path.unlink(missing_ok=True)


class TestWebLoader:
    @patch("app.ingestion.web_loader.trafilatura.fetch_url")
    @patch("app.ingestion.web_loader.trafilatura.extract")
    def test_successful_extraction(self, mock_extract, mock_fetch):
        mock_fetch.return_value = "<html><body>content</body></html>"
        mock_extract.return_value = "Extracted page content for testing purposes."

        loader = WebLoader()
        source_id, chunks = loader.load_and_split(
            "https://example.com", label="Example"
        )

        assert isinstance(source_id, str)
        assert len(chunks) > 0
        assert all(c.metadata["source_type"] == "web" for c in chunks)

    @patch("app.ingestion.web_loader.trafilatura.fetch_url")
    def test_raises_on_failed_download(self, mock_fetch):
        mock_fetch.return_value = None
        loader = WebLoader()
        with pytest.raises(ValueError, match="Failed to download"):
            loader.load_and_split("https://example.com", label="x")

    @patch("app.ingestion.web_loader.trafilatura.fetch_url")
    @patch("app.ingestion.web_loader.trafilatura.extract")
    def test_raises_on_empty_extraction(self, mock_extract, mock_fetch):
        mock_fetch.return_value = "<html></html>"
        mock_extract.return_value = None
        loader = WebLoader()
        with pytest.raises(ValueError, match="No extractable text"):
            loader.load_and_split("https://example.com", label="x")
