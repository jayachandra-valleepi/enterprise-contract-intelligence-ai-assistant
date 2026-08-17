from __future__ import annotations

import time
from typing import Any, Sequence

from pinecone import Pinecone, ServerlessSpec
from pinecone.exceptions import PineconeException

from backend.app.config.settings import settings

from backend.app.vectorstore.base import (
    VectorRecord,
    VectorSearchResult,
    VectorStore,
)


class PineconeVectorStore(VectorStore):
    """
    Pinecone vector store for the
    Xerox Contract Intelligence Platform.

    Responsibilities
    ----------------
    - Connect to Pinecone
    - Check whether the index exists
    - Create the index if it does not exist
    - Wait until the index is ready
    - Validate embedding dimension
    - Upsert vectors
    - Search vectors
    - Apply metadata filters
    - Delete vectors
    - Return index statistics

    Pinecone stores:
        - embeddings
        - chunk text
        - document metadata

    PostgreSQL stores:
        - users
        - roles
        - permissions
        - application metadata
        - chat history metadata
        - feedback
        - audit logs
    """

    def __init__(
        self,
        embedding_dimension: int,
    ) -> None:
        """
        Initialize Pinecone.

        embedding_dimension comes from the
        Sentence Transformer model.

        Example:

            all-mpnet-base-v2
                    ↓
                768 dimensions
        """

        if embedding_dimension <= 0:
            raise ValueError(
                "Embedding dimension must be greater than zero."
            )

        if not settings.pinecone_api_key:
            raise ValueError(
                "Pinecone API key is required."
            )

        if not settings.pinecone_index_name:
            raise ValueError(
                "Pinecone index name is required."
            )

        self.embedding_dimension = embedding_dimension

        self.index_name = (
            settings.pinecone_index_name
        )

        self.default_namespace = (
            settings.pinecone_namespace
        )

        # -----------------------------------------------------
        # Connect to Pinecone
        # -----------------------------------------------------

        self.client = Pinecone(
            api_key=settings.pinecone_api_key
        )

        # -----------------------------------------------------
        # Create index if required
        # -----------------------------------------------------

        self._create_index_if_not_exists()

        # -----------------------------------------------------
        # Connect to the index
        # -----------------------------------------------------

        self.index = self.client.Index(
            self.index_name
        )

        # -----------------------------------------------------
        # Validate dimension
        # -----------------------------------------------------

        self._validate_index_dimension()

    # =========================================================
    # INDEX MANAGEMENT
    # =========================================================

    def _get_existing_index_names(
        self,
    ) -> set[str]:
        """
        Return the names of all existing Pinecone indexes.
        """

        try:

            indexes = self.client.list_indexes()

            names: set[str] = set()

            for index in indexes:

                if isinstance(index, dict):

                    name = index.get("name")

                else:

                    name = getattr(
                        index,
                        "name",
                        None,
                    )

                if name:
                    names.add(str(name))

            return names

        except PineconeException as exc:

            raise RuntimeError(
                "Unable to retrieve Pinecone indexes."
            ) from exc

    def _create_index_if_not_exists(
        self,
    ) -> None:
        """
        Check whether the configured index exists.

        If it does not exist, create it automatically.
        """

        existing_indexes = (
            self._get_existing_index_names()
        )

        # -----------------------------------------------------
        # Index already exists
        # -----------------------------------------------------

        if self.index_name in existing_indexes:

            print(
                f"Pinecone index already exists: "
                f"{self.index_name}"
            )

            return

        # -----------------------------------------------------
        # Index does not exist
        # -----------------------------------------------------

        print(
            f"Pinecone index '{self.index_name}' "
            f"does not exist."
        )

        print(
            f"Creating Pinecone index "
            f"'{self.index_name}'..."
        )

        try:

            self.client.create_index(
                name=self.index_name,
                dimension=self.embedding_dimension,
                metric="cosine",
                spec=ServerlessSpec(
                    cloud=settings.pinecone_cloud,
                    region=settings.pinecone_region,
                ),
            )

        except PineconeException as exc:

            raise RuntimeError(
                f"Unable to create Pinecone index "
                f"'{self.index_name}'."
            ) from exc

        print(
            f"Pinecone index creation started: "
            f"{self.index_name}"
        )

        # -----------------------------------------------------
        # Wait until ready
        # -----------------------------------------------------

        self._wait_for_index()

    def _wait_for_index(
        self,
        timeout_seconds: int = 120,
        poll_interval_seconds: int = 2,
    ) -> None:
        """
        Wait until Pinecone index becomes ready.
        """

        print(
            "Waiting for Pinecone index "
            "to become ready..."
        )

        start_time = time.time()

        while True:

            try:

                description = (
                    self.client.describe_index(
                        self.index_name
                    )
                )

                status = getattr(
                    description,
                    "status",
                    None,
                )

                if status is None:

                    if isinstance(
                        description,
                        dict,
                    ):
                        status = description.get(
                            "status"
                        )

                if isinstance(
                    status,
                    dict,
                ):

                    ready = status.get(
                        "ready",
                        False,
                    )

                else:

                    ready = getattr(
                        status,
                        "ready",
                        False,
                    )

                if ready:

                    print(
                        "Pinecone index is ready."
                    )

                    return

            except PineconeException as exc:

                if (
                    time.time() - start_time
                    >= timeout_seconds
                ):

                    raise RuntimeError(
                        "Timed out while waiting "
                        "for Pinecone index."
                    ) from exc

            if (
                time.time() - start_time
                >= timeout_seconds
            ):

                raise TimeoutError(
                    f"Pinecone index "
                    f"'{self.index_name}' "
                    f"did not become ready within "
                    f"{timeout_seconds} seconds."
                )

            time.sleep(
                poll_interval_seconds
            )

    def _validate_index_dimension(
        self,
    ) -> None:
        """
        Verify that Pinecone index dimension matches
        the Sentence Transformer embedding dimension.
        """

        try:

            description = (
                self.client.describe_index(
                    self.index_name
                )
            )

        except PineconeException as exc:

            raise RuntimeError(
                f"Unable to describe Pinecone index "
                f"'{self.index_name}'."
            ) from exc

        index_dimension = getattr(
            description,
            "dimension",
            None,
        )

        if index_dimension is None:

            if isinstance(
                description,
                dict,
            ):

                index_dimension = (
                    description.get(
                        "dimension"
                    )
                )

        if index_dimension is None:

            raise RuntimeError(
                "Unable to determine Pinecone "
                "index dimension."
            )

        if int(index_dimension) != (
            self.embedding_dimension
        ):

            raise ValueError(
                "Pinecone dimension mismatch. "
                f"Pinecone index dimension = "
                f"{index_dimension}, "
                f"Embedding dimension = "
                f"{self.embedding_dimension}."
            )

        print(
            f"Pinecone dimension validated: "
            f"{index_dimension}"
        )

    # =========================================================
    # UPSERT
    # =========================================================

    def upsert(
        self,
        records: Sequence[VectorRecord],
        namespace: str | None = None,
        batch_size: int = 100,
    ) -> None:
        """
        Insert or update vectors in Pinecone.
        """

        if not records:
            return

        if batch_size <= 0:
            raise ValueError(
                "Batch size must be greater than zero."
            )

        target_namespace = (
            namespace
            or self.default_namespace
        )

        for start in range(
            0,
            len(records),
            batch_size,
        ):

            batch = records[
                start:start + batch_size
            ]

            vectors = []

            for record in batch:

                if not record.id:

                    raise ValueError(
                        "Vector ID cannot be empty."
                    )

                if not record.values:

                    raise ValueError(
                        f"Vector values cannot be "
                        f"empty for ID: {record.id}"
                    )

                if len(record.values) != (
                    self.embedding_dimension
                ):

                    raise ValueError(
                        f"Vector dimension mismatch "
                        f"for ID '{record.id}'. "
                        f"Expected "
                        f"{self.embedding_dimension}, "
                        f"received "
                        f"{len(record.values)}."
                    )

                vectors.append(
                    {
                        "id": record.id,
                        "values": record.values,
                        "metadata": record.metadata,
                    }
                )

            try:

                self.index.upsert(
                    vectors=vectors,
                    namespace=target_namespace,
                )

            except PineconeException as exc:

                raise RuntimeError(
                    "Unable to upsert vectors "
                    "into Pinecone."
                ) from exc

    # =========================================================
    # SEARCH
    # =========================================================

    def search(
        self,
        vector: Sequence[float],
        top_k: int = 5,
        namespace: str | None = None,
        metadata_filter: dict[str, Any] | None = None,
    ) -> list[VectorSearchResult]:
        """
        Search Pinecone for similar vectors.
        """

        if not vector:

            raise ValueError(
                "Query vector cannot be empty."
            )

        if len(vector) != (
            self.embedding_dimension
        ):

            raise ValueError(
                "Query vector dimension mismatch. "
                f"Expected "
                f"{self.embedding_dimension}, "
                f"received "
                f"{len(vector)}."
            )

        if top_k <= 0:

            raise ValueError(
                "top_k must be greater than zero."
            )

        target_namespace = (
            namespace
            or self.default_namespace
        )

        query_kwargs: dict[str, Any] = {
            "namespace": target_namespace,
            "vector": list(vector),
            "top_k": top_k,
            "include_metadata": True,
            "include_values": False,
        }

        if metadata_filter:

            query_kwargs["filter"] = (
                metadata_filter
            )

        try:

            response = self.index.query(
                **query_kwargs
            )

        except PineconeException as exc:

            raise RuntimeError(
                "Unable to search Pinecone."
            ) from exc

        matches = getattr(
            response,
            "matches",
            [],
        )

        results: list[
            VectorSearchResult
        ] = []

        for match in matches:

            match_id = getattr(
                match,
                "id",
                None,
            )

            if match_id is None:
                continue

            score = getattr(
                match,
                "score",
                0.0,
            )

            metadata = getattr(
                match,
                "metadata",
                {},
            )

            results.append(
                VectorSearchResult(
                    id=str(match_id),
                    score=float(score),
                    metadata=dict(
                        metadata or {}
                    ),
                )
            )

        return results

    # =========================================================
    # DELETE
    # =========================================================

    def delete(
        self,
        ids: Sequence[str],
        namespace: str | None = None,
    ) -> None:
        """
        Delete vectors by IDs.
        """

        if not ids:
            return

        target_namespace = (
            namespace
            or self.default_namespace
        )

        try:

            self.index.delete(
                ids=list(ids),
                namespace=target_namespace,
            )

        except PineconeException as exc:

            raise RuntimeError(
                "Unable to delete vectors "
                "from Pinecone."
            ) from exc

    def delete_namespace(
        self,
        namespace: str | None = None,
    ) -> None:
        """
        Delete all vectors from a namespace.
        """

        target_namespace = (
            namespace
            or self.default_namespace
        )

        try:

            self.index.delete(
                delete_all=True,
                namespace=target_namespace,
            )

        except PineconeException as exc:

            raise RuntimeError(
                "Unable to delete namespace "
                f"'{target_namespace}'."
            ) from exc

    # =========================================================
    # STATISTICS
    # =========================================================

    def describe_index_stats(
        self,
    ) -> Any:
        """
        Return Pinecone index statistics.
        """

        try:

            return (
                self.index.describe_index_stats()
            )

        except PineconeException as exc:

            raise RuntimeError(
                "Unable to retrieve Pinecone "
                "index statistics."
            ) from exc