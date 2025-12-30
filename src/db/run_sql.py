from pathlib import Path
import duckdb

def run_sql_file(con: duckdb.DuckDBPyConnection, sql_path: Path) -> None:
    sql = sql_path.read_text(encoding="utf-8")
    con.execute(sql)
