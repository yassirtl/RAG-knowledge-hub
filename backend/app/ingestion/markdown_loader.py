import logging
from pathlib import Path

from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_core.documents import Document

from app.ingestion.base import BaseLoader
from app.schemas.ingest import SourceType

logger = logging.getLogger(__name__)


class MarkdownLoader(BaseLoader):
    """Load and chunk Markdown / plain-text files."""

    source_type = SourceType.MARKDOWN

    def _load(self, source_key: str, **kwargs) -> list[Document]:
        path = Path(source_key)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")

        if path.suffix.lower() in {".md", ".mdx"}:
            loader = UnstructuredMarkdownLoader(str(path), mode="single")
            docs = loader.load()
        else:
            text = path.read_text(encoding="utf-8")
            docs = [Document(page_content=text, metadata={"filename": path.name})]

        logger.info("Loaded '%s' (%d doc(s)).", path.name, len(docs))
        return docs
