import pandas as pd
import boto3
import io
from datetime import datetime

def lambda_handler(event, context):
    
    s3_client = boto3.client('s3')
    AWS_S3_BUCKET = 'crisis-detection-bucket-ronel'
    AWS_S3_Key = 'incremental_train_data/batch_'+datetime.now().strftime("%Y%m%d_%H%M%S")+'.csv'
    
    # parse event
    target = [i['target'] for i in event]
    text = [i['text'] for i in event]
    
    # create df
    df = pd.DataFrame({'target':target,'text':text})
    
    # write df to s3
    with io.StringIO() as csv_buffer:
        df.to_csv(csv_buffer, index=False)
    
        response = s3_client.put_object(
            Bucket=AWS_S3_BUCKET, Key=AWS_S3_Key, Body=csv_buffer.getvalue()
        )
    
        status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")
    
        if status == 200:
            print(f"Successful S3 put_object response. Status - {status}")
        else:
            print(f"Unsuccessful S3 put_object response. Status - {status}")
    