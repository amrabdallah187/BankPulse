import os
import pandas as pd
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas
import sys

def load_csv_to_snowflake(file_path: str, table_name: str):
    """
    Connects to Snowflake and uploads a pandas DataFrame from a CSV file into a specified table.
    """
    try:
        print(f"--- Starting upload for {file_path} to table {table_name} ---")
        
        # --- 1. Connect to Snowflake using environment variables ---
        print("🔐 Connecting to Snowflake...")
        conn = snowflake.connector.connect(
            user=os.getenv("SNOWFLAKE_USER"),
            password=os.getenv("SNOWFLAKE_PASSWORD"),
            account=os.getenv("SNOWFLAKE_ACCOUNT"),
            warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
            database=os.getenv("SNOWFLAKE_DATABASE"),
            schema=os.getenv("SNOWFLAKE_SCHEMA")
        )
        print("✅ Connection successful.")

        # --- 2. Load and Prepare Data ---
        print(f"📄 Reading CSV file: {file_path}")
        df = pd.read_csv(file_path)
        
        # Snowflake table names are case-insensitive by default and often stored as uppercase.
        # It's a good practice to standardize column names to uppercase to avoid issues.
        df.columns = [col.upper() for col in df.columns]
        print(f"   - Found {len(df)} rows and {len(df.columns)} columns.")

        # --- 3. Upload the DataFrame to Snowflake ---
        print(f"🚀 Uploading data to Snowflake table: {table_name.upper()}...")
        success, nchunks, nrows, _ = write_pandas(
            conn=conn,
            df=df,
            table_name=table_name.upper(),
            auto_create_table=True, # Automatically create the table if it doesn't exist
            overwrite=True # Overwrite the table if it already exists
        )
        
        if success:
            print(f"✅ Successfully uploaded {nrows} rows in {nchunks} chunks.")
        else:
            print(f"❌ Upload failed.")

    except Exception as e:
        print(f"🔥 An error occurred: {e}")
        sys.exit(1)
    finally:
        if 'conn' in locals() and conn:
            conn.close()
            print("🔒 Connection closed.")
    print("-" * 50)


if __name__ == "__main__":
    # We define which files to upload and what to name their tables in Snowflake
    datasets_to_upload = {
        "data/raw/fx_rates.csv": "FX_RATES_RAW",
        "data/raw/worldbank_economic_data.csv": "WORLDBANK_ECONOMIC_DATA_RAW",
        "data/raw/credit_risk_dataset.csv": "CREDIT_RISK_RAW"
    }
    
    for file, table in datasets_to_upload.items():
        load_csv_to_snowflake(file_path=file, table_name=table)

    print("\n🎉 All datasets have been processed!")
