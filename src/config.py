from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_RAW = PROJECT_ROOT / "data" / "raw"
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"

RAW_CSV = DATA_RAW / "uci_credit_default.csv"
DUCKDB_PATH = DATA_PROCESSED / "risk.duckdb"
TRAIN_PARQUET = DATA_PROCESSED / "training_set.parquet"
