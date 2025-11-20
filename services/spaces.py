import os
import boto3
from fastapi import UploadFile

ACCESS_KEY = os.environ.get("DO_SPACES_KEY")
SECRET_KEY = os.environ.get("DO_SPACES_SECRET")
ENDPOINT_URL = os.environ.get("DO_SPACES_ENDPOINT_URL")
BUCKET_NAME = os.environ.get("DO_SPACES_BUCKET_NAME")

s3 = boto3.client(
    's3',
    endpoint_url=ENDPOINT_URL,
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
)

def upload_file_to_space(file: UploadFile, object_name: str, content_type: str) -> str:
    try:
        s3.upload_fileobj(
            Fileobj=file.file,
            Bucket=BUCKET_NAME,
            Key=object_name, 
            ExtraArgs={
                'ACL': 'public-read', 
                'ContentType': content_type 
            }
        )
        file_url = f"{ENDPOINT_URL}/{BUCKET_NAME}/{object_name}"
        return file_url
    except Exception as e:
        print(f"Error al subir a Spaces: {e}")
        return None