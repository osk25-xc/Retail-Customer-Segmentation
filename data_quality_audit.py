"""Run practical data-quality checks on the retail customer dataset.

Usage:
    python data_quality_audit.py
    python data_quality_audit.py --input data/retail_customers.csv

The script reports issues; it does not silently modify the source dataset.
"""
from __future__ import annotations

import argparse
from pathlib import Path
import pandas as pd

REQUIRED_COLUMNS = {
    "customer_id",
    "country",
    "gender",
    "age",
    "purchase_frequency",
    "average_order_value",
    "total_purchases",
    "recency_days",
    "total_items",
    "favorite_category",
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit retail customer data quality.")
    parser.add_argument(
        "--input",
        default="data/retail_customers.csv",
        help="Path to the retail customer CSV",
    )
    args = parser.parse_args()

    path = Path(args.input)
    if not path.exists():
        raise FileNotFoundError(
            f"Could not find {path}. Generate the dataset first with create_dataset.py."
        )

    df = pd.read_csv(path)
    print("\n=== Retail Customer Data Quality Audit ===")
    print(f"File: {path}")
    print(f"Rows: {len(df):,}")
    print(f"Columns: {len(df.columns):,}")

    missing_columns = sorted(REQUIRED_COLUMNS - set(df.columns))
    if missing_columns:
        print(f"\nFAIL — missing required columns: {missing_columns}")
        return

    print("\n--- Missing values by column ---")
    missing = df[list(REQUIRED_COLUMNS)].isna().sum().sort_values(ascending=False)
    print(missing.to_string())

    print("\n--- Duplicate customer IDs ---")
    duplicate_ids = int(df["customer_id"].duplicated(keep=False).sum())
    print(duplicate_ids)

    checks = {
        "age outside 18–100": ~df["age"].between(18, 100),
        "purchase_frequency <= 0": df["purchase_frequency"] <= 0,
        "average_order_value < 0": df["average_order_value"] < 0,
        "total_purchases < 0": df["total_purchases"] < 0,
        "recency_days < 0": df["recency_days"] < 0,
        "total_items <= 0": df["total_items"] <= 0,
        "blank country": df["country"].astype("string").str.strip().eq(""),
        "blank favorite_category": df["favorite_category"].astype("string").str.strip().eq(""),
    }

    print("\n--- Rule checks ---")
    issue_total = 0
    for label, mask in checks.items():
        count = int(mask.fillna(False).sum())
        issue_total += count
        print(f"{label}: {count}")

    expected_spend = df["purchase_frequency"] * df["average_order_value"]
    inconsistent_spend = (
        (df["total_purchases"] - expected_spend).abs() > 0.02
    ) & df[["total_purchases", "purchase_frequency", "average_order_value"]].notna().all(axis=1)
    inconsistent_count = int(inconsistent_spend.sum())
    print(f"total_purchases inconsistent with frequency × average_order_value: {inconsistent_count}")

    missing_total = int(df[list(REQUIRED_COLUMNS)].isna().sum().sum())
    status = "REVIEW REQUIRED" if (
        missing_total or duplicate_ids or issue_total or inconsistent_count
    ) else "PASS — no issues found by these checks"
    print(f"\nOverall status: {status}")
    print("Note: validate business rules with the data owner before treating any flagged row as an error.")


if __name__ == "__main__":
    main()
