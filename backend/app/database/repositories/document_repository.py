from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.database.models import Document


class DocumentRepository:
    """
    Repository for document metadata.

    Actual documents are stored in AWS S3.
    PostgreSQL stores document metadata only.
    """

    def __init__(self, db: Session):
        self.db = db

    # --------------------------------------------------------------
    # Create document metadata
    # --------------------------------------------------------------

    def create(
        self,
        file_name: str,
        s3_key: str,
        document_type: Optional[str] = None,
        version: int = 1,
        status: str = "uploaded",
    ) -> Document:

        document = Document(
            file_name=file_name,
            s3_key=s3_key,
            document_type=document_type,
            version=version,
            status=status,
        )

        self.db.add(document)
        self.db.commit()
        self.db.refresh(document)

        return document

    # --------------------------------------------------------------
    # Get by document ID
    # --------------------------------------------------------------

    def get_by_id(
        self,
        document_id: int,
    ) -> Optional[Document]:

        statement = select(Document).where(
            Document.document_id == document_id
        )

        return self.db.scalar(statement)

    # --------------------------------------------------------------
    # Get by S3 key
    # --------------------------------------------------------------

    def get_by_s3_key(
        self,
        s3_key: str,
    ) -> Optional[Document]:

        statement = select(Document).where(
            Document.s3_key == s3_key
        )

        return self.db.scalar(statement)

    # --------------------------------------------------------------
    # Get all processed documents
    # --------------------------------------------------------------

    def get_processed_documents(
        self,
    ) -> list[Document]:

        statement = (
            select(Document)
            .where(Document.status == "processed")
            .order_by(Document.updated_at.desc())
        )

        return list(
            self.db.scalars(statement).all()
        )

    # --------------------------------------------------------------
    # Update document status
    # --------------------------------------------------------------

    def update_status(
        self,
        document_id: int,
        status: str,
    ) -> Optional[Document]:

        document = self.get_by_id(document_id)

        if document is None:
            return None

        document.status = status

        self.db.commit()
        self.db.refresh(document)

        return document

    # --------------------------------------------------------------
    # Update document version
    # --------------------------------------------------------------

    def update_version(
        self,
        document_id: int,
        version: int,
    ) -> Optional[Document]:

        document = self.get_by_id(document_id)

        if document is None:
            return None

        document.version = version

        self.db.commit()
        self.db.refresh(document)

        return document

    # --------------------------------------------------------------
    # Update document metadata
    # --------------------------------------------------------------

    def update_metadata(
        self,
        document_id: int,
        file_name: Optional[str] = None,
        document_type: Optional[str] = None,
        version: Optional[int] = None,
        status: Optional[str] = None,
    ) -> Optional[Document]:

        document = self.get_by_id(document_id)

        if document is None:
            return None

        if file_name is not None:
            document.file_name = file_name

        if document_type is not None:
            document.document_type = document_type

        if version is not None:
            document.version = version

        if status is not None:
            document.status = status

        self.db.commit()
        self.db.refresh(document)

        return document