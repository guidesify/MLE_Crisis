from sagemaker.sklearn import SKLearn

def lambda_handler(event, context):
    # Set the paths and filenames
    train_script = 'train.py'  # Replace with the actual filename of your train script
    utilities_script = ['utils.py']  # Replace with the actual filename(s) of your dependencies
    batch_path = 's3://your-bucket-name/base.csv'  # Replace with the actual S3 path of your base.csv file

    # Call the train_model function
    trained_model = model_training(train_script, utilities_script, batch_path)

    # Perform any further processing or handling of the trained model as needed

    return {
        'statusCode': 200,
        'body': 'Training completed successfully'
    }