"""Run practical data-quality checks on the retail customer dataset.

Usage:
    python data_quality_audit.py
    python data_quality_audit.py --input data/retail_customers.csv

The script reports issues; it does not silently modify the source dataset.
"""
from __future__ import annotations

import argparse
from pathlib import Path
import sys

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
NUMERIC_COLUMNS = (
    "age",
    "purchase_frequency",
    "average_order_value",
    "total_purchases",
    "recency_days",
    "total_items",
)


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
        print(f"FAIL — input file not found: {path}", file=sys.stderr)
        sys.exit(2)

    try:
        df = pd.read_csv(path)
    except (OSError, pd.errors.ParserError, UnicodeDecodeError) as exc:
        print(f"FAIL — could not read input CSV: {exc}", file=sys.stderr)
        sys.exit(2)

    print("\n=== Retail Customer Data Quality Audit ===")
    print(f"File: {path}")
    print(f"Rows: {len(df):,}")
    print(f"Columns: {len(df.columns):,}")

    missing_columns = sorted(REQUIRED_COLUMNS - set(df.columns))
    if missing_columns:
        print(f"\nFAIL — missing required columns: {missing_columns}")
        sys.exit(1)

    # Convert numeric fields for validation, while counting non-empty values
    # that could not be parsed as numbers. The source file is never rewritten.
    non_numeric_counts = {}
    for column in NUMERIC_COLUMNS:
        original = df[column]
        converted = pd.to_numeric(original, errors="coerce")
        non_numeric_counts[column] = int((original.notna() & converted.isna()).sum())
        df[column] = converted

    print("\n--- Missing values by column ---")
    missing = df[list(REQUIRED_COLUMNS)].isna().sum().sort_values(ascending=False)
    print(missing.to_string())

    print("\n--- Non-numeric values in numeric columns ---")
    for column, count in non_numeric_counts.items():
        print(f"{column}: {count}")

    print("\n--- Duplicate customer IDs ---")
    customer_ids = df["customer_id"].astype("string").str.strip()
    duplicate_ids = int(customer_ids.duplicated(keep=False).sum())
    print(duplicate_ids)

    checks = {
        "blank customer_id": customer_ids.isna() | customer_ids.eq(""),
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
    spend_columns = ["total_purchases", "purchase_frequency", "average_order_value"]
    valid_spend = df[spend_columns].notna().all(axis=1)
    inconsistent_spend = (
        (df["total_purchases"] - expected_spend).abs() > 0.02
    ) & valid_spend
    inconsistent_count = int(inconsistent_spend.sum())
    print(
        "total_purchases inconsistent with frequency × average_order_value: "
        f"{inconsistent_count}"
    )

    missing_total = int(df[list(REQUIRED_COLUMNS)].isna().sum().sum())
    non_numeric_total = sum(non_numeric_counts.values())
    has_issues = (
        missing_total
        or non_numeric_total
        or duplicate_ids
        or issue_total
        or inconsistent_count
    )
    status = "REVIEW REQUIRED" if has_issues else "PASS — no issues found by these checks"
    print(f"\nOverall status: {status}")
    print(
        "Note: validate business rules with the data owner before treating any "
        "flagged row as an error."
    )


if __name__ == "__main__":
    main()
