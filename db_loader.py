# app/db_loader.py

import os
import pandas as pd
from sqlalchemy import create_engine

# Create output directory if it doesn't exist
os.makedirs("database", exist_ok=True)

# Connect to SQLite database (will create ecommerce.db if it doesn't exist)
engine = create_engine("sqlite:///database/ecommerce.db")


# Helper Function to Clean Data
def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    # Strip whitespace from column names
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    # Remove columns with all NaNs
    df.dropna(axis=1, how='all', inplace=True)

    # Remove rows with all NaNs
    df.dropna(axis=0, how='all', inplace=True)

    # Fill remaining NaNs with placeholder (optional)
    df.fillna(value="", inplace=True)

    return df


# Load, clean, and optionally convert dates for specific tables
def load_and_store_csv(filename: str, table_name: str, date_columns: list = None, date_format: str = None):
    filepath = os.path.join("data", filename)
    print(f"Processing {filepath} → table `{table_name}`...")

    df = pd.read_csv(filepath, encoding="ISO-8859-1")

    df = clean_dataframe(df)

    # Convert date columns if specified
    if date_columns and date_format:
        for col in date_columns:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], format=date_format, errors='coerce').dt.date

    # Save to SQL
    df.to_sql(table_name, engine, index=False, if_exists="replace")
    print(f"✅ Loaded `{table_name}` ({len(df)} rows)")


# ------------------------- #
# Run for All 3 Datasets
# ------------------------- #
if __name__ == "__main__":
    load_and_store_csv(
        "Product-Level Eligibility Table.csv",
        "eligibility",
        date_columns=["eligibility_datetime_utc"],
        date_format="%m/%d/%y"  # if needed
    )

    load_and_store_csv(
        "Product-Level Ad Sales and Metrics.csv",
        "ad_sales_metrics",
        date_columns=["date"],
        date_format="%m/%d/%y"
    )

    load_and_store_csv(
        "Product-Level Total Sales and Metrics.csv",
        "total_sales_metrics",
        date_columns=["date"],
        date_format="%m/%d/%y"
    )

    print("\n✅ All datasets have been loaded into ecommerce.db")
