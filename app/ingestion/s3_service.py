import boto3
from pathlib import Path

from app.Config.settings import settings


class S3Service:

    def __init__(self):

        self.bucket_name = settings.AWS_S3_BUCKET_NAME

        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_DEFAULT_REGION
        )

    # --------------------------------------------------
    # LIST PDF FILES
    # --------------------------------------------------

    def list_pdf_files(self, prefix: str = ""):

        pdf_files = []

        paginator = self.s3_client.get_paginator(
            "list_objects_v2"
        )

        pages = paginator.paginate(
            Bucket=self.bucket_name,
            Prefix=prefix
        )

        for page in pages:

            for obj in page.get("Contents", []):

                key = obj["Key"]

                if key.lower().endswith(".pdf"):
                    pdf_files.append(key)

        return pdf_files

    # --------------------------------------------------
    # DOWNLOAD PDF
    # --------------------------------------------------

    def download_pdf(
        self,
        s3_key: str,
        local_folder: str = "data/raw"
    ):

        # Example:
        # s3_key = "France/Page_12.pdf"

        s3_path = Path(s3_key)

        # Get country name
        # France
        country = s3_path.parts[0]

        # Get PDF name
        # Page_12.pdf
        file_name = s3_path.name

        # Create country folder
        # data/raw/France
        country_folder = Path(local_folder) / country

        country_folder.mkdir(
            parents=True,
            exist_ok=True
        )

        # Final path
        # data/raw/France/Page_12.pdf
        local_path = country_folder / file_name

        print(f"Downloading: {s3_key}")
        print(f"Saving to: {local_path}")

        self.s3_client.download_file(
            self.bucket_name,
            s3_key,
            str(local_path)
        )

        return str(local_path)

    # --------------------------------------------------
    # GET PDF METADATA
    # --------------------------------------------------

    def get_file_metadata(self, s3_key: str):

        response = self.s3_client.head_object(
            Bucket=self.bucket_name,
            Key=s3_key
        )

        return {
            "s3_key": s3_key,
            "size": response.get("ContentLength"),
            "last_modified": response.get("LastModified"),
            "etag": response.get("ETag")
        }

    # --------------------------------------------------
    # DOWNLOAD ALL PDFs
    # --------------------------------------------------

    def download_all_pdfs(
        self,
        prefix: str = "",
        local_folder: str = "data/raw"
    ):

        pdf_files = self.list_pdf_files(prefix)

        downloaded_files = []

        for s3_key in pdf_files:

            local_path = self.download_pdf(
                s3_key=s3_key,
                local_folder=local_folder
            )

            downloaded_files.append({
                "s3_key": s3_key,
                "local_path": local_path
            })

        return downloaded_files