import time
import argparse, os, glob
import pandas as pd
from sklearn.experimental import enable_halving_search_cv
from sklearn.model_selection import HalvingRandomSearchCV, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.compose import ColumnTransformer
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix, classification_report
from utils import load_data, save_model
import joblib
import tarfile
import json
import boto3

def get_latest_folder(bucket_name, prefix):
    s3 = boto3.client('s3')
    
    # List objects in the bucket with the specified prefix
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix, Delimiter='/')
    
    # Extract the folders from the response
    folders = [folder['Prefix'] for folder in response.get('CommonPrefixes', [])]
    
    qualified_folders = []

    for folder in folders:
        output_folder = folder + 'output/'
        response = s3.list_objects_v2(Bucket=bucket_name, Prefix=output_folder)

        if 'Contents' in response:
            qualified_folders.append(folder)
            
    sorted_folders = sorted(qualified_folders, reverse=True)

    if sorted_folders:
        return sorted_folders[0]
    else:
        return None

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--sm-model-dir", type=str, default=os.environ.get("SM_MODEL_DIR"))
    parser.add_argument('--model-dir', type=str, default=os.environ.get('SM_MODEL_DIR'))
    parser.add_argument("--train", type=str, default=os.environ.get("SM_CHANNEL_TRAIN"))

    bucket_name = 'crisis-detection-bucket'
    prefix = 'model/'
    args, _ = parser.parse_known_args()
    model_dir = args.model_dir
    sm_model_dir = args.sm_model_dir
    training_dir = args.train
    train_data = glob.glob(os.path.join(training_dir, "*.csv"))[0]
    old_model_dir = get_latest_folder(bucket_name, prefix)
    
    print(train_data)
    print(old_model_dir)

    # Extract the model file from the tar.gz archive
    s3 = boto3.client('s3')
    local_file_path = 'model.tar.gz'
    s3.download_file(bucket_name, old_model_dir+'output/'+local_file_path, local_file_path)
    with tarfile.open(local_file_path, 'r:gz') as tar:
        tar.extractall('.')
        
    # Load the trained model
    model = joblib.load('model.joblib')
    
    # Load training data
    df = load_data(train_data)
    X = df.drop(['id', 'target', 'keyword','location'], axis=1, errors='ignore')
    y = df['target']
    
    # Check model predictive score on new data first
    y_pred = model.predict(X)
    f1 = f1_score(y, y_pred, average='binary')
    print('F1 Score Before Partial Fit: {:.4f}'.format(f1))
    
    # Partial fit the new data
    X_train = model.named_steps['col_transformer'].transform(X)
    model.named_steps['clf'].partial_fit(X_train, y)
    
    # Evaluate the new model on the new data again
    y_pred = model.predict(X)
    f1 = f1_score(y, y_pred, average='binary')
    print('F1 Score After Partial Fit on New Data: {:.4f}'.format(f1))

    # Save the best model
    save_model(model, sm_model_dir)

if __name__ == '__main__':
    main()

# Model serving
"""
Deserialize fitted model
"""
def model_fn(model_dir):
    model = joblib.load(os.path.join(model_dir, "model.joblib"))
    return model

"""
input_fn
    request_body: The body of the request sent to the model.
    request_content_type: (string) specifies the format/variable type of the request
"""
def input_fn(request_body, request_content_type):
    if request_content_type == "application/json":
        request_body = json.loads(request_body)
        inpVar = request_body["Input"]
        df = pd.DataFrame({"text": inpVar})  # Convert inpVar to DataFrame with "text" column
        return df
    else:
        raise ValueError("This model only supports application/json input")

"""
predict_fn
    input_data: returned array from input_fn above
    model (sklearn model) returned model loaded from model_fn above
"""
def predict_fn(input_data, model):
    probabilities = model.predict_proba(input_data)  # Predict class probabilities
    predictions = model.predict(input_data)  # Predict class labels
    return predictions, probabilities

"""
output_fn
    prediction: the returned value from predict_fn above
    content_type: the content type the endpoint expects to be returned. Ex: JSON, string
"""
def output_fn(prediction, content_type):
    labels, probabilities = prediction

    # Convert predictions and probabilities to list format
    labels = [int(label) for label in labels]
    probabilities = probabilities.tolist()

    respJSON = {"Output": labels, "Probabilities": probabilities}
    return respJSON
