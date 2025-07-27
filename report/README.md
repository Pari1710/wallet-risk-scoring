# 📊 Wallet Risk Scoring from Compound V2

## 🗃️ Data Collection
The transaction-level data was extracted from Dune Analytics using Compound V2 tables.  
Due to query limitations and potential rate limits, a subset of wallet addresses was used to generate a manageable sample.
From this sample, we derived **wallet-level aggregates** such as:
- 📊 Borrow count  
- 💵 Total borrowed (USD)  
- 🔁 Repay count  
- ⚠️ Liquidation event count  

These features were **normalized**, and a final **risk score (0–100)** was computed for each wallet using a weighted scoring model.

---

### 📁 Wallet Features Dataset

The following columns were used to derive risk scores for each wallet:

| Column Name           | Description                                                                 |
|------------------------|-----------------------------------------------------------------------------|
| `wallet_id`            | Ethereum wallet address                                                     |
| `total_supplied`       | Total amount (in USD) supplied by the wallet to Compound                   |
| `total_borrowed`       | Total amount (in USD) borrowed from Compound by the wallet                 |
| `liquidations`         | Number of times the wallet was liquidated (indicating default risk)        |
| `borrow_supply_ratio`  | Ratio of total borrowed to total supplied → a higher value suggests riskier borrowing behavior |

These features were extracted and calculated to help identify **on-chain risk patterns**, especially for wallets that show signs of over-leveraging, defaults, or unstable borrowing patterns.


## 📁 Files

- `main.py`: Loads and cleans wallet data
- `scoring.py`: Applies the risk scoring model
- `wallet_features.csv`: Final aggregated data
- `report/README.md`: Project report and methodology

## 📊 Tech Used

- Python (Pandas, NumPy)
- Dune Analytics (for data sourcing)
- Git/GitHub (for version control)

## 📈 Scoring Method
Each wallet was assigned a score between **0 and 1000**, calculated based on:

- **Repay-to-Borrow Ratio** (Good behavior)
- **Liquidation Rate** (Penalty)
- **Normalized Borrow Volume** (Activity)

- **0 = Highest Risk**
- **1000 = Lowest Risk**

- Each feature was **normalized** (using min-max scaling) to bring all values to a common scale.
- A **weighted scoring formula** was applied:
  - Higher borrow & liquidation counts increase risk
  - Higher repay counts decrease risk


### Formula:
score = 0.4 * (repay_ratio) + 0.3 * (1 - liquidation_rate) + 0.3 * (normalized_borrow_volume)

The result is scaled to 0–1000 for comparability.


### ✅ Justification of Risk Indicators
- **High Borrow Volume**: Suggests greater exposure to debt and risk
- **Low Repay Count**: Indicates poor repayment behavior
- **High Liquidations**: Strong indicator of default or overleveraging
- **Balanced borrow & repay**: Suggests responsible on-chain behavior

These indicators align with common practices in decentralized credit evaluation and risk modeling.



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

## 🔮 Future Enhancements

Here are some potential improvements and extensions to the current project:

- **Real-Time Data Integration**  
  Integrate live data fetching from Compound V2/V3 using Web3, Alchemy, or Moralis for real-time risk scoring.

- **Support for Other Lending Protocols**  
  Extend the framework to support Aave, MakerDAO, and Venus to provide a more comprehensive DeFi risk profile.

- **Machine Learning Model for Scoring**  
  Train a supervised or unsupervised ML model using wallet behavior history and known risk labels (if available).

- **Dashboard / Visualization**  
  Build an interactive dashboard using Streamlit or Dash to visualize wallet scores, trends, and risks.

