from app.models.document_metadata import DocumentMetadata


class MetadataServices:

    def __init__(self, client):
        self.client = client

    def get_metadata(self, bucket, key, local_path):

        response = self.client.head_object(
            Bucket=bucket,
            Key=key
        )

        return DocumentMetadata(

            file_name=key.split("/")[-1],

            country=key.split("/")[0],

            s3_key=key,

            local_path=str(local_path),

            file_size=response["ContentLength"],

            last_modified=response["LastModified"]
        )