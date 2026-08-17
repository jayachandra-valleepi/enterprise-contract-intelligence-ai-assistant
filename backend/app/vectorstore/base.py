from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Sequence


@dataclass(frozen=True)
class VectorRecord:
    """
    A vector that can be stored in a vector database.
    """

    id: str
    values: list[float]
    metadata: dict[str, Any]


@dataclass(frozen=True)
class VectorSearchResult:
    """
    Result returned from vector similarity search.
    """

    id: str
    score: float
    metadata: dict[str, Any]


class VectorStore(ABC):
    """
    Abstract interface for vector stores.

    Pinecone is the current implementation.

    Keeping this interface separate allows the application
    to switch vector databases later without changing the
    RAG business logic.
    """

    @abstractmethod
    def upsert(
        self,
        records: Sequence[VectorRecord],
        namespace: str | None = None,
    ) -> None:
        """
                Insert or update vectors.
        """
        raise NotImplementedError

    
    @abstractmethod
    def search(
        self,
        vector: Sequence[float],
        top_k: int,
        namespace: str | None = None,
        metadata_filter: dict[str, Any] | None = None,
    ) -> list[VectorSearchResult]:
        """
                    Search for similar vectors.
        """
        raise NotImplementedError


    @abstractmethod
    def delete(
        self,
        ids: Sequence[str],
        namespace: str | None = None,
    ) -> None:
        """
        Delete vectors.
        """
        raise NotImplementedError

        