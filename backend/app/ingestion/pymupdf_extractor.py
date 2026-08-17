from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import fitz

@dataclass(frozen=True)
class PyMuPDFResult:
    """
    Text extraction result from PyMuPDF.
    """

    text: str
    page_count: int


class PyMuPDFExtractor:
    """
    Extract text from text-based PDFs using PyMuPDF.
    """

    def extract(
        self,
        pdf_path: Path,
    ) -> PyMuPDFResult:

        if not pdf_path.exists():
            raise FileNotFoundError(
                f"PDF not found: {pdf_path}"
            )

        if pdf_path.suffix.lower() != ".pdf":
            raise ValueError(
                "Only PDF files are supported."
            )

        pages: list[str] = []

        try:
            document = fitz.open(
                str(pdf_path)
            )

        except Exception as exc:
            raise RuntimeError(
                f"Unable to open PDF: {pdf_path}"
            ) from exc

        try:
            page_count = len(document)

            for page_number, page in enumerate(
                document,
                start=1,
            ):

                text = page.get_text(
                    "text"
                )

                if text:
                    pages.append(
                        f"\n--- Page {page_number} ---\n"
                        f"{text}"
                    )

        finally:
            document.close()

        return PyMuPDFResult(
            text="\n".join(pages),
            page_count=page_count,
        )