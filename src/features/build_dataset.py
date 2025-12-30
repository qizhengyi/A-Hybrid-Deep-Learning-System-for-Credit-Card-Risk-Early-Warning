import duckdb
from pathlib import Path
from src.config import RAW_CSV, DATA_PROCESSED, DUCKDB_PATH, TRAIN_PARQUET, PROJECT_ROOT
from src.db.run_sql import run_sql_file

SQL_DIR = PROJECT_ROOT / "sql"

def main() -> None:
    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)

    if not RAW_CSV.exists():
        raise FileNotFoundError(
            f"Raw CSV not found: {RAW_CSV}\n"
            f"Place UCI dataset CSV at data/raw/uci_credit_default.csv"
        )

    con = duckdb.connect(str(DUCKDB_PATH))

    # schema
    run_sql_file(con, SQL_DIR / "00_schema.sql")

    # load raw csv into table (auto detect header + types)
    con.execute("DELETE FROM credit_card_raw;")
    con.execute(
        """
        INSERT INTO credit_card_raw
        SELECT
          LIMIT_BAL,
          SEX,
          EDUCATION,
          MARRIAGE,
          AGE,
          PAY_0,
          PAY_2,
          PAY_3,
          PAY_4,
          PAY_5,
          PAY_6,
          BILL_AMT1,
          BILL_AMT2,
          BILL_AMT3,
          BILL_AMT4,
          BILL_AMT5,
          BILL_AMT6,
          PAY_AMT1,
          PAY_AMT2,
          PAY_AMT3,
          PAY_AMT4,
          PAY_AMT5,
          PAY_AMT6,
          "default payment next month"::INTEGER AS LABEL
        FROM read_csv_auto(?, header=true);
        """,
        [str(RAW_CSV)],
    )

    # feature view + training set
    run_sql_file(con, SQL_DIR / "02_feature_view.sql")
    run_sql_file(con, SQL_DIR / "03_training_set.sql")

    # export parquet
    con.execute("COPY training_set TO ? (FORMAT PARQUET);", [str(TRAIN_PARQUET)])

    n = con.execute("SELECT COUNT(*) FROM training_set;").fetchone()[0]
    print(f"OK: training_set rows = {n}")
    print(f"Saved: {TRAIN_PARQUET}")
    print(f"DuckDB: {DUCKDB_PATH}")

if __name__ == "__main__":
    main()
