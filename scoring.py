import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# Step 1: Load the feature data
df = pd.read_csv("wallet_features.csv")

# Step 2: Normalize features
scaler = MinMaxScaler()
df[['norm_borrowed', 'norm_liquidations', 'norm_ratio']] = scaler.fit_transform(
    df[['total_borrowed', 'liquidations', 'borrow_supply_ratio']]
)

# Step 3: Invert risky features to calculate score
df['risk_score'] = 1000 * (
    1
    - (0.5 * df['norm_borrowed'])    # Borrowing = Risky
    - (0.3 * df['norm_liquidations'])  # Liquidation = Very Risky
    - (0.2 * df['norm_ratio'])         # High borrow/supply ratio = Risky
)

# Step 4: Final formatting
df['risk_score'] = df['risk_score'].round().astype(int)
final_df = df[['wallet_id', 'risk_score']].rename(columns={'risk_score': 'score'})

# Step 5: Save final output
final_df.to_csv("wallet_scores.csv", index=False)
print("✅ Risk scores saved to wallet_scores.csv")
print(final_df.head())
