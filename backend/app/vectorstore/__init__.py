"""
Vector store services for the Xerox Contract Intelligence Platform.
"""

from backend.app.vectorstore.base import (
    VectorRecord,
    VectorSearchResult,
    VectorStore,
)

from backend.app.vectorstore.pinecone_store import (
    PineconeVectorStore,
)

__all__ = [
    "VectorRecord",
    "VectorSearchResult",
    "VectorStore",
    "PineconeVectorStore",
]