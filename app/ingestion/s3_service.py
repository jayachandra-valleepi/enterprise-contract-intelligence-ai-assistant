from pathlib import Path

from app.ingestion.downloader import Downloader
from app.ingestion.metadata_service import MetadataServices
from app.ingestion.paginator import S3Paginator


class S3Service:

    def __init__(self, client):
        self.client = client
        self.downloader = Downloader(client)
        self.metadata = MetadataServices(client)
        self.paginator = S3Paginator(client)

    def download_pdfs(self, bucket):

        metadata_list = []

        # Create the data folder if it doesn't exist
        data_folder = Path("data")
        data_folder.mkdir(parents=True, exist_ok=True)

        for page in self.paginator.get_pages(bucket):

            if "Contents" not in page:
                continue

            for obj in page["Contents"]:

                key = obj["Key"]

                # Skip folders
                if key.endswith("/"):
                    continue

                # Download only PDF files
                if not key.lower().endswith(".pdf"):
                    continue

                # Get country from S3 path
                country = key.split("/")[0]

                # Get PDF file name
                file_name = Path(key).name

                # Create country folder
                country_folder = data_folder / country
                country_folder.mkdir(parents=True, exist_ok=True)

                # Local download path
                local_path = country_folder / file_name

                print(f"Downloading: {key}")

                # Download PDF
                self.downloader.download(
                    bucket,
                    key,
                    local_path
                )

                # Read metadata
                metadata = self.metadata.get_metadata(
                    bucket,
                    key,
                    local_path
                )

                metadata_list.append(metadata)

                print(f"Downloaded: {local_path}")

        return metadata_list