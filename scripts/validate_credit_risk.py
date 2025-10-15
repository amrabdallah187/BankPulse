import pandas as pd
from pydantic import BaseModel, Field, ValidationError
import sys
from typing import Optional
from enum import Enum

# --- 1. Define Allowed Categories using Enums ---
class HomeOwnership(str, Enum):
    RENT = "RENT"
    OWN = "OWN"
    MORTGAGE = "MORTGAGE"
    OTHER = "OTHER"

class LoanIntent(str, Enum):
    PERSONAL = "PERSONAL"
    EDUCATION = "EDUCATION"
    MEDICAL = "MEDICAL"
    VENTURE = "VENTURE"
    HOMEIMPROVEMENT = "HOMEIMPROVEMENT"
    DEBTCONSOLIDATION = "DEBTCONSOLIDATION"

class LoanGrade(str, Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    E = "E"
    F = "F"
    G = "G"

class DefaultOnFile(str, Enum):
    Y = "Y"
    N = "N"

# --- 2. Define the Expected Data Structure for a Single Row ---
class CreditRiskData(BaseModel):
    person_age: int = Field(ge=18, le=100)
    person_income: int = Field(ge=0)
    person_home_ownership: HomeOwnership
    person_emp_length: Optional[float] = Field(default=None, ge=0)
    loan_intent: LoanIntent
    loan_grade: LoanGrade
    loan_amnt: int = Field(ge=0)
    loan_int_rate: Optional[float] = Field(default=None, ge=0)
    loan_status: int = Field(ge=0, le=1)
    loan_percent_income: float = Field(ge=0, le=1)
    cb_person_default_on_file: DefaultOnFile
    cb_person_cred_hist_length: int = Field(ge=0)

# --- 3. Load the Data with Pandas ---
DATA_PATH = "data/raw/credit_risk_dataset.csv"
print(f"✅ Loading data from {DATA_PATH}...")
try:
    df = pd.read_csv(DATA_PATH)
except FileNotFoundError:
    print(f"❌ CRITICAL: '{DATA_PATH}' not found. Please download it from Kaggle and place it in 'data/raw/'.")
    sys.exit(1)

# --- 4. Data Correction ---
# Instead of removing bad rows, we'll fix them based on your suggestion.
print("\n🧹 Correcting data...")
# Find rows where age is unrealistic (e.g., > 100)
unrealistic_age_mask = df['person_age'] > 100
num_corrected = unrealistic_age_mask.sum()

if num_corrected > 0:
    # Apply the correction: assume it's a typo and subtract 100 (e.g., 144 -> 44)
    df.loc[unrealistic_age_mask, 'person_age'] -= 100
    print(f"   - Corrected {num_corrected} rows with unrealistic ages by subtracting 100.")
else:
    print("   - No unrealistic ages found to correct.")

# Convert all pandas NaN values to Python's None for Pydantic.
df = df.where(pd.notna(df), None)

# --- 5. Perform Validations on Corrected Data ---
errors = []
print("\n🔎 Performing validations on corrected data...")

# Rule 1: Check row count
if len(df) < 10000:
    errors.append(f"Row count is only {len(df)}, which is unexpectedly low for this dataset.")
else:
    print(f"   - ✅ Row count is {len(df)}, which looks reasonable.")

# Rule 2: Validate each row
invalid_row_count = 0
for index, row in df.iterrows():
    try:
        row_dict = row.to_dict()
        cleaned_row = {k: None if pd.isna(v) else v for k, v in row_dict.items()}
        CreditRiskData(**cleaned_row)
    except ValidationError as e:
        invalid_row_count += 1
        if invalid_row_count == 1:
            errors.append(f"Row {index+2} is invalid: {e}")

if invalid_row_count == 0:
    print("   - ✅ All rows conform to the expected schema and validation rules.")
else:
    errors.append(f"   ... and {invalid_row_count - 1} other rows are also invalid.")

# --- 6. Report Final Result ---
print("\n✅ Validation complete.")

if not errors:
    print("\n🎉 Validation SUCCEEDED!")
else:
    print("\n🚨 Validation FAILED! The following issues were found:")
    for error in errors:
        print(f"   - {error}")
    sys.exit(1)
