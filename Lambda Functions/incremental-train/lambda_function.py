import json
import pandas as pd
import boto3
import io
import time
import uuid
import tarfile
import os
from datetime import datetime


### CHANGE bucket
### CHANGE role

def get_execution_role():
    iam_client = boto3.client('iam')
    response = iam_client.list_roles()
    roles = response['Roles']
    for role in roles:
        if 'Crisis_Detection' in role['RoleName']: # CHANGE THIS
            return role['Arn']

def lambda_handler(event, context):
    role = get_execution_role()
    
    bucket = 'crisis-detection'
    file = create_and_upload(bucket, event)
    step = incremental_train(bucket, role, file)

    return {
        'statusCode': 200,
        'body': json.dumps(step)
    }

def create_and_upload(bucket, event):
    # retrieve new data from S3
    s3 = boto3.client('s3')


    suffix = datetime.now().strftime("%Y%m%d_%H%M%S")+'.csv'
    file = 'incremental_train_data/batch_'+ suffix
    
    # parse event
    target = [i['target'] for i in event]
    text = [i['text'] for i in event]
    
    # create df
    df = pd.DataFrame({'target':target,'text':text})
    df_csv = df.to_csv(index=False)
    
    # Upload the file to S3
    s3.put_object(Body=df_csv, Bucket=bucket, Key=file)

    tar_filename = '/tmp/sourcedir.tar.gz'
    with tarfile.open(tar_filename, 'w:gz') as tar:
        tar.add('incremental.py')
        tar.add('utils.py')

    with open(tar_filename, 'rb') as file2:
        tar_content = file2.read()

    s3.put_object(Body=tar_content, Bucket=bucket, Key='code_incremental/{}'.format(os.path.basename(tar_filename)))

    return file
    
def incremental_train(bucket, role, file):

    prefix = 'model_incremental'
    region = boto3.Session().region_name
    client = boto3.client("sagemaker", region_name=region)
    
    # Create a unique job name
    unique_suffix = f'{int(time.time())}-{uuid.uuid4().hex[:8]}'
    job_name = 'sagemaker-crisis-detection-job-{}'.format(unique_suffix)
    output_path = 's3://{}/{}'.format(bucket, prefix)
    instance_type = 'ml.m5.large'

    #create sagemaker client
    sagemaker_client = boto3.client('sagemaker')

    #define params
    training_params = {
        'AlgorithmSpecification': {
            'TrainingImage': '683313688378.dkr.ecr.us-east-1.amazonaws.com/sagemaker-scikit-learn:1.2-1-cpu-py3',
            'TrainingInputMode': 'File'
        },
        'RoleArn': role,
        'OutputDataConfig': {
            'S3OutputPath': output_path
        },
        'ResourceConfig': {
            'InstanceCount': 1,
            'InstanceType': instance_type,
            'VolumeSizeInGB': 30
        },
        'TrainingJobName': job_name,
        'HyperParameters': {
            'sagemaker_container_log_level': '20',
            'sagemaker_job_name': job_name,
            'sagemaker_program': 'incremental.py',
            'sagemaker_region': 'us-east-1',
            'sagemaker_submit_directory': 's3://{}/code_incremental/sourcedir.tar.gz'.format(bucket),
        },
        'StoppingCondition': {
            'MaxRuntimeInSeconds': 86400
        },
        'InputDataConfig': [
            {
                'ChannelName': 'train',
                'DataSource': {
                    'S3DataSource': {
                        'S3DataType': 'S3Prefix',
                        'S3Uri': 's3://{}/{}'.format(bucket, file),
                        'S3DataDistributionType': 'FullyReplicated'
                    }
                },
                'ContentType': 'text/csv',
                'CompressionType': 'None',
                'RecordWrapperType': 'None'
            }
        ],
    }

    try:
        sagemaker_client.create_training_job(**training_params)
    except Exception as e:
        return str(e)

    return 'Incremental training triggered successfully'
    

