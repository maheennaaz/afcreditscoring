import pandas as pd


def compute_credit_score(df):
    """
    Computes credit score (0–1000)
    based on user wallet behavior from preprocessed data.
    Emphasizes repayment behavior, 
    penalizes liquidations, and considers net borrowing.
    """
    scores = {}

    for _, row in df.iterrows():
        wallet = row['wallet']
        num_deposits = row.get('num_deposits', 0)
        num_borrows = row.get('num_borrows', 0)
        num_repays = row.get('num_repays', 0)
        num_redeems = row.get('num_redeems', 0)
        num_liquidations = row.get('num_liquidations', 0)
        total_borrow_amount = row.get('total_borrow_amount', 0)
        total_repay_amount = row.get('total_repay_amount', 0)

        # Defensive checks
        net_borrow = total_borrow_amount - total_repay_amount
        net_borrow = max(net_borrow, 0)

        # Enhanced scoring logic
        score = (
            num_deposits * 8 +                     # Incentivize deposits
            num_repays * 20 +                     
            # Strong reward for repayments
            (total_repay_amount * 0.005) -         
            # Repayment amount helps
            (net_borrow * 0.01) -                  
            # Penalize outstanding borrow
            num_borrows * 5 -                      
            # Light penalty for borrowing
            num_redeems * 2 -                      
            # Light penalty for redeeming
            num_liquidations * 30                
            # Heavy penalty for liquidation
        )

        # Normalize to 0–1000 scale
        score = max(0, min(1000, int(score)))
        scores[wallet] = score

    credit_scores_df = pd.DataFrame(scores.items(), columns=[
        "userWallet", "creditScore"])
    return credit_scores_df


# Wrapper for main.py compatibility
def assign_credit_scores(df):
    return compute_credit_score(df)
