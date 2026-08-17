from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from backend.app.config.settings import settings


# ============================================================
# DATABASE URL
# ============================================================

database_url = URL.create(
    drivername="postgresql+psycopg",
    username=settings.postgres_user,
    password=settings.postgres_password,
    host=settings.postgres_host,
    port=settings.postgres_port,
    database=settings.postgres_db,
)


# ============================================================
# PostgreSQL Engine
# ============================================================

engine = create_engine(
    database_url,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
    echo=False,
)


# ============================================================
# SESSION FACTORY
# ============================================================

SessionLocal = sessionmaker(
    bind=engine,
    class_=Session,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)


# ============================================================
# BASE MODEL
# ============================================================

class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""
    pass


# ============================================================
# DATABASE SESSION DEPENDENCY
# ============================================================

def get_db() -> Generator[Session, None, None]:
    """
    Provides a SQLAlchemy database session.

    FastAPI will use this function as a dependency.

    The session is always closed after the request.
    """

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# ============================================================
# Create Application Tables
# ============================================================

def create_tables() -> None:
    """Create all database tables.

    Development/testing helper.

    Production should use Alembic migrations instead.
    

    Existing tables such as users and permissions are mapped
    by SQLAlchemy but are NOT intentionally recreated"""
    from backend.app.database import models  # noqa: F401

    Base.metadata.create_all(bind=engine)