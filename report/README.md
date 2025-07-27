# 📊 Wallet Risk Scoring from Compound V2

## 🗃️ Data Collection
The transaction-level data was extracted from Dune Analytics using Compound V2 tables.  
Due to query limitations and potential rate limits, a subset of wallet addresses was used to generate a manageable sample.

## 🔍 Feature Selection
The following features were derived:
- Total Amount Borrowed (USD)
- Total Amount Repaid (USD)
- Number of Borrows
- Number of Repayments
- Number of Liquidation Events

These features were extracted from historical borrow/repay/liquidation events on-chain.

## 📈 Scoring Method
Each wallet was assigned a score between **0 and 1000**, calculated based on:

- **Repay-to-Borrow Ratio** (Good behavior)
- **Liquidation Rate** (Penalty)
- **Normalized Borrow Volume** (Activity)

### Formula:
score = 0.4 * (repay_ratio) + 0.3 * (1 - liquidation_rate) + 0.3 * (normalized_borrow_volume)

The result is scaled to 0–1000 for comparability.

## 🧾 Output Format
Final output is in `data/wallet_scores.csv`, formatted as:

wallet_id,score
0xfaa0768bde629806739c3a4620656c5d26f44ef2,732
...


## 📂 Files Included

| File/Folders              | Description                            |
|---------------------------|----------------------------------------|
| `wallet_features.csv`     | Full derived feature data              |
| `wallet_features_sample.csv` | Smaller test sample                    |
| `wallet_ids.xlsx`         | Original wallet IDs from Dune export  |
| `main.py` / `scoring.py`  | Risk scoring scripts                   |
| `data/wallet_scores.csv`  | Final output                           |
| `report/README.md`        | This report                            |

## ✅ Summary
This project estimates wallet risk scores using Compound protocol on-chain transaction behavior, providing a basis for risk-aware lending, credit evaluation, or wallet filtering.

