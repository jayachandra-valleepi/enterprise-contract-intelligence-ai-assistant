from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import boto3
from botocore.exceptions import BotoCoreError, ClientError


@dataclass(frozen=True)
class TextractResult:
    """
    OCR extraction result.
    """

    text: str
    page_count: int


class TextractExtractor:
    """
    Extract text from scanned PDFs using AWS Textract.

    Uses synchronous Textract document analysis.
    """

    def __init__(
        self,
        region_name: str,
    ) -> None:

        self.client = boto3.client(
            "textract",
            region_name=region_name,
        )

    def extract(
        self,
        pdf_path: Path,
    ) -> TextractResult:

        if not pdf_path.exists():
            raise FileNotFoundError(
                f"PDF not found: {pdf_path}"
            )

        try:
            with pdf_path.open("rb") as file:
                document_bytes = file.read()

            response = self.client.detect_document_text(
                Document={
                    "Bytes": document_bytes,
                }
            )

        except (ClientError, BotoCoreError) as exc:
            raise RuntimeError(
                f"Textract failed for: {pdf_path.name}"
            ) from exc

        lines: list[str] = []

        for block in response.get(
            "Blocks",
            [],
        ):

            if block.get("BlockType") == "LINE":

                text = block.get(
                    "Text",
                    "",
                ).strip()

                if text:
                    lines.append(text)

        page_numbers = {
            block.get("Page")
            for block in response.get(
                "Blocks",
                [],
            )
            if block.get("Page") is not None
        }

        return TextractResult(
            text="\n".join(lines),
            page_count=len(page_numbers),
        )