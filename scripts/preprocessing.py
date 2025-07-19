import pandas as pd
from datetime import datetime


def parse_timestamp(ts):
    try:
        return datetime.utcfromtimestamp(int(ts))
    except Exception:
        return pd.NaT


def preprocess_data(df):
    # Rename wallet column if needed
    if 'userWallet' in df.columns:
        df.rename(columns={'userWallet': 'wallet'}, inplace=True)

    # Safely parse timestamps
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s', errors='coerce')

    # Standardize action to lowercase
    df['action'] = df['action'].str.lower()

    # Convert amount field
    if 'actionData.amount' in df.columns:
        df['amount'] = pd.to_numeric(df['actionData.amount'], errors='coerce')
    elif 'amount' in df.columns:
        df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
    else:
        df['amount'] = 0

    # Drop missing values
    df.dropna(subset=['wallet', 'action'], inplace=True)

    # Filter valid actions
    df = df[df['action'].isin(['deposit', 'borrow', 'repay', 'liquidation'])]

    # Grouping and Feature Engineering
    grouped = df.groupby("wallet")

    features = pd.DataFrame()
    features["num_deposits"] = grouped.apply(lambda x: (x[
        "action"] == "deposit").sum())
    features["num_borrows"] = grouped.apply(lambda x: (x[
        "action"] == "borrow").sum())
    features["num_repays"] = grouped.apply(lambda x: (x[
        "action"] == "repay").sum())
    features["num_liquidations"] = grouped.apply(lambda x: (x[
        "action"] == "liquidation").sum())
    features["total_borrowed"] = grouped.apply(lambda x: x.loc[x[
        "action"] == "borrow", "amount"].sum())
    features["total_repaid"] = grouped.apply(lambda x: x.loc[x[
        "action"] == "repay", "amount"].sum())
    features["borrow_repay_ratio"] = features[
        "total_repaid"] / features["total_borrowed"].replace(0, 1)
    features["tx_count"] = grouped.size()
    features["avg_amount"] = grouped["amount"].mean()

    features = features.fillna(0).reset_index()
    
    return features