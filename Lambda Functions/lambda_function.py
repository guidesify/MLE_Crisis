import json
import pandas as pd
import boto3
import io
import time
import uuid
import tarfile
import os

def lambda_handler(event, context):
    bucket = 'crisis-detection-2'
        
    # TODO implement
    step = "error"
    
    # try:
    file = create_and_upload(bucket)
    step = "Upload Complete, file path is {}".format(file)

    role = get_execution_role()
    step = "Execution role is {}".format(role)

    step = train_model(bucket, role, file)

    return {
        'statusCode': 200,
        'body': json.dumps(step)
    }
    # except:
    #     return { 
    #         'statusCode': 400, 
    #         'body': json.dumps(step) 
            
    #     }


def create_and_upload(bucket):
    s3 = boto3.client('s3')
    s3.create_bucket(Bucket=bucket)
    
    df = pd.read_csv('data.csv')
    df = df[['target', 'text']]
    
    # Write DataFrame to a CSV file in memory (StringIO)
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    
    # Encode the CSV content as bytes before uploading
    csv_content = csv_buffer.getvalue().encode('utf-8')
    
    # Upload the encoded CSV content to S3
    file = 'batch_1/batch_1.csv'
    s3.put_object(Body=csv_content, Bucket=bucket, Key=file)
    
    # Upload code to S3
    tar_filename = '/tmp/sourcedir.tar.gz'
    with tarfile.open(tar_filename, 'w:gz') as tar:
        tar.add('train.py')
        tar.add('utils.py')
    
    with open(tar_filename, 'rb') as file2:
        tar_content = file2.read()
    
    s3.put_object(Body=tar_content, Bucket=bucket, Key='code/{}'.format(os.path.basename(tar_filename)))

    return file


def get_execution_role():
    iam_client = boto3.client('iam')
    response = iam_client.list_roles()
    roles = response['Roles']
    for role in roles:
        if 'crisis-detection' in role['RoleName']:
            return role['Arn']


def train_model(bucket, role, file):
    # Define the training script and dependencies
    train_script = 'train.py'  # Replace with your actual training script name
    dependencies = ['utils.py']  # Replace with your required dependencies
    
    # Set up the training job configuration
    prefix = 'model'
    

    # Generate a unique suffix using timestamp and random string
    unique_suffix = f'{int(time.time())}-{uuid.uuid4().hex[:8]}'
    
    # Create a unique job name by appending the suffix
    job_name = f'sagemaker-crisis-detection-job-{unique_suffix}'
    code_location = "s3://{}/jobs".format(bucket)
    output_path = "s3://{}/{}".format(bucket, prefix)
    instance_type = 'ml.c5.xlarge'
    
    # Create the SageMaker client
    sagemaker_client = boto3.client('sagemaker')
    
    # Define the training job parameters
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
            'sagemaker_program': 'train.py',
            'sagemaker_region': 'us-east-1',
            'sagemaker_submit_directory': 's3://{}/code/sourcedir.tar.gz'.format(bucket),
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
        ]
    }
    
    # Create the SageMaker training job
    try:
        sagemaker_client.create_training_job(**training_params)
    except Exception as e:
        return str(e)
    
    return "Training job created successfully."