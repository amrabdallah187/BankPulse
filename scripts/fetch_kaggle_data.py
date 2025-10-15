import kagglehub
import sys
from pathlib import Path
import shutil

# --- Configuration ---
DATASET_NAME = "laotse/credit-risk-dataset"
TARGET_CSV = "credit_risk_dataset.csv"
RAW_DATA_DIR = Path("data") / "raw"
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True) # Ensure the target directory exists

# --- Main Script ---
def fetch_kaggle_dataset():
    """
    Downloads the dataset from Kaggle and moves the CSV to the data/raw directory.
    """
    print(f"📡 Downloading and locating dataset '{DATASET_NAME}' from Kaggle...")
    
    try:
        # kagglehub now downloads AND unzips, returning the path to the folder.
        dataset_dir = Path(kagglehub.dataset_download(DATASET_NAME))
        print(f"✅ Dataset files located at: {dataset_dir}")
    except Exception as e:
        print(f"❌ Failed to download dataset. Have you authenticated with Kaggle?")
        print(f"   Original error: {e}")
        sys.exit(1)
        
    # --- Move the CSV file ---
    source_csv_path = dataset_dir / TARGET_CSV
    target_csv_path = RAW_DATA_DIR / TARGET_CSV
    
    if source_csv_path.exists():
        print(f"🚚 Moving '{TARGET_CSV}' to '{target_csv_path.resolve()}'...")
        shutil.move(source_csv_path, target_csv_path)
    else:
        print(f"❌ Could not find '{TARGET_CSV}' in the downloaded directory: {dataset_dir}")
        sys.exit(1)
        
    print("✨ All done!")
    
    return target_csv_path

if __name__ == "__main__":
    final_path = fetch_kaggle_dataset()
    print(f"\n✅ Credit risk dataset is now at: {final_path.resolve()}")
