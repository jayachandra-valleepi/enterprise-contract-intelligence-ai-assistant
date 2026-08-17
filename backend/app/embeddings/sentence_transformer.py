from __future__ import annotations

from pathlib import Path
from typing import Sequence

import numpy as np
from sentence_transformers import SentenceTransformer

class SentenceTransformerEmbeddingModel:
    """
    Local Sentence Transformer embedding model.

    Used by the Xerox Contract Intelligence Platform to convert
    document chunks and user queries into dense numerical vectors.

    The same embedding model must be used for:
        - document chunks
        - user queries

    This ensures both vectors exist in the same embedding space.
    """

    DEFAULT_MODEL_NAME = (
        "sentence-transformers/all-MiniLM-L6-v2"
    )

    def __init__(
        self,
        model_name_or_path: str = DEFAULT_MODEL_NAME,
        device: str | None = None,
        normalize_embeddings: bool = True,
    ) -> None:

        if not model_name_or_path:
            raise ValueError(
                "Embedding model name or path is required."
            )

        self.model_name_or_path = model_name_or_path
        self.normalize_embeddings = normalize_embeddings

        model_path = Path(model_name_or_path)

        if model_path.exists():
            self.model = SentenceTransformer(
                str(model_path),
                device=device,
            )
        else:
            self.model = SentenceTransformer(
                model_name_or_path,
                device=device,
            )

    @property
    def dimension(self) -> int:
        """
        Return the embedding vector dimension.
        """

        dimension = self.model.get_sentence_embedding_dimension()

        if dimension is None:
            raise RuntimeError(
                "Unable to determine embedding dimension."
            )

        return int(dimension)

    def embed_text(
        self,
        text: str,
    ) -> list[float]:
        """
        Generate an embedding for a single text.
        """

        if not text or not text.strip():
            raise ValueError(
                "Text cannot be empty."
            )

        embedding = self.model.encode(
            text,
            convert_to_numpy=True,
            normalize_embeddings=self.normalize_embeddings,
        )

        return embedding.astype(
            np.float32
        ).tolist()

    def embed_texts(
        self,
        texts: Sequence[str],
        batch_size: int = 32,
        show_progress_bar: bool = False,
    ) -> list[list[float]]:
        """
        Generate embeddings for multiple texts.
        """

        if not texts:
            return []

        cleaned_texts: list[str] = []

        for text in texts:

            if not text or not text.strip():
                raise ValueError(
                    "Input texts cannot contain empty text."
                )

            cleaned_texts.append(
                text.strip()
            )

        embeddings = self.model.encode(
            cleaned_texts,
            batch_size=batch_size,
            show_progress_bar=show_progress_bar,
            convert_to_numpy=True,
            normalize_embeddings=self.normalize_embeddings,
        )

        return [
            vector.astype(np.float32).tolist()
            for vector in embeddings
        ]