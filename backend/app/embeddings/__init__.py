"""
Embedding services for the Xerox Contract Intelligence Platform.
"""

from backend.app.embeddings.embedding_service import (
    EmbeddingService,
)
from backend.app.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddingModel,
)

__all__ = [
    "EmbeddingService",
    "SentenceTransformerEmbeddingModel",
]