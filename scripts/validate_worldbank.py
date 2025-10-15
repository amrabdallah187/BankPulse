import pandas as pd
from pydantic import BaseModel, Field, ValidationError
import sys
from typing import Optional

# --- 1. Define the Expected Data Structure for a Single Row ---
# We define what a valid row of our economic data should look like.
# We use 'Optional' because some countries may not have data for all indicators in all years.
class EconomicData(BaseModel):
    country_name: str
    year: int = Field(ge=2010, le=2023) # Must be an integer between 2010 and 2023
    gdp_current_usd: Optional[float] = Field(default=None, gt=0) # If present, must be positive
    inflation_annual_perc: Optional[float] = None
    policy_interest_rate_perc: Optional[float] = None


# --- 2. Load the Data with Pandas ---
DATA_PATH = "data/raw/worldbank_economic_data.csv"
print(f"✅ Loading data from {DATA_PATH}...")
try:
    df = pd.read_csv(DATA_PATH)
except FileNotFoundError:
    print(f"❌ CRITICAL: '{DATA_PATH}' not found. Please run 'fetch_worldbank_data.py' first.")
    sys.exit(1)


# --- 3. Perform Validations ---
errors = []
print("\n🔎 Performing validations...")

# Rule 1: Check table row count
# With 4 countries over 14 years, we expect up to 56 rows. A sanity check for at least 10 is good.
if len(df) < 10:
    errors.append(f"Row count is only {len(df)}, which is unexpectedly low.")
else:
    print("   - ✅ Row count seems reasonable.")

# Rule 2: Check for unexpected missing key data
key_columns = ['country_name', 'year']
if df[key_columns].isnull().values.any():
    null_cols = df[key_columns].columns[df[key_columns].isnull().any()].tolist()
    errors.append(f"Missing values found in key columns: {', '.join(null_cols)}")
else:
    print("   - ✅ No missing values in key columns ('country_name', 'year').")

# Rule 3: Validate each row against the Pydantic model
invalid_row_count = 0
for index, row in df.iterrows():
    try:
        # Pydantic checks data types (e.g., year is int) and value ranges (e.g., year >= 2010)
        # It correctly handles NaN values from pandas for our Optional fields.
        EconomicData(**row.to_dict())
    except ValidationError as e:
        invalid_row_count += 1
        # We'll only report the first error to avoid flooding the console
        if invalid_row_count == 1:
            errors.append(f"Row {index+2} is invalid: {e}")

if invalid_row_count == 0:
    print("   - ✅ All rows have valid data types and values.")
else:
    # The full error for the first invalid row is already in the errors list.
    errors.append(f"   ... and {invalid_row_count - 1} other rows are also invalid.")

# --- 4. Report Final Result ---
print("\n✅ Validation complete.")

if not errors:
    print("\n🎉 Validation SUCCEEDED!")
else:
    print("\n🚨 Validation FAILED! The following issues were found:")
    for error in errors:
        print(f"   - {error}")
    sys.exit(1)
