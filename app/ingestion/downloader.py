from pathlib import Path

class Downloader:

    def __init__(self, client):
        self.client = client

    def download(self, bucket, key, local_path):

        Path(local_path).parent.mkdir(
            parents=True,
            exist_ok=True
        )

        print(f"Downloading {key}")

        self.client.download_file(
            Bucket=bucket,
            Key=key,
            Filename=str(local_path)
        )

        print("Downloaded Successfully")