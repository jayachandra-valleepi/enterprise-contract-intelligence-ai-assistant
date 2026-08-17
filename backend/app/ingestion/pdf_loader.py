from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from backend.app.ingestion.pymupdf_extractor import (
    PyMuPDFExtractor,
)
from backend.app.ingestion.textract_extractor import (
    TextractExtractor,
)


@dataclass(frozen=True)
class ExtractedDocument:
    """
    Result of PDF text extraction.
    """

    text: str
    extraction_method: str
    page_count: int


class PDFLoader:
    """
    Loads text from PDFs.

    Strategy:

    1. Try PyMuPDF.
    2. If extracted text is insufficient, use Textract.
    """

    def __init__(
        self,
        pymupdf_extractor: PyMuPDFExtractor,
        textract_extractor: TextractExtractor,
        minimum_text_length: int = 100,
    ) -> None:

        self.pymupdf = pymupdf_extractor
        self.textract = textract_extractor
        self.minimum_text_length = minimum_text_length

    def load(
        self,
        pdf_path: Path,
    ) -> ExtractedDocument:

        pymupdf_result = self.pymupdf.extract(
            pdf_path
        )

        if (
            len(pymupdf_result.text.strip())
            >= self.minimum_text_length
        ):
            return ExtractedDocument(
                text=pymupdf_result.text,
                extraction_method="pymupdf",
                page_count=pymupdf_result.page_count,
            )

        textract_result = self.textract.extract(
            pdf_path
        )

        return ExtractedDocument(
            text=textract_result.text,
            extraction_method="textract",
            page_count=textract_result.page_count,
        )