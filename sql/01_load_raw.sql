-- Replace path by parameter in Python; this file is referenced by build_dataset.py
-- Example:
-- COPY credit_card_raw FROM 'data/raw/uci_credit_default.csv' (HEADER, AUTO_DETECT TRUE);

-- For DuckDB we usually do:
-- INSERT INTO credit_card_raw SELECT ... FROM read_csv_auto('path', header=true);
