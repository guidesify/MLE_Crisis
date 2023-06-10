import boto3
import pandas as pd
import numpy as np

# Create an S3 client
s3_client = boto3.client('s3')

# Specify a unique bucket name
bucket_name = 'crisis-detection-bucket-1' # <--- CHANGE THIS VARIABLE TO A UNIQUE NAME FOR YOUR BUCKET

def init_data(data_path):

    try:
        # Create the S3 bucket
        s3_client.create_bucket(Bucket=bucket_name)
        print("Bucket created successfully!")
    except ClientError as e:
        # Check if the error is due to bucket already existing
        error_code = e.response['Error']['Code']
        if error_code == 'BucketAlreadyOwnedByYou':
            print("Bucket already exists. Continuing with the existing bucket.")
        else:
            print("An error occurred while creating the bucket:", error_code)
            raise

    df = data_path[['target','text']]
    
    return df


