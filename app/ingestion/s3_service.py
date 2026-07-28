from pathlib import Path

from app.config import settings
from app.ingestion.s3_client import S3Client


class S3Service:

    def __init__(self):
        self.client = S3Client.get_client()
        self.bucket = settings.S3_BUCKET_NAME

    def list_pdf_files(self):

        response = self.client.list_objects_v2(
            Bucket=self.bucket
        )

        pdf_files = []

        if "Contents" in response:
            for obj in response["Contents"]:

                key = obj["Key"]

                if key.lower().endswith(".pdf"):
                    pdf_files.append(key)

        return pdf_files

    def download_pdf(self, s3_key, local_folder="data/temp_pdfs"):

        local_path = Path(local_folder) / Path(s3_key)

        local_path.parent.mkdir(parents=True, exist_ok=True)

        self.client.download_file(
            self.bucket,
            s3_key,
            str(local_path)
        )

        return str(local_path)

    def delete_local_pdf(self, local_path):

        file_path = Path(local_path)

        if file_path.exists():
            file_path.unlink()


if __name__ == "__main__":

    service = S3Service()

    print(f"\nBucket : {service.bucket}")

    pdf_files = service.list_pdf_files()

    print(f"Total PDF Files : {len(pdf_files)}\n")

    # Download only one file at a time
    for index, s3_key in enumerate(pdf_files, start=1):

        print(f"[{index}] Processing : {s3_key}")

        # Download PDF
        local_pdf = service.download_pdf(s3_key)

        country = Path(s3_key).parts[0]

        print(f"Country      : {country}")
        print(f"Local File   : {local_pdf}")

        # Stop here.
        # Next step is:
        # PDFLoader -> ChunkService -> EmbeddingService -> PineconeService

        break