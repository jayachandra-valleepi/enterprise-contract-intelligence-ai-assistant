from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterator

import boto3
from botocore.exceptions import BotoCoreError, ClientError


@dataclass(frozen=True)
class S3Document:
    """
    Represents a PDF document stored in S3.
    """

    bucket: str
    key: str
    etag: str | None
    size: int
    last_modified: datetime


class S3Loader:
    """
    Reads PDF documents from AWS S3.

    S3 is the source of truth for enterprise documents.
    """

    def __init__(
        self,
        bucket_name: str,
        region_name: str,
        prefix: str = "",
    ) -> None:

        if not bucket_name:
            raise ValueError("S3 bucket name is required.")

        self.bucket_name = bucket_name
        self.prefix = prefix.strip("/")

        self.client = boto3.client(
            "s3",
            region_name=region_name,
        )

    def list_documents(self) -> Iterator[S3Document]:
        """
        List PDF documents from the configured S3 prefix.
        """

        continuation_token: str | None = None

        while True:

            kwargs = {
                "Bucket": self.bucket_name,
                "Prefix": self.prefix,
            }

            if continuation_token:
                kwargs["ContinuationToken"] = continuation_token

            try:
                response = self.client.list_objects_v2(
                    **kwargs
                )

            except (ClientError, BotoCoreError) as exc:
                raise RuntimeError(
                    "Unable to list documents from S3."
                ) from exc

            for item in response.get("Contents", []):

                key = item["Key"]

                # Ignore folders.
                if key.endswith("/"):
                    continue

                # Only process PDFs.
                if not key.lower().endswith(".pdf"):
                    continue

                yield S3Document(
                    bucket=self.bucket_name,
                    key=key,
                    etag=item.get("ETag"),
                    size=item.get("Size", 0),
                    last_modified=item["LastModified"],
                )

            if not response.get("IsTruncated"):
                break

            continuation_token = response.get(
                "NextContinuationToken"
            )

    def download_document(
        self,
        document: S3Document,
        destination: Path,
    ) -> Path:
        """
        Download an S3 PDF to a temporary local location.
        """

        destination.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        try:
            self.client.download_file(
                document.bucket,
                document.key,
                str(destination),
            )

        except (ClientError, BotoCoreError) as exc:
            raise RuntimeError(
                f"Unable to download S3 object: {document.key}"
            ) from exc

        return destination

    def get_object_metadata(
        self,
        document: S3Document,
    ) -> dict:
        """
        Retrieve metadata for an S3 object.
        """

        try:
            response = self.client.head_object(
                Bucket=document.bucket,
                Key=document.key,
            )

        except (ClientError, BotoCoreError) as exc:
            raise RuntimeError(
                f"Unable to read metadata for: {document.key}"
            ) from exc

        return {
            "content_type": response.get("ContentType"),
            "content_length": response.get("ContentLength"),
            "etag": response.get("ETag"),
            "last_modified": response.get("LastModified"),
        }