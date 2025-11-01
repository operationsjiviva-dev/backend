import boto3
from config.settings import AWS_S3_KEY, AWS_S3_SECRET


class AWSS3:

    @classmethod
    def get_client(cls):
        client = boto3.client("s3", region_name="ap-south-1", aws_access_key_id=AWS_S3_KEY,
                              aws_secret_access_key=AWS_S3_SECRET)
        return client
