
from datetime import datetime
from typing import Optional

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.database.connection import Base


# ==================================================================
# EXISTING USERS TABLE
# ==================================================================

class User(Base):
    """
    Maps to the existing PostgreSQL users table.

    IMPORTANT:
    This table already exists in PostgreSQL.

    SQLAlchemy uses this model to READ user information.
    It should not be treated as a new user-management table.
    """

    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    full_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    role: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    department: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    last_login: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )


# ==================================================================
# EXISTING PERMISSIONS TABLE
# ==================================================================

class Permission(Base):
    """
    Maps to the existing PostgreSQL permissions table.

    Example:

    Admin     -> ASK_QUESTION
    Admin     -> UPLOAD_DOCUMENT
    Analyst   -> ASK_QUESTION
    Viewer    -> VIEW_DOCUMENT

    The table already exists.
    """

    __tablename__ = "permissions"

    permission_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    role: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
    )

    permission_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

# ==================================================================
# DOCUMENTS TABLE
# ==================================================================

class Document(Base):
    """
    Stores metadata about documents available in the RAG system.

    IMPORTANT:

    Users do NOT upload documents.

    AWS S3 is the source of documents.

    This table stores metadata about those S3 documents.

    Example:

        S3
        |
        +-- contracts/abc_contract.pdf
        |
        +-- contracts/xyz_contract.pdf

    PostgreSQL stores metadata about them.
    """

    __tablename__ = "documents"

    document_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    file_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    s3_key: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
        unique=True,
        index=True,
    )

    document_type: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
    )

    version: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="uploaded",
        index=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    conversations: Mapped[list["Conversation"]] = relationship(
        back_populates="document",
    )


# ==================================================================
# CONVERSATIONS TABLE
# ==================================================================

class Conversation(Base):
    """
    Represents a user's conversation with the RAG system.

    Example:

        User:
            Jay

        Conversation:
            Contract Questions

        Messages:
            User question
            Assistant answer
            User follow-up
            Assistant answer
    """

    __tablename__ = "conversations"

    conversation_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.user_id"),
        nullable=False,
        index=True,
    )

    document_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("documents.document_id"),
        nullable=True,
        index=True,
    )

    title: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    document: Mapped[Optional["Document"]] = relationship(
        back_populates="conversations",
    )

    messages: Mapped[list["ChatMessage"]] = relationship(
        back_populates="conversation",
        cascade="all, delete-orphan",
    )


# ==================================================================
# CHAT MESSAGES TABLE
# ==================================================================

class ChatMessage(Base):
    """
    Stores individual user and assistant messages.

    role values:

        user
        assistant
    """

    __tablename__ = "chat_messages"

    message_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    conversation_id: Mapped[int] = mapped_column(
        ForeignKey("conversations.conversation_id"),
        nullable=False,
        index=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.user_id"),
        nullable=False,
        index=True,
    )

    role: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    conversation: Mapped["Conversation"] = relationship(
        back_populates="messages",
    )


# ==================================================================
# AUDIT LOGS TABLE
# ==================================================================

class AuditLog(Base):
    """
    Stores application security and activity logs.

    Examples:

        LOGIN
        LOGOUT
        ASK_QUESTION
        VIEW_DOCUMENT
        SEARCH_DOCUMENT
    """

    __tablename__ = "audit_logs"

    audit_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.user_id"),
        nullable=False,
        index=True,
    )

    action: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    resource_type: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
    )

    resource_id: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
    )

    details: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    ip_address: Mapped[Optional[str]] = mapped_column(
        String(45),
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="SUCCESS",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        index=True,
    )


# ==================================================================
# FEEDBACK TABLE
# ==================================================================

class Feedback(Base):
    """
    Stores user feedback about RAG answers.

    Example:

        rating = 5
        comment = "Correct answer"

    This will be useful later for RAG evaluation.
    """

    __tablename__ = "feedback"

    feedback_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    message_id: Mapped[int] = mapped_column(
        ForeignKey("chat_messages.message_id"),
        nullable=False,
        index=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.user_id"),
        nullable=False,
        index=True,
    )

    rating: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    comment: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    __table_args__ = (
        UniqueConstraint(
            "message_id",
            "user_id",
            name="uq_feedback_message_user",
        ),
    )

