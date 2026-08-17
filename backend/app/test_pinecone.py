from __future__ import annotations

from backend.app.config.settings import settings

from backend.app.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddingModel,
)

from backend.app.embeddings.embedding_service import (
    EmbeddingService,
)

from backend.app.vectorstore.pinecone_store import (
    PineconeVectorStore,
)


def main() -> None:

    print("=" * 70)
    print("XEROX CONTRACT INTELLIGENCE")
    print("PINECONE VECTOR STORE TEST")
    print("=" * 70)

    # ---------------------------------------------------------
    # 1. Load embedding model
    # ---------------------------------------------------------

    print()
    print("Loading embedding model...")

    model = SentenceTransformerEmbeddingModel()

    embedding_service = EmbeddingService(
        model=model
    )

    dimension = embedding_service.dimension

    print(
        f"Embedding Model : "
        f"{settings.embedding_model}"
    )

    print(
        f"Embedding Dimension : {dimension}"
    )

    # ---------------------------------------------------------
    # 2. Connect to Pinecone
    # ---------------------------------------------------------

    print()
    print("Connecting to Pinecone...")

    vector_store = PineconeVectorStore(
        embedding_dimension=dimension
    )

    print(
        f"Index Name : "
        f"{vector_store.index_name}"
    )

    print(
        f"Namespace : "
        f"{vector_store.default_namespace}"
    )

    # ---------------------------------------------------------
    # 3. Get index statistics
    # ---------------------------------------------------------

    print()
    print("Checking Pinecone index statistics...")

    stats = vector_store.describe_index_stats()

    print()
    print("Pinecone Statistics:")
    print(stats)

    # ---------------------------------------------------------
    # 4. Create a test query embedding
    # ---------------------------------------------------------

    print()
    print("Creating test embedding...")

    test_text = (
        "Xerox contract information "
        "for enterprise customers."
    )

    vector = embedding_service.embed_query(
        test_text
    )

    print(
        f"Test Vector Dimension : "
        f"{len(vector)}"
    )

    # ---------------------------------------------------------
    # 5. Validate embedding dimension
    # ---------------------------------------------------------

    if len(vector) != dimension:

        raise ValueError(
            "Embedding dimension mismatch. "
            f"Expected {dimension}, "
            f"got {len(vector)}."
        )

    print(
        "Embedding dimension validation: PASSED"
    )

    # ---------------------------------------------------------
    # 6. Test vector search
    # ---------------------------------------------------------

    print()
    print("Testing vector search...")

    results = vector_store.search(
        vector=vector,
        top_k=5,
    )

    print(
        f"Search Results : {len(results)}"
    )

    if not results:

        print(
            "No vectors found in the Pinecone "
            "index yet."
        )

        print(
            "This is expected if no document "
            "chunks have been upserted."
        )

    else:

        for result in results:

            print("-" * 50)

            print(
                f"ID    : {result.id}"
            )

            print(
                f"Score : {result.score}"
            )

            print(
                f"Metadata : {result.metadata}"
            )

    # ---------------------------------------------------------
    # 7. Final result
    # ---------------------------------------------------------

    print()
    print("=" * 70)
    print(
        "PINECONE VECTOR STORE TEST "
        "COMPLETED SUCCESSFULLY"
    )
    print("=" * 70)


if __name__ == "__main__":
    main()