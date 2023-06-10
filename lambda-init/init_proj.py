import boto3
import pandas as pd
import numpy as np

# from sklearn.model_selection import train_test_split
# from sagemaker.sklearn import SKLearn

# Create an S3 client
s3_client = boto3.client('s3')

# Specify a unique bucket name
bucket_name = 'crisis-detection-bucket-1' # <--- CHANGE THIS VARIABLE TO A UNIQUE NAME FOR YOUR BUCKET

def init_proj(data_path):

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


def train_model(train_script, dependencies_script, batch_path, role, sagemaker_session, bucket_name):
    # Set up the SKLearn estimator with dependencies
    sk_estimator = SKLearn(
        entry_point=train_script,
        dependencies=dependencies_script,
        role=role,
        instance_count=1,
        instance_type="ml.c5.xlarge",
        framework_version="1.2-1",
        script_mode=True,
        py_version='py3',
        sagemaker_session=sagemaker_session,
        output_path="s3://{}/{}".format(bucket_name, prefix),
        base_job_name= "sagemaker-crisis-detection",
        code_location= "s3://{}/{}".format(bucket_name, "jobs")
    
    )

    # Train the model
    print(batch_path)
    s3_input = TrainingInput(batch_path)
    sk_estimator.fit({'train': s3_input}, wait=False)

    return sk_estimator