import pathlib
from datetime import datetime

import boto3
from botocore.exceptions import NoCredentialsError


class S3Client:
    def __init__(self, config: dict):
        self.s3_client = boto3.client('s3')
        self.config = config

    def upload_file(self, file_path: pathlib.Path, object_name=None):
        """Uploads a file to an S3 bucket."""
        if object_name is None:
            object_name = file_path.name

        bucket_name = self.config['aws']['s3_bucket_name']        
        try:
            self.s3_client.upload_file(file_path, bucket_name, object_name)
            print(f"File {file_path} uploaded to s3://{bucket_name}/{object_name}")
        except NoCredentialsError:
            print("AWS credentials not found!")
        except Exception as e:
            print(f"An error occurred: {e}")
            self.s3_client.upload_file(file_path, bucket_name, object_name)

            print(f"An error occurred: {e}")
            self.s3_client.upload_file(file_path, bucket_name, object_name)
            print(f"An error occurred: {e}")