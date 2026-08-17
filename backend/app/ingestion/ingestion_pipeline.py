from __future__ import annotations

import tempfile
from pathlib import Path

from backend.app.ingestion.chunker import(
    DocumentChunk,
    DocumentChunker
)

from backend.app.ingestion.document_cleaner import (
    DocumentCleaner
)

from backend.app.ingestion.document_parser import(
    DocumentParser
)

from backend.app.ingestion.metadata_extractor import(
    DocumentMetadata,
    MetadataExtractor,
)

from backend.app.ingestion.s3_loader import (
    S3Document,
    S3Loader
)


class IngestionPipeline:
    """
    End-to-end document ingestion pipeline.

    AWS S3
        ↓
    Download PDF
        ↓
    Extract text
        ↓
    Clean text
        ↓
    Extract metadata
        ↓
    Chunk text
        ↓
    Return ingestion result

    PostgreSQL persistence and vector-store indexing are
    intentionally handled by later application layers.
    """

    def __init__(
        self,
        s3_loader: S3Loader,
        document_parser: DocumentParser,
        cleaner: DocumentCleaner,
        metadata_extractor: MetadataExtractor,
        chunker: DocumentChunker,
    ) -> None:

        self.s3_loader = s3_loader
        self.document_parser = document_parser
        self.cleaner = cleaner
        self.metadata_extractor = metadata_extractor
        self.chunker = chunker

    def ingest_document(
        self,
        s3_document: S3Document,
    ) -> "IngestionResult":

        metadata = self.metadata_extractor.extract(
            s3_document.key
        )

        with tempfile.TemporaryDirectory(
            prefix="xerox-rag-"
        ) as temp_dir:

            pdf_path = (
                Path(temp_dir)
                / metadata.file_name
            )

            self.s3_loader.download_document(
                document=s3_document,
                destination=pdf_path,
            )

            parsed_document = (
                self.document_parser.parse(
                    pdf_path
                )
            )

            cleaned_text = self.cleaner.clean(
                parsed_document.text
            )

            if not cleaned_text:
                raise ValueError(
                    f"No text extracted from "
                    f"{metadata.file_name}"
                )

            chunks = self.chunker.split(
                cleaned_text
            )

            if not chunks:
                raise ValueError(
                    f"No chunks generated for "
                    f"{metadata.file_name}"
                )

            return IngestionResult(
                metadata=metadata,
                extraction_method=(
                    parsed_document.extraction_method
                ),
                page_count=(
                    parsed_document.page_count
                ),
                text_length=len(cleaned_text),
                chunks=chunks,
                s3_etag=s3_document.etag,
                s3_size=s3_document.size,
                s3_last_modified=(
                    s3_document.last_modified
                ),
            )

    def ingest_all(
        self,
    ) -> list["IngestionResult"]:

        results: list[IngestionResult] = []

        for document in (
            self.s3_loader.list_documents()
        ):

            result = self.ingest_document(
                document
            )

            results.append(result)

        return results


class IngestionResult:
    """
    Final result returned by the ingestion pipeline.
    """

    def __init__(
        self,
        metadata: DocumentMetadata,
        extraction_method: str,
        page_count: int,
        text_length: int,
        chunks: list[DocumentChunk],
        s3_etag: str | None,
        s3_size: int,
        s3_last_modified,
    ) -> None:

        self.metadata = metadata
        self.extraction_method = extraction_method
        self.page_count = page_count
        self.text_length = text_length
        self.chunks = chunks
        self.s3_etag = s3_etag
        self.s3_size = s3_size
        self.s3_last_modified = s3_last_modified