import requests
import pandas as pd
from pathlib import Path
import sys

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

URL = "https://api.frankfurter.app/2023-01-01..2023-12-31"
params = {"from": "USD", "to": "EUR,GBP"}

print("📡 Fetching exchange rate data from Frankfurter...")
r = requests.get(URL, params=params)

if r.status_code != 200:
    print(f"❌ API returned status {r.status_code}")
    print("Response preview:", r.text[:200])
    sys.exit(1)

try:
    json_data = r.json()
except Exception:
    print("❌ Could not parse JSON — response may be HTML or empty.")
    print("Response preview:", r.text[:300])
    sys.exit(1)

data = json_data.get("rates", {})
if not data:
    print("⚠️ No 'rates' data found in API response.")
    sys.exit(1)

df = pd.DataFrame.from_dict(data, orient="index")
df.index = pd.to_datetime(df.index)
df = df.reset_index().rename(columns={"index": "date"})

output_path = DATA_DIR / "fx_rates.csv"
df.to_csv(output_path, index=False)
print(f"✅ Data saved to {output_path.resolve()}")
print(df.head())
