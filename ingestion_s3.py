import boto3
import os
from botocore.exceptions import ClientError

def upload_file_to_s3(file_name, bucket, object_name=None):
    """
    Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    #cloud connection
    s3_client = boto3.client('s3', region_name ='us-east-1')
    print (f"Uploading {file_name} to bucket {bucket} as {object_name}...")
    try:
        s3_client.upload_file(file_name, bucket, object_name)
        print(f"Successfully uploaded {file_name} to bucket {bucket}")
        return True
    except ClientError as e:
        print(f"Error uploading {file_name}: {e}")
        return False
    return True

#script execution
bucket_name = "customers-data-hadassa-2026-landing-zone" 
local_archive = "customer_data.csv"

upload_file_to_s3(local_archive, bucket_name)