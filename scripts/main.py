# import json
import os  # noqa: F401
import pandas as pd  # noqa: F401

from preprocessing import preprocess_data
from scoring import assign_credit_scores
from utils import load_data, save_scores

DATA_PATH = '../data/sample_transactions.json'
OUTPUT_PATH = 'outputs/credit_scores.csv'


def main():
    # Step 1: Load raw transaction data
    print("🔍 Loading raw data...")
    raw_data = load_data(DATA_PATH)
    print(f"✅ Raw data records loaded: {len(raw_data)}")

    # Step 2: Preprocess data to extract features
    print("🧼 Preprocessing data...")
    processed_df = preprocess_data(raw_data)
    print(f"✅ Processed rows: {len(processed_df)}")
    
    # Step 3: Assign credit scores based on behavior
    print("🔢 Assigning credit scores...")
    scored_df = assign_credit_scores(processed_df)
    print(f"✅ Scored records: {len(scored_df)}")

    # Step 4: Save results
    print("💾 Saving to output file...")
    save_scores(scored_df, OUTPUT_PATH)
    print(f"✅ Done! Credit scores saved to: {OUTPUT_PATH}")


# 👇 This line actually runs the code above
if __name__ == "__main__":
    main()

