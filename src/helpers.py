import sqlite3
import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"

FILENAME_MAP = {
    "customers": "olist_customers_dataset.csv",
    "orders": "olist_orders_dataset.csv",
    "order_items": "olist_order_items_dataset.csv",
    "payments": "olist_order_payments_dataset.csv",
    "reviews": "olist_order_reviews_dataset.csv",
    "products": "olist_products_dataset.csv",
    "sellers": "olist_sellers_dataset.csv",
    "product_translation": "product_category_name_translation.csv",
}

def get_connection(tables: list[str]) -> sqlite3.Connection:
    """
    Create an in-memory SQLite DB and load the specified Olist tables into it.
    `tables` should be short names matching keys in FILENAME_MAP.
    """
    conn = sqlite3.connect(":memory:")
    for table in tables:
        csv_path = DATA_DIR / FILENAME_MAP[table]
        df = pd.read_csv(csv_path)
        df.to_sql(table, conn, index=False, if_exists="replace")
    return conn

def sql(query: str, conn: sqlite3.Connection) -> pd.DataFrame:
    """Run a SQL query against the given connection, return a DataFrame."""
    return pd.read_sql_query(query, conn)