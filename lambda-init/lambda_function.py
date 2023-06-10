import boto3
import pandas as pd
from init_proj import init_proj, train_model

# import sagemaker

def lambda_handler(event, context):

    # Store the preprocessed data in S3
    s3 = boto3.client('s3')
    bucket_name = 'crisis-detection-bucket-1' # <--- CHANGE THIS VARIABLE TO A UNIQUE NAME FOR YOUR BUCKET

    file_name = 'base.csv'
    
    dataset = pd.read_csv('data.csv')
    df = init_proj(dataset)
    
    # Convert DataFrame to CSV
    preprocessed_data_csv = df.to_csv(index=False)
    
    # Upload the file to S3
    s3.put_object(Body=preprocessed_data_csv, Bucket=bucket_name, Key=file_name)

    # sagemaker_session = sagemaker.Session()
    sagemaker_session = boto3.client('sagemaker')
    print('1')
    session = boto3.Session()
    sts_client = session.client('sts')
    response = sts_client.get_caller_identity()
    print('2)')
    role_arn = response['Arn']
    sagemaker_session = session.client('sagemaker')
    print('3')
    # role = sagemaker_session.get_execution_role()
    base_model = train_model('train.py', ['utils.py'], 's3://crisis-detection-bucket-1/base.csv', role_arn, sagemaker_session, bucket_name)
    print('4')

    return {
        'statusCode': 200,
        'body': str(response) # 'Preprocessed data stored in S3'
    }