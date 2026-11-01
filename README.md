# Retail Customer Segmentation | RFM Analysis

A Python project for exploring customer purchasing behavior with Recency, Frequency, and Monetary (RFM) measures, supported by data-quality checks.

## Business objective

Summarize customer purchase behavior and identify groups that may be useful for retention and engagement analysis.

## RFM framework

- **Recency:** Days since the customer's latest purchase. Lower is more recent.
- **Frequency:** Number of purchases in the defined observation window.
- **Monetary:** Total customer spend in the same observation window.

Document the snapshot date, observation window, and scoring boundaries before interpreting segments.

## Data-quality audit

The command-line audit checks required columns, missing values, duplicate or blank customer IDs, invalid ranges, blank category/country values, non-numeric values, and consistency between purchase-frequency and monetary fields.

Run from the repository root:

```bash
python data_quality_audit.py --input data/retail_customers.csv
```

The audit does not modify the input file. Review flagged records against the dataset's business rules before treating them as errors.

## Tests

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
```

GitHub Actions is configured to run the unittest suite; check the Actions tab for the latest workflow result.

## Analysis workflow

1. Inspect and validate the source data.
2. Aggregate transaction data to one row per customer, if required.
3. Calculate RFM metrics using a documented observation window.
4. Apply the implemented scoring or segmentation method.
5. Compare segment sizes and monetary contribution.
6. Summarize findings with limitations and possible business experiments.

## Tools

Python · Pandas · NumPy · Matplotlib · Seaborn · Scikit-learn · Jupyter Notebook · unittest · GitHub Actions

## Interpretation

RFM segments describe observed purchasing patterns; they do not explain customer motivation or prove that a particular campaign will work. Validate segment definitions before acting on them.

Maintained by [Omkar S. Kshirsagar](https://github.com/osk25-xc).
