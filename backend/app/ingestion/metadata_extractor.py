from __future__ import annotations

from dataclasses import dataclass
from pathlib import PurePosixPath


@dataclass(frozen=True)
class DocumentMetadata:
    """
    Metadata associated with a source document.
    """

    file_name: str
    s3_key: str
    document_type: str
    region: str | None
    country: str | None


class MetadataExtractor:
    """
    Extract metadata from S3 object paths and filenames.
    """

    CONTRACT_KEYWORDS = (
        "contract",
        "agreement",
        "msa",
        "sow",
        "lease",
        "nda",
    )

    def extract(
        self,
        s3_key: str,
    ) -> DocumentMetadata:

        path = PurePosixPath(s3_key)

        file_name = path.name

        document_type = (
            self._detect_document_type(
                file_name
            )
        )

        parts = path.parts

        region = (
            parts[0]
            if len(parts) >= 2
            else None
        )

        country = (
            parts[1]
            if len(parts) >= 3
            else None
        )

        return DocumentMetadata(
            file_name=file_name,
            s3_key=s3_key,
            document_type=document_type,
            region=region,
            country=country,
        )

    def _detect_document_type(
        self,
        file_name: str,
    ) -> str:

        name = file_name.lower()

        for keyword in self.CONTRACT_KEYWORDS:

            if keyword in name:
                return "contract"

        return "unknown"