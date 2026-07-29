from app.config import settings
from app.ingestion.s3_client import S3Client

class S3Paginator:
    def __init__(self, client):
        self.client = client

    def get_pages(self, bucket):
        paginator = self.client.get_paginator("list_objects_v2")
        return paginator.paginate(Bucket=bucket)


# if __name__ == "__main__":
#     client = S3Client.get_client()

#     paginator = S3Paginator(client)

#     pages = paginator.get_pages(settings.S3_BUCKET_NAME)

#     for page in pages:
#         if "Contents" in page:
#             for obj in page["Contents"]:
#                 print(obj["Key"])
            