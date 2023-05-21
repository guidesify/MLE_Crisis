import time
import argparse, os
import pandas as pd
from sklearn.experimental import enable_halving_search_cv
from sklearn.model_selection import HalvingRandomSearchCV, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.compose import ColumnTransformer
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix, classification_report
from utils import load_data, save_model
import joblib
import json

# Create a RandomizedSearchCV function to find the best parameters/hyperparameters tuning
def RandomizedSearchCV_function(classifier, parameters, X_train=None, y_train=None):
    start_time = time.time()
    # Define column transformer and pipeline
    column_transformer = ColumnTransformer([
        ('vect', TfidfVectorizer(analyzer='word',strip_accents=None, encoding='utf-8',preprocessor=None,ngram_range=(1, 2),token_pattern=r'(?u)\b\w[\w-]*\w\b|\b\w+\b', stop_words='english'), 'text')
    ], remainder='drop')
    pipeline = Pipeline([
        ('col_transformer', column_transformer),
        ('clf', classifier)
    ])

    # Create a randomized search cross validation and no verbose
    search_cv = HalvingRandomSearchCV(pipeline, parameters, scoring='f1', n_jobs=-1, cv=5, verbose=0, random_state=2023) 
    best_model = search_cv.fit(X_train, y_train)
    print('Best Score: {}: {}'.format(classifier.__class__.__name__, best_model.best_score_))
    print('Best Parameters: {}'.format(best_model.best_params_))
    
    print('Time taken: {:.2f} seconds'.format(time.time() - start_time))
    print('='*50)
    return best_model.best_estimator_

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--sm-model-dir", type=str, default=os.environ.get("SM_MODEL_DIR"))
    parser.add_argument("--model_dir", type=str)
    parser.add_argument("--train", type=str, default=os.environ.get("SM_CHANNEL_TRAIN"))

    args, _ = parser.parse_known_args()
    model_dir = args.model_dir
    sm_model_dir = args.sm_model_dir
    training_dir = args.train

    # Load training data
    df = load_data(training_dir + "/data.csv")
    X = df.drop(['id', 'target', 'keyword','location'], axis=1)
    y = df['target']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=2023, stratify=y)

    # Train and find the best model
    best_model = RandomizedSearchCV_function(LogisticRegression(), {'clf__C': (0.1, 0.5, 1, 10, 15, 20)}, X_train=X_train, y_train=y_train)

    # Evaluate the best model on the training data
    y_pred = best_model.predict(X_test)
    f1 = f1_score(y_test, y_pred, average='binary')
    print('F1 Score: {:.4f}'.format(f1))

    # Save the best model
    save_model(best_model, sm_model_dir)

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
