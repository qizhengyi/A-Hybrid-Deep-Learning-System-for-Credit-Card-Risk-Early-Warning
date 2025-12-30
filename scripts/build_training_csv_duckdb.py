"""
Build a training-ready CSV using SQL-based feature engineering.

This script:
1. Loads the raw UCI CSV into DuckDB
2. Creates engineered risk features using SQL
3. Exports a clean training_set.csv for ML models

This mimics a production-style feature store workflow.
"""

import duckdb
from pathlib import Path

# Project root
ROOT = Path(__file__).resolve().parents[1]

# Input raw CSV
RAW_CSV = ROOT / "data" / "raw" / "uci_credit_default.csv"

# Output directory
PROCESSED_DIR = ROOT / "data" / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

# DuckDB database path
DB_PATH = PROCESSED_DIR / "risk.duckdb"

# Output training CSV
OUT_TRAIN_CSV = PROCESSED_DIR / "training_set.csv"


def main():
    if not RAW_CSV.exists():
        raise FileNotFoundError(
            f"Raw CSV not found: {RAW_CSV}. "
            "Run download_uci_to_csv.py first."
        )

    # Connect to DuckDB (file-backed)
    con = duckdb.connect(str(DB_PATH))

    # Load raw CSV into DuckDB table
    con.execute("DROP TABLE IF EXISTS credit_card_raw;")
    con.execute(
        """
        CREATE TABLE credit_card_raw AS
        SELECT *
        FROM read_csv_auto(?, header=true);
        """,
        [str(RAW_CSV)]
    )

    # Normalize label column name if necessary
    columns = [
        r[1] for r in con.execute(
            "PRAGMA table_info('credit_card_raw')"
        ).fetchall()
    ]

    if "default payment next month" not in columns:
        default_col = None
        for c in columns:
            if "default" in c.lower():
                default_col = c
                break
        if default_col is None:
            raise RuntimeError("No default label column found in raw data.")

        con.execute(
            f'ALTER TABLE credit_card_raw '
            f'RENAME COLUMN "{default_col}" TO "default payment next month";'
        )

    # Create training feature table
    con.execute("DROP TABLE IF EXISTS training_set;")
    con.execute(
        """
        CREATE TABLE training_set AS
        SELECT
          -- Surrogate customer identifier
          row_number() OVER () AS customer_id,

          -- Static features
          LIMIT_BAL,
          SEX,
          EDUCATION,
          MARRIAGE,
          AGE,

          -- Delinquency indicators
          (PAY_0 > 0)::INT AS delinquent_m1,
          (PAY_2 > 0)::INT AS delinquent_m2,
          (PAY_3 > 0)::INT AS delinquent_m3,
          (PAY_4 > 0)::INT AS delinquent_m4,
          (PAY_5 > 0)::INT AS delinquent_m5,
          (PAY_6 > 0)::INT AS delinquent_m6,

          -- Number of delinquent months in last 6 months
          ((PAY_0 > 0)::INT + (PAY_2 > 0)::INT + (PAY_3 > 0)::INT +
           (PAY_4 > 0)::INT + (PAY_5 > 0)::INT + (PAY_6 > 0)::INT)
           AS delinquent_cnt_6m,

          -- Credit utilization ratios
          BILL_AMT1 * 1.0 / NULLIF(LIMIT_BAL, 0) AS util_m1,
          BILL_AMT2 * 1.0 / NULLIF(LIMIT_BAL, 0) AS util_m2,
          BILL_AMT3 * 1.0 / NULLIF(LIMIT_BAL, 0) AS util_m3,

          -- Payment ratios
          PAY_AMT1 * 1.0 / NULLIF(BILL_AMT1, 0) AS pay_ratio_m1,
          PAY_AMT2 * 1.0 / NULLIF(BILL_AMT2, 0) AS pay_ratio_m2,
          PAY_AMT3 * 1.0 / NULLIF(BILL_AMT3, 0) AS pay_ratio_m3,

          -- Label
          "default payment next month"::INT AS label
        FROM credit_card_raw;
        """
    )

    # Export training table to CSV
    con.execute(
        "COPY training_set TO ? (HEADER, DELIMITER ',');",
        [str(OUT_TRAIN_CSV)]
    )

    row_count = con.execute(
        "SELECT COUNT(*) FROM training_set;"
    ).fetchone()[0]

    print(f"[SUCCESS] Training CSV saved to: {OUT_TRAIN_CSV}")
    print(f"Number of rows: {row_count}")


if __name__ == "__main__":
    main()
