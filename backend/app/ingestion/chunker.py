from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class DocumentChunk:
    """
    Represents a chunk of document text.
    """

    chunk_index: int
    text: str


class DocumentChunker:
    """
    Splits cleaned document text into overlapping chunks.

    Character-based chunking is intentionally kept simple
    at this stage. Retrieval quality can be optimized later.
    """

    def __init__(
        self,
        chunk_size: int = 500,
        chunk_overlap: int = 50,
    ) -> None:

        if chunk_size <= 0:
            raise ValueError(
                "chunk_size must be greater than zero."
            )

        if chunk_overlap < 0:
            raise ValueError(
                "chunk_overlap cannot be negative."
            )

        if chunk_overlap >= chunk_size:
            raise ValueError(
                "chunk_overlap must be smaller than chunk_size."
            )

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split(
        self,
        text: str,
    ) -> list[DocumentChunk]:

        text = text.strip()

        if not text:
            return []

        chunks: list[DocumentChunk] = []

        start = 0
        chunk_index = 0

        text_length = len(text)

        while start < text_length:

            end = min(
                start + self.chunk_size,
                text_length,
            )

            chunk_text = text[
                start:end
            ].strip()

            if chunk_text:
                chunks.append(
                    DocumentChunk(
                        chunk_index=chunk_index,
                        text=chunk_text,
                    )
                )

                chunk_index += 1

            if end >= text_length:
                break

            start = end - self.chunk_overlap

        return chunks
