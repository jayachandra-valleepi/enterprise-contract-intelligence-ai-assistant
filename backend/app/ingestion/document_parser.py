from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from app.ingestion.pdf_loader import (
    ExtractedDocument,
    PDFLoader,
)


@dataclass(frozen=True)
class ParsedDocument:
    """
    Parsed document after PDF extraction.
    """

    source_path: Path
    text: str
    extraction_method: str
    page_count: int


class DocumentParser:
    """
    Converts a PDF file into extracted text.
    """

    def __init__(
        self,
        pdf_loader: PDFLoader,
    ) -> None:

        self.pdf_loader = pdf_loader

    def parse(
        self,
        pdf_path: Path,
    ) -> ParsedDocument:

        result: ExtractedDocument = (
            self.pdf_loader.load(
                pdf_path
            )
        )

        return ParsedDocument(
            source_path=pdf_path,
            text=result.text,
            extraction_method=(
                result.extraction_method
            ),
            page_count=result.page_count,
        )