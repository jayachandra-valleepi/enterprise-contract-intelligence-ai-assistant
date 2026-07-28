from dotenv import load_dotenv
import os

load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_DEFAULT_REGION")

S3_BUCKET_NAME = os.getenv("AWS_S3_BUCKET_NAM")
S3_PREFIX = os.getenv("S3_PREFIX")