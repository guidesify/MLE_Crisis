import json
import logging
import boto3
logging.getLogger().setLevel(logging.INFO)

# GIVE THE ROLE THE REQUIRED PERMISSIONS AND REMEMBER TO SET S3 AS TRIGGER
# BEWARE OF RECURSIVE INVOCATIONS
# CHANGE THE ROLE TOO BELOW IN THE get_execution_role() FUNCTION
def lambda_handler(event, context):
    # TODO implement
    bucket = str(event['Records'][0]['s3']['bucket']['name'])
    model_url = str(event['Records'][0]['s3']['object']['key'])
    job_id_start_index = model_url.find('job-') + 4
    job_id_end_index = model_url.find('/output')
    job_id = model_url[job_id_start_index:job_id_end_index]
    logging.info((bucket, model_url, job_id))
    
    region = boto3.Session().region_name
    client = boto3.client("sagemaker", region_name=region)
    sagemaker_role = get_execution_role()
    
    #Get container image (prebuilt example)
    container = '683313688378.dkr.ecr.us-east-1.amazonaws.com/sagemaker-scikit-learn:1.2-1-cpu-py3'

    #Create model
    model_name = "crisis-" + job_id

    response = client.create_model(
        ModelName = model_name,
        ExecutionRoleArn = sagemaker_role,
        Containers = [{
            "Image": container,
            "Mode": "SingleModel",
            "ModelDataUrl": 's3://{}/{}'.format(bucket,model_url),
            "Environment": {
                "SAGEMAKER_PROGRAM": "incremental.py",
                "SAGEMAKER_REGION": region,
                "SAGEMAKER_SUBMIT_DIRECTORY": 's3://{}/code_incremental/sourcedir.tar.gz'.format(bucket)
            }
        }]
    )

    
    config_name = "config-" + job_id
    response = client.create_endpoint_config(
        EndpointConfigName=config_name,
        ProductionVariants=[
        {
            "ModelName": model_name,
            "VariantName": "AllTraffic",
            "ServerlessConfig": {
                "MemorySizeInMB": 1024,
                "MaxConcurrency": 1,
            }
        } 
        ]
    )

    response = client.create_endpoint(
    EndpointName="detector-" + job_id,
    EndpointConfigName=config_name
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps(str(response))
    }

def get_execution_role():
    iam_client = boto3.client('iam')
    response = iam_client.list_roles()
    roles = response['Roles']
    for role in roles:
        if 'Crisis_Detection' in role['RoleName']: # CHANGE THIS
            return role['Arn']