import pandas as pd
import json
import os


def load_data(filepath):
    with open(filepath, 'r') as file:
        data = json.load(file)
    df = pd.json_normalize(data)  # Flatten nested JSON into columns
    return df


def save_scores(df, filepath):
    # Ensure the directory exists
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    # Save the CSV
    df.to_csv(filepath, index=False)
    print(f"✅ Credit scores saved to: {filepath}")