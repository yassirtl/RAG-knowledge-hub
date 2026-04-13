import logging

import trafilatura
from langchain_core.documents import Document

from app.ingestion.base import BaseLoader
from app.schemas.ingest import SourceType

logger = logging.getLogger(__name__)


class WebLoader(BaseLoader):
    """Scrape a web page and extract its main content using trafilatura."""

    source_type = SourceType.WEB

    def _load(self, source_key: str, **kwargs) -> list[Document]:
        """
        Args:
            source_key: The URL to scrape.
        """
        downloaded = trafilatura.fetch_url(source_key)
        if not downloaded:
            raise ValueError(f"Failed to download content from: {source_key}")

        text = trafilatura.extract(
            downloaded,
            include_comments=False,
            include_tables=True,
            no_fallback=False,
        )
        if not text:
            raise ValueError(f"No extractable text found at: {source_key}")

        logger.info(
            "Extracted %d characters from '%s'.", len(text), source_key[:80]
        )
        return [Document(page_content=text, metadata={"url": source_key})]
