"""
Download the UCI Credit Card Default dataset and convert it to CSV format.

This script:
1. Downloads the original XLS file from the UCI Machine Learning Repository
2. Cleans column names if needed
3. Saves the dataset as a reproducible CSV file

The raw CSV is NOT committed to Git and is used as the input
for SQL-based feature engineering.
"""

import pandas as pd
from pathlib import Path

# UCI dataset URL (official source)
UCI_XLS_URL = (
    "https://archive.ics.uci.edu/ml/machine-learning-databases/00350/"
    "default%20of%20credit%20card%20clients.xls"
)

# Project root directory
ROOT = Path(__file__).resolve().parents[1]

# Output directory for raw data
RAW_DIR = ROOT / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)

# Output CSV path
OUT_CSV = RAW_DIR / "uci_credit_default.csv"


def main():
    print("Downloading UCI Credit Card Default dataset...")

    # The first row in the XLS file contains metadata,
    # so we use header=1 to read the actual column names.
    df = pd.read_excel(UCI_XLS_URL, header=1)

    # Drop the ID column if present (not a predictive feature)
    if "ID" in df.columns:
        df = df.drop(columns=["ID"])

    # Ensure the label column name matches the training pipeline
    # Expected label name: "default payment next month"
    if "default payment next month" not in df.columns:
        for col in df.columns:
            if "default" in col.lower():
                df = df.rename(columns={col: "default payment next month"})
                break

    # Save raw CSV
    df.to_csv(OUT_CSV, index=False)

    print(f"[SUCCESS] Raw CSV saved to: {OUT_CSV}")
    print(f"Dataset shape: {df.shape}")
    print("Columns:")
    for c in df.columns:
        print(f"  - {c}")


if __name__ == "__main__":
    main()
