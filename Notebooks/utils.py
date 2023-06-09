import os
import pandas as pd
import joblib

def load_data(file_path):
    # Load data from CSV file
    data = pd.read_csv(file_path)
    return data

def save_model(model, save_dir):
    # Save the trained model to a directory
    joblib.dump(model, os.path.join(save_dir, "model.joblib"))
    print('Model saved to {}'.format(save_dir))
