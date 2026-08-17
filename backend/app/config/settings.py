
from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application configuration loaded from environment variables / .env file.
    """

    # ============================================================
    # APPLICATION
    # ============================================================

    app_name: str = Field(
        default="Enterprise-RAG-Application",
        validation_alias="APP_NAME",
    )

    app_env: str = Field(
        default="development",
        validation_alias="APP_ENV",
    )

    debug: bool = Field(
        default=False,
        validation_alias="DEBUG",
    )

    api_v1_prefix: str = Field(
        default="/api/v1",
        validation_alias="API_V1_PREFIX",
    )

    # ============================================================
    # SECURITY / JWT
    # ============================================================

    jwt_secret_key: str = Field(
        validation_alias="JWT_SECRET_KEY",
    )

    jwt_algorithm: str = Field(
        default="HS256",
        validation_alias="JWT_ALGORITHM",
    )

    access_token_expire_minutes: int = Field(
        default=30,
        validation_alias="ACCESS_TOKEN_EXPIRE_MINUTES",
    )

    refresh_token_expire_days: int = Field(
        default=7,
        validation_alias="REFRESH_TOKEN_EXPIRE_DAYS",
    )

    # ============================================================
    # POSTGRESQL
    # ============================================================

    postgres_host: str = Field(
        default="localhost",
        validation_alias="POSTGRES_HOST",
    )

    postgres_port: int = Field(
        default=5432,
        validation_alias="POSTGRES_PORT",
    )

    postgres_db: str = Field(
        default="postgres",
        validation_alias="POSTGRES_DB",
    )

    postgres_user: str = Field(
        default="postgres",
        validation_alias="POSTGRES_USER",
    )

    postgres_password: str = Field(
        validation_alias="POSTGRES_PASSWORD",
    )

    database_url: str = Field(
        validation_alias="DATABASE_URL",
    )

    # ============================================================
    # REDIS
    # ============================================================

    redis_host: str = Field(
        default="localhost",
        validation_alias="REDIS_HOST",
    )

    redis_port: int = Field(
        default=6379,
        validation_alias="REDIS_PORT",
    )

    redis_db: int = Field(
        default=0,
        validation_alias="REDIS_DB",
    )

    redis_password: str = Field(
        default="",
        validation_alias="REDIS_PASSWORD",
    )

    redis_url: str = Field(
        default="redis://localhost:6379/0",
        validation_alias="REDIS_URL",
    )

    # ============================================================
    # AWS
    # ============================================================

    aws_access_key_id: str | None = Field(
        default=None,
        validation_alias="AWS_ACCESS_KEY_ID",
    )

    aws_secret_access_key: str | None = Field(
        default=None,
        validation_alias="AWS_SECRET_ACCESS_KEY",
    )

    aws_region: str = Field(
        default="us-east-1",
        validation_alias="AWS_REGION",
    )

    s3_bucket_name: str = Field(
        validation_alias="S3_BUCKET_NAME",
    )

    s3_prefix: str | None = Field(
        default=None,
        validation_alias="AWS_S3_PREFIX",
    )

    # ============================================================
    # AWS TEXTRACT
    # ============================================================

    textract_enabled: bool = Field(
        default=True,
        validation_alias="TEXTRACT_ENABLED",
    )

    # ============================================================
    # GROQ
    # ============================================================

    groq_api_key: str = Field(
        validation_alias="GROQ_API_KEY",
    )

    groq_model: str = Field(
        validation_alias="GROQ_MODEL",
    )

    # ============================================================
    # SENTENCE TRANSFORMERS
    # ============================================================

    embedding_model: str = Field(
        default="sentence-transformers/all-MiniLM-L6-v2",
        validation_alias="EMBEDDING_MODEL",
    )

    embedding_dimension: int = Field(
        default=384,
        validation_alias="EMBEDDING_DIMENSION",
    )

    # ============================================================
    # PINECONE
    # ============================================================

    pinecone_api_key: str = Field(
        validation_alias="PINECONE_API_KEY",
    )

    pinecone_index_name: str = Field(
        validation_alias="PINECONE_INDEX_NAME",
    )

    pinecone_namespace: str = Field(
        default="contracts",
        validation_alias="PINECONE_NAMESPACE",
    )
    pinecone_cloud: str = Field(
            default="aws",
            validation_alias="PINECONE_CLOUD",
    )
    pinecone_region: str = Field(
                default="us-east-1",
                validation_alias="PINECONE_REGION",
        )
    

    # ============================================================
    # COHERE RERANKER
    # ============================================================

    cohere_api_key: str = Field(
        validation_alias="COHERE_API_KEY",
    )

    cohere_rerank_model: str = Field(
        default="rerank-v3.5",
        validation_alias="COHERE_RERANK_MODEL",
    )

    # ============================================================
    # RAG CONFIGURATION
    # ============================================================

    chunk_size: int = Field(
        default=800,
        validation_alias="CHUNK_SIZE",
    )

    chunk_overlap: int = Field(
        default=150,
        validation_alias="CHUNK_OVERLAP",
    )

    semantic_top_k: int = Field(
        default=20,
        validation_alias="SEMANTIC_TOP_K",
    )

    bm25_top_k: int = Field(
        default=20,
        validation_alias="BM25_TOP_K",
    )

    hybrid_top_k: int = Field(
        default=20,
        validation_alias="HYBRID_TOP_K",
    )

    rerank_top_k: int = Field(
        default=5,
        validation_alias="RERANK_TOP_K",
    )

    similarity_threshold: float = Field(
        default=0.70,
        validation_alias="SIMILARITY_THRESHOLD",
    )

    # ============================================================
    # CACHE
    # ============================================================

    cache_enabled: bool = Field(
        default=True,
        validation_alias="CACHE_ENABLED",
    )

    cache_ttl: int = Field(
        default=3600,
        validation_alias="CACHE_TTL",
    )

    # ============================================================
    # RAGAS
    # ============================================================

    ragas_enabled: bool = Field(
        default=True,
        validation_alias="RAGAS_ENABLED",
    )

    # ============================================================
    # MONITORING
    # ============================================================

    prometheus_enabled: bool = Field(
        default=True,
        validation_alias="PROMETHEUS_ENABLED",
    )

    otel_enabled: bool = Field(
        default=True,
        validation_alias="OTEL_ENABLED",
    )

    otel_service_name: str = Field(
        default="enterprise-rag",
        validation_alias="OTEL_SERVICE_NAME",
    )

    otel_service_version: str = Field(
        default="1.0.0",
        validation_alias="OTEL_SERVICE_VERSION",
    )

    # ============================================================
    # LOGGING
    # ============================================================

    log_level: str = Field(
        default="INFO",
        validation_alias="LOG_LEVEL",
    )

    # ============================================================
    # PYDANTIC SETTINGS CONFIGURATION
    # ============================================================

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """
    Return a cached Settings object.

    Using lru_cache prevents loading and parsing the .env file
    repeatedly for every request.
    """
    return Settings()


settings = get_settings()