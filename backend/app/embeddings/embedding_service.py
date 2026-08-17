from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from backend.app.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddingModel,
)


@dataclass(frozen=True)
class EmbeddedText:
    """
    Represents text together with its embedding.
    """

    text: str
    vector: list[float]


class EmbeddingService:
    """
    Application-level embedding service.

    Responsibilities:
        - Generate document embeddings
        - Generate query embeddings
        - Keep embedding logic away from Pinecone
    """

    def __init__(
        self,
        model: SentenceTransformerEmbeddingModel,
    ) -> None:

        self.model = model

    @property
    def dimension(self) -> int:
        """
        Return embedding dimension.
        """

        return self.model.dimension

    def embed_document(
        self,
        text: str,
    ) -> list[float]:
        """
        Create an embedding for a document chunk.
        """

        return self.model.embed_text(
            text
        )

    def embed_documents(
        self,
        texts: Sequence[str],
        batch_size: int = 32,
    ) -> list[list[float]]:
        """
        Create embeddings for multiple document chunks.
        """

        return self.model.embed_texts(
            texts=texts,
            batch_size=batch_size,
        )

    def embed_query(
        self,
        query: str,
    ) -> list[float]:
        """
        Create an embedding for a user query.
        """

        return self.model.embed_text(
            query
        )