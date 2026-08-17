from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterator

import boto3
from botocore.exceptions import BotoCoreError, ClientError

from backend.app.config.settings import settings


# ============================================================
# S3 Document
# ============================================================


@dataclass(frozen=True)
class S3Document:
    """
    Represents a PDF document stored in AWS S3.
    """

    bucket: str
    key: str
    etag: str | None
    size: int
    last_modified: datetime


# ============================================================
# S3 Loader
# ============================================================


class S3Loader:
    """
    Loads enterprise PDF documents from AWS S3.

    AWS S3 is the source of truth for Xerox contract documents.

    Responsibilities:
        1. Connect to S3
        2. List PDF documents
        3. Handle S3 pagination
        4. Download PDF documents
        5. Retrieve S3 object metadata

    PostgreSQL is NOT accessed here.

    PostgreSQL persistence is handled by the document repository
    layer later in the application.
    """

    def __init__(self) -> None:

        # ------------------------------------------------------
        # Validate S3 bucket configuration
        # ------------------------------------------------------

        if not settings.s3_bucket_name:

            raise ValueError(
                "S3 bucket name is required."
            )

        # ------------------------------------------------------
        # Store configuration
        # ------------------------------------------------------

        self.bucket_name = (
            settings.s3_bucket_name
        )

        self.prefix = (
            settings.s3_prefix.strip("/")
            if settings.s3_prefix
            else ""
        )

        # ------------------------------------------------------
        # Create boto3 S3 client
        #
        # AWS credentials are NOT hard-coded here.
        #
        # boto3 uses the standard AWS credential chain.
        # ------------------------------------------------------

        self.client = boto3.client(
            "s3",
            region_name=settings.aws_region,
        )

    # ========================================================
    # List Documents
    # ========================================================

    def list_documents(
        self,
    ) -> Iterator[S3Document]:
        """
        List PDF documents from the configured S3 prefix.

        Example S3 structure:

            bucket/
                India/
                    contract1.pdf
                    contract2.pdf

                France/
                    contract3.pdf

                Germany/
                    contract4.pdf

                UK/
                    contract5.pdf

        If S3_PREFIX is empty, all folders are scanned.

        If S3_PREFIX is 'contracts', only:

            contracts/

        is scanned.
        """

        continuation_token: str | None = None

        while True:

            # --------------------------------------------------
            # Build S3 request
            # --------------------------------------------------

            request = {
                "Bucket": self.bucket_name,
                "Prefix": self.prefix,
            }

            # --------------------------------------------------
            # Add pagination token
            # --------------------------------------------------

            if continuation_token:

                request[
                    "ContinuationToken"
                ] = continuation_token

            # --------------------------------------------------
            # Call S3
            # --------------------------------------------------

            try:

                response = (
                    self.client.list_objects_v2(
                        **request
                    )
                )

            except ClientError as exc:

                error = exc.response.get(
                    "Error",
                    {},
                )

                error_code = error.get(
                    "Code",
                    "Unknown",
                )

                error_message = error.get(
                    "Message",
                    str(exc),
                )

                raise RuntimeError(
                    "Unable to list documents from S3. "
                    f"AWS error: {error_code} - "
                    f"{error_message}"
                ) from exc

            except BotoCoreError as exc:

                raise RuntimeError(
                    "Unable to communicate with AWS S3."
                ) from exc

            # --------------------------------------------------
            # Process objects
            # --------------------------------------------------

            for item in response.get(
                "Contents",
                [],
            ):

                key = item["Key"]

                # ------------------------------------------------
                # Ignore folders
                # ------------------------------------------------

                if key.endswith("/"):
                    continue

                # ------------------------------------------------
                # Only process PDF files
                # ------------------------------------------------

                if not key.lower().endswith(
                    ".pdf"
                ):
                    continue

                # ------------------------------------------------
                # Create S3Document
                # ------------------------------------------------

                yield S3Document(
                    bucket=self.bucket_name,
                    key=key,
                    etag=item.get("ETag"),
                    size=item.get(
                        "Size",
                        0,
                    ),
                    last_modified=item[
                        "LastModified"
                    ],
                )

            # --------------------------------------------------
            # Check pagination
            # --------------------------------------------------

            if not response.get(
                "IsTruncated",
                False,
            ):
                break

            continuation_token = (
                response.get(
                    "NextContinuationToken"
                )
            )

            if not continuation_token:
                break

    # ========================================================
    # Download Document
    # ========================================================

    def download_document(
        self,
        document: S3Document,
        destination: Path,
    ) -> Path:
        """
        Download an S3 PDF document to a local temporary path.

        The application does not permanently store the PDF
        locally.

        Example:

            S3
             ↓
            temporary local file
             ↓
            PDF extraction
             ↓
            temporary file removed
        """

        # ------------------------------------------------------
        # Create destination directory
        # ------------------------------------------------------

        destination.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        # ------------------------------------------------------
        # Download
        # ------------------------------------------------------

        try:

            self.client.download_file(
                document.bucket,
                document.key,
                str(destination),
            )

        except ClientError as exc:

            error = exc.response.get(
                "Error",
                {},
            )

            error_code = error.get(
                "Code",
                "Unknown",
            )

            error_message = error.get(
                "Message",
                str(exc),
            )

            raise RuntimeError(
                "Unable to download S3 document. "
                f"Key: {document.key}. "
                f"AWS error: {error_code} - "
                f"{error_message}"
            ) from exc

        except BotoCoreError as exc:

            raise RuntimeError(
                "Unable to communicate with AWS S3 "
                f"while downloading: {document.key}"
            ) from exc

        return destination

    # ========================================================
    # Get Object Metadata
    # ========================================================

    def get_object_metadata(
        self,
        document: S3Document,
    ) -> dict:
        """
        Retrieve metadata for an S3 object.

        Returns:

            content_type
            content_length
            etag
            last_modified
        """

        try:

            response = (
                self.client.head_object(
                    Bucket=document.bucket,
                    Key=document.key,
                )
            )

        except ClientError as exc:

            error = exc.response.get(
                "Error",
                {},
            )

            error_code = error.get(
                "Code",
                "Unknown",
            )

            error_message = error.get(
                "Message",
                str(exc),
            )

            raise RuntimeError(
                "Unable to read S3 object metadata. "
                f"Key: {document.key}. "
                f"AWS error: {error_code} - "
                f"{error_message}"
            ) from exc

        except BotoCoreError as exc:

            raise RuntimeError(
                "Unable to communicate with AWS S3 "
                f"while reading metadata: "
                f"{document.key}"
            ) from exc

        return {
            "content_type": response.get(
                "ContentType"
            ),
            "content_length": response.get(
                "ContentLength"
            ),
            "etag": response.get(
                "ETag"
            ),
            "last_modified": response.get(
                "LastModified"
            ),
        }