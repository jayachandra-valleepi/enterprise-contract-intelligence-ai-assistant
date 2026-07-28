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

    def download_pdf(self, s3_key, local_folder="data/pdfs"):

        Path(local_folder).mkdir(parents=True, exist_ok=True)

        local_path = Path(local_folder) / Path(s3_key).name

        self.client.download_file(
            self.bucket,
            s3_key,
            str(local_path)
        )

        return str(local_path)



if __name__ == "__main__":

    service = S3Service()

    print("Bucket:", service.bucket)

    pdf_files = service.list_pdf_files()

    print(f"Total PDF Files: {len(pdf_files)}")

    for pdf in pdf_files:
        print(pdf)