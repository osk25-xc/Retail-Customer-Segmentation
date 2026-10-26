"""Regression tests for the data quality audit CLI.

Run from the repository root with:
    python -m unittest discover -s tests -v
"""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import pandas as pd

SCRIPT = Path(__file__).resolve().parents[1] / "data_quality_audit.py"
VALID_ROW = {
    "customer_id": "C001",
    "country": "India",
    "gender": "Female",
    "age": 30,
    "purchase_frequency": 2,
    "average_order_value": 100.0,
    "total_purchases": 200.0,
    "recency_days": 10,
    "total_items": 3,
    "favorite_category": "Beauty",
}


class DataQualityAuditCliTests(unittest.TestCase):
    def run_audit(self, frame):
        with tempfile.TemporaryDirectory() as tmp:
            csv_path = Path(tmp) / "customers.csv"
            frame.to_csv(csv_path, index=False)
            return subprocess.run(
                [sys.executable, str(SCRIPT), "--input", str(csv_path)],
                capture_output=True,
                text=True,
                check=False,
            )

    def test_clean_row_reports_pass(self):
        result = self.run_audit(pd.DataFrame([VALID_ROW]))
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assertIn("PASS — no issues found by these checks", result.stdout)

    def test_invalid_age_is_reported(self):
        row = dict(VALID_ROW, age=12)
        result = self.run_audit(pd.DataFrame([row]))
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assertIn("age outside 18–100: 1", result.stdout)
        self.assertIn("Overall status: REVIEW REQUIRED", result.stdout)

    def test_missing_required_column_returns_failure_code(self):
        row = {key: value for key, value in VALID_ROW.items() if key != "country"}
        result = self.run_audit(pd.DataFrame([row]))
        self.assertEqual(result.returncode, 1, msg=result.stderr)
        self.assertIn("FAIL — missing required columns", result.stdout)
        self.assertIn("country", result.stdout)

    def test_duplicate_customer_ids_are_reported(self):
        second_row = dict(VALID_ROW, country="India")
        result = self.run_audit(pd.DataFrame([VALID_ROW, second_row]))
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assertIn("Duplicate customer IDs", result.stdout)
        self.assertIn("\\n2\\n", result.stdout)
        self.assertIn("Overall status: REVIEW REQUIRED", result.stdout)

    def test_inconsistent_spend_is_reported(self):
        row = dict(VALID_ROW, total_purchases=250.0)
        result = self.run_audit(pd.DataFrame([row]))
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assertIn(
            "total_purchases inconsistent with frequency × average_order_value: 1",
            result.stdout,
        )
        self.assertIn("Overall status: REVIEW REQUIRED", result.stdout)


if __name__ == "__main__":
    unittest.main()
