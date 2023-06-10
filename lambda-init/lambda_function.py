import boto3
import pandas as pd
from init_proj import init_data

def lambda_handler(event, context):

    # Store the preprocessed data in S3
    s3 = boto3.client('s3')
    bucket_name = 'crisis-detection-bucket-1' # <--- CHANGE THIS VARIABLE TO A UNIQUE NAME FOR YOUR BUCKET
    file_name = 'base.csv'
    
    dataset = pd.read_csv('data.csv')
    df = init_data(dataset)
    
    # Convert DataFrame to CSV
    preprocessed_data_csv = df.to_csv(index=False)
    
    # Upload the file to S3
    s3.put_object(Body=preprocessed_data_csv, Bucket=bucket_name, Key=file_name)

    return {
        'statusCode': 200,
        'body': 'Preprocessed data stored in S3'
    }