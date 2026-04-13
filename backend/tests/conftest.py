import os
import tempfile
from collections.abc import Generator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

os.environ.setdefault("OPENAI_API_KEY", "sk-test-key")
os.environ.setdefault("CHROMA_PERSIST_DIR", tempfile.mkdtemp())
os.environ.setdefault("UPLOAD_DIR", tempfile.mkdtemp())


@pytest.fixture(scope="session")
def sample_pdf_path() -> Generator[Path, None, None]:
    """Create a minimal single-page PDF for testing."""
    try:
        import fpdf  # type: ignore

        pdf = fpdf.FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Knowledge Hub test document.", ln=True)
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
            tmp = Path(f.name)
        pdf.output(str(tmp))
        yield tmp
        tmp.unlink(missing_ok=True)
    except ImportError:
        pytest.skip("fpdf not installed; skipping PDF fixture.")


@pytest.fixture(scope="session")
def sample_md_path() -> Generator[Path, None, None]:
    with tempfile.NamedTemporaryFile(
        suffix=".md", mode="w", delete=False, encoding="utf-8"
    ) as f:
        f.write("# Test Document\n\nThis is a test markdown document.\n")
        tmp = Path(f.name)
    yield tmp
    tmp.unlink(missing_ok=True)


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    from app.main import app

    with TestClient(app) as c:
        yield c
