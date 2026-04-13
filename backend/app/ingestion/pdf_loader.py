import logging
from pathlib import Path

from langchain_community.document_loaders import PyMuPDFLoader
from langchain_core.documents import Document

from app.ingestion.base import BaseLoader
from app.schemas.ingest import SourceType

logger = logging.getLogger(__name__)


class PDFLoader(BaseLoader):
    """Load and chunk PDF files using PyMuPDF."""

    source_type = SourceType.PDF

    def _load(self, source_key: str, **kwargs) -> list[Document]:
        path = Path(source_key)
        if not path.exists():
            raise FileNotFoundError(f"PDF not found: {path}")

        loader = PyMuPDFLoader(str(path))
        docs = loader.load()

        for doc in docs:
            doc.metadata["page"] = doc.metadata.get("page", 0) + 1

        logger.info("Loaded %d pages from '%s'.", len(docs), path.name)
        return docs
