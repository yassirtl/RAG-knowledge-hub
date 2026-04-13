import logging
import shutil
import uuid
from pathlib import Path

from fastapi import APIRouter, File, Form, HTTPException, UploadFile, status

from app.api.deps import SettingsDep
from app.core.vectorstore import add_documents, delete_by_source_id, get_chunk_count_by_source
from app.ingestion.markdown_loader import MarkdownLoader
from app.ingestion.pdf_loader import PDFLoader
from app.ingestion.web_loader import WebLoader
from app.schemas.ingest import DeleteSourceRequest, IngestResponse, IngestUrlRequest, SourceType

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/ingest", tags=["Ingestion"])


@router.post("/pdf", response_model=IngestResponse, status_code=status.HTTP_201_CREATED)
async def ingest_pdf(
    settings: SettingsDep,
    file: UploadFile = File(..., description="PDF file to ingest"),
    label: str | None = Form(None, description="Human-readable label"),
) -> IngestResponse:
    """Upload and ingest a PDF file into the knowledge base."""
    if file.content_type not in {"application/pdf", "application/octet-stream"}:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Only PDF files are supported.",
        )

    content = await file.read()
    max_bytes = settings.max_pdf_size_mb * 1024 * 1024
    if len(content) > max_bytes:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File exceeds the {settings.max_pdf_size_mb} MB limit.",
        )

    tmp_path = settings.upload_dir / f"{uuid.uuid4()}.pdf"
    try:
        tmp_path.write_bytes(content)
        display_label = label or Path(file.filename or "document.pdf").stem
        loader = PDFLoader()
        source_id, chunks = loader.load_and_split(str(tmp_path), label=display_label)
        add_documents(chunks)
    except Exception as exc:
        logger.exception("PDF ingestion failed: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        ) from exc
    finally:
        tmp_path.unlink(missing_ok=True)

    return IngestResponse(
        source_id=source_id,
        source_type=SourceType.PDF,
        chunk_count=len(chunks),
        label=display_label,
    )


@router.post("/url", response_model=IngestResponse, status_code=status.HTTP_201_CREATED)
async def ingest_url(payload: IngestUrlRequest) -> IngestResponse:
    """Scrape a web page and ingest its content into the knowledge base."""
    url_str = str(payload.url)
    display_label = payload.source_label or url_str

    try:
        loader = WebLoader()
        source_id, chunks = loader.load_and_split(url_str, label=display_label)
        add_documents(chunks)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)
        ) from exc
    except Exception as exc:
        logger.exception("Web ingestion failed: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc)
        ) from exc

    return IngestResponse(
        source_id=source_id,
        source_type=SourceType.WEB,
        chunk_count=len(chunks),
        label=display_label,
    )


@router.post(
    "/file",
    response_model=IngestResponse,
    status_code=status.HTTP_201_CREATED,
)
async def ingest_markdown(
    settings: SettingsDep,
    file: UploadFile = File(..., description="Markdown or plain-text file"),
    label: str | None = Form(None),
) -> IngestResponse:
    """Upload and ingest a Markdown or plain-text file."""
    allowed_types = {
        "text/markdown",
        "text/plain",
        "application/octet-stream",
    }
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Only Markdown and plain-text files are supported.",
        )

    suffix = Path(file.filename or "doc.md").suffix or ".md"
    tmp_path = settings.upload_dir / f"{uuid.uuid4()}{suffix}"
    try:
        content = await file.read()
        tmp_path.write_bytes(content)
        display_label = label or Path(file.filename or "document").stem
        loader = MarkdownLoader()
        source_id, chunks = loader.load_and_split(str(tmp_path), label=display_label)
        add_documents(chunks)
    except Exception as exc:
        logger.exception("Markdown ingestion failed: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc)
        ) from exc
    finally:
        tmp_path.unlink(missing_ok=True)

    return IngestResponse(
        source_id=source_id,
        source_type=SourceType.MARKDOWN,
        chunk_count=len(chunks),
        label=display_label,
    )


@router.delete("/source", status_code=status.HTTP_204_NO_CONTENT)
async def delete_source(payload: DeleteSourceRequest) -> None:
    """Remove all chunks for a given source from the knowledge base."""
    try:
        delete_by_source_id(payload.source_id)
    except Exception as exc:
        logger.exception("Source deletion failed: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc)
        ) from exc


@router.get("/source/{source_id}/chunks", response_model=dict)
async def get_source_chunks(source_id: str) -> dict:
    """Return the number of stored chunks for a given source."""
    count = get_chunk_count_by_source(source_id)
    return {"source_id": source_id, "chunk_count": count}
