import requests
import pandas as pd

# STEP 1: Load wallet addresses from Excel file
wallet_df = pd.read_excel("wallet_ids.xlsx")
wallets = wallet_df['wallet_id'].tolist()

# STEP 2: The Graph API endpoint for Compound V2
COMPOUND_V2_URL = "https://api.thegraph.com/subgraphs/name/graphprotocol/compound-v2"

# STEP 3: Create GraphQL query for each wallet
def build_query(wallet_address):
    return {
        "query": f"""
        {{
          account(id: "{wallet_address.lower()}") {{
            id
            tokens {{
              symbol
              supplyBalanceUnderlying
              borrowBalanceUnderlying
            }}
            liquidationCount
          }}
        }}
        """
    }

# STEP 4: Query function that handles errors
def get_wallet_data(wallet):
    query = build_query(wallet)
    response = requests.post(COMPOUND_V2_URL, json=query)

    try:
        json_data = response.json()

        if "data" not in json_data:
            print(f"❌ API error for {wallet}:")
            print(json_data)
            return None

        data = json_data["data"]["account"]
        if data is None:
            return {
                "wallet_id": wallet,
                "total_supplied": 0,
                "total_borrowed": 0,
                "liquidations": 0,
                "borrow_supply_ratio": 0
            }

        # Calculate totals
        total_supplied = sum(float(t["supplyBalanceUnderlying"]) for t in data["tokens"])
        total_borrowed = sum(float(t["borrowBalanceUnderlying"]) for t in data["tokens"])
        liquidations = int(data.get("liquidationCount", 0))
        ratio = total_borrowed / total_supplied if total_supplied > 0 else 0

        return {
            "wallet_id": wallet,
            "total_supplied": total_supplied,
            "total_borrowed": total_borrowed,
            "liquidations": liquidations,
            "borrow_supply_ratio": ratio
        }

    except Exception as e:
        print(f"❌ Failed to fetch data for {wallet}: {e}")
        return None

# STEP 5: Loop through wallets (start with just 1 to test)
results = []
for wallet in wallets[:1]:  # Change to [:100] to run on full dataset
    print(f"⏳ Processing wallet: {wallet}")
    data = get_wallet_data(wallet)
    if data:
        results.append(data)

# STEP 6: Save or display result
df = pd.DataFrame(results)
print(df)

# STEP 7: Save to intermediate CSV (optional)
df.to_csv("wallet_features_sample.csv", index=False)
print("✅ Sample data saved to wallet_features_sample.csv")
