import requests
import pandas as pd
from pathlib import Path
import sys

# --- Configuration ---
INDICATORS = {
    "NY.GDP.MKTP.CD": "gdp_current_usd",
    "FP.CPI.TOTL.ZG": "inflation_annual_perc",
    "FR.INR.DPOL": "policy_interest_rate_perc"
}
COUNTRIES = ["EG", "US", "GB", "DE"]
DATE_RANGE = "2010:2023"

# --- Setup Directories ---
RAW_DATA_DIR = Path("data") / "raw"
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_PATH = RAW_DATA_DIR / "worldbank_economic_data.csv"


# --- Main Script ---
def fetch_world_bank_data():
    """
    Fetches indicators from the World Bank API, making a separate request for each indicator
    to ensure robustness against missing data.
    """
    print("📡 Fetching economic data from the World Bank API (one indicator at a time)...")
    
    all_dataframes = []
    countries_str = ";".join(COUNTRIES)

    for indicator_code, indicator_name in INDICATORS.items():
        print(f"   - Fetching '{indicator_name}'...")
        
        url = f"http://api.worldbank.org/v2/country/{countries_str}/indicator/{indicator_code}"
        params = {
            "date": DATE_RANGE,
            "format": "json",
            "per_page": 2000
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            # Check if the response is valid and contains data
            if not response.json() or len(response.json()) < 2 or not response.json()[1]:
                print(f"   - ⚠️  Warning: No data returned for '{indicator_name}'. Skipping.")
                continue

            data = response.json()[1]
            df = pd.DataFrame(data)
            all_dataframes.append(df)

        except requests.exceptions.RequestException as e:
            print(f"   - ❌ Error fetching '{indicator_name}': {e}. Skipping.")
            continue

    if not all_dataframes:
        print("\n❌ Critical: Failed to fetch any data from the World Bank API. Exiting.")
        sys.exit(1)
        
    print("\n✅ All available data has been fetched.")
    
    # Combine all the collected data into a single DataFrame
    full_df = pd.concat(all_dataframes, ignore_index=True)

    # --- Data Cleaning and Transformation ---
    df = full_df[['country', 'date', 'indicator', 'value']]
    df.rename(columns={'country': 'country_name', 'date': 'year', 'indicator': 'indicator_name'}, inplace=True)
    df['indicator_name'] = df['indicator_name'].apply(lambda x: INDICATORS.get(x['id'], x['id']))
    df['country_name'] = df['country_name'].apply(lambda x: x['value'])

    df_pivot = df.pivot_table(
        index=['country_name', 'year'],
        columns='indicator_name',
        values='value'
    ).reset_index()
    
    df_pivot.sort_values(by=['country_name', 'year'], inplace=True)
    
    print("🔄 Processed data into a clean, wide format.")
    return df_pivot


if __name__ == "__main__":
    world_bank_df = fetch_world_bank_data()
    
    world_bank_df.to_csv(OUTPUT_PATH, index=False)
    
    print(f"\n✅ Data successfully saved to: {OUTPUT_PATH.resolve()}")
    print("\n--- Data Preview ---")
    print(world_bank_df.head())
    print("--------------------")
