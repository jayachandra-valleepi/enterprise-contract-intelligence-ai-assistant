from app.ingestion.s3_client import S3Client
from app.ingestion.s3_service import S3Service
from app.config import settings

BUCKET_NAME = settings.S3_BUCKET_NAME
TEMP_FOLDER = "temp"


def main():
    client = S3Client.get_client()

    service = S3Service(client)

    metadata = service.download_pdfs(
        bucket=BUCKET_NAME
    )

    print(f"Downloaded {len(metadata)} PDF(s).")


if __name__ == "__main__":
    main()