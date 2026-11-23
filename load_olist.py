"""Load the Olist CSVs from data/raw/ into Postgres (schema: raw)."""
import os
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, text

DATA_DIR = Path("data/raw")
DB_URL = os.getenv("DATABASE_URL", "postgresql+psycopg://olist:olist@localhost:5432/olist")


def table_name(csv_path: Path) -> str:
    # olist_orders_dataset.csv -> orders
    return csv_path.stem.removeprefix("olist_").removesuffix("_dataset")


def date_columns(df: pd.DataFrame) -> list[str]:
    return [c for c in df.columns if "date" in c or "timestamp" in c or c.endswith("_at")]


def main() -> None:
    engine = create_engine(DB_URL)
    with engine.begin() as conn:
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS raw"))
    for csv_path in sorted(DATA_DIR.glob("*.csv")):
        df = pd.read_csv(csv_path)
        for col in date_columns(df):
            df[col] = pd.to_datetime(df[col])
        name = table_name(csv_path)
        df.to_sql(name, engine, schema="raw", if_exists="replace", index=False, chunksize=10_000)
        print(f"raw.{name}: {len(df):,} rows")


if __name__ == "__main__":
    main()

# The script does three things:

# It creates a raw schema in Postgres to hold the untouched source tables.
# It reads each CSV and turns its date columns into real timestamps, which you'll need for delivery-time math.
# It writes each CSV to a table named after the file, so olist_orders_dataset.csv becomes raw.orders.