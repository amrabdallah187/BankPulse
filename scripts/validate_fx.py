import pandas as pd
from pydantic import BaseModel, Field, ValidationError
import sys

# This script uses Pydantic for robust, simple data validation without
# any external configuration files.

# --- 1. Define the Expected Data Structure for a Single Row ---
# We define what a valid row of our fx_rates data should look like.
class FxRate(BaseModel):
    # The Field function allows us to add validation rules.
    EUR: float = Field(gt=0.8, lt=1.2)  # Must be a float greater than 0.8 and less than 1.2
    GBP: float = Field(gt=0.7, lt=1.1)  # Must be a float greater than 0.7 and less than 1.1

# --- 2. Load the Data with Pandas ---
DATA_PATH = "data/fx_rates.csv"
print(f"✅ Loading data from {DATA_PATH}...")
try:
    df = pd.read_csv(DATA_PATH)
except FileNotFoundError:
    print(f"❌ CRITICAL: '{DATA_PATH}' not found. Please run 'fetch_fx_data.py' first.")
    sys.exit(1)

# --- 3. Perform Validations ---
errors = []
print("\n🔎 Performing validations...")

# Rule 1: Check table row count
if not (250 <= len(df) <= 270):
    errors.append(f"Row count is {len(df)}, which is outside the expected range of 250-270.")
else:
    print("   - ✅ Row count is within the expected range.")

# Rule 2: Check for missing values
if df.isnull().values.any():
    null_cols = df.columns[df.isnull().any()].tolist()
    errors.append(f"Missing values found in columns: {', '.join(null_cols)}")
else:
    print("   - ✅ No missing values found.")

# Rule 3: Validate each row against the Pydantic model
for index, row in df.iterrows():
    try:
        # Pydantic will automatically check the data types and value ranges
        FxRate(**row.to_dict())
    except ValidationError as e:
        # If a row is invalid, we record the error and stop checking
        errors.append(f"Row {index+2} is invalid: {e}")
        break # Stop on the first invalid row for a cleaner error message
else:
    # This 'else' block only runs if the 'for' loop completes without a 'break'
    print("   - ✅ All rows have valid data types and are within value ranges.")

# --- 4. Report Final Result ---
print("\n✅ Validation complete.")

if not errors:
    print("\n🎉 Validation SUCCEEDED!")
else:
    print("\n🚨 Validation FAILED! The following issues were found:")
    for error in errors:
        print(f"   - {error}")
    sys.exit(1)
