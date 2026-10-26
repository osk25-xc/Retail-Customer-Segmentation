# Retail Customer Segmentation | RFM Analysis

A Python analytics project that uses Recency, Frequency, and Monetary (RFM) measures to explore customer purchasing behavior and support customer-retention analysis.

## Business objective

Understand how recently and frequently customers purchase, compare customer value, and identify groups that may benefit from different retention strategies.

## RFM framework

- **Recency:** How recently a customer purchased.
- **Frequency:** How often a customer purchased.
- **Monetary:** How much a customer spent.

## Data quality audit

The command-line audit checks required columns, missing values, duplicate and blank customer IDs, invalid ranges, blank category/country values, non-numeric values in numeric fields, and consistency between purchase frequency, average order value, and total purchases.

Run it from the repository root:

```bash
python data_quality_audit.py --input data/retail_customers.csv
```

If you omit `--input`, the script looks for `data/retail_customers.csv`. The audit does not modify the input file. A clean dataset returns exit code `0`; data-quality findings are summarized for review; missing required columns return `1`; an unreadable or missing input file returns `2`.

Business rules such as age limits and spend consistency should be confirmed with the data owner before flagged rows are treated as errors.

## Run the automated tests

Install dependencies and run the regression suite:

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
```

GitHub Actions also runs the unittest suite for repository changes. Check the Actions tab for the latest run status.

## Analysis workflow

1. Inspect the dataset structure and validate data quality.
2. Calculate RFM measures from the available customer or transaction data.
3. Apply the project's RFM scoring or clustering approach.
4. Compare segment sizes and monetary contribution.
5. Visualize the results and formulate testable business recommendations.

## Business questions

- Which customers purchase recently and frequently?
- Which segments contribute more monetary value?
- Which customer groups may need re-engagement?
- How could segment-level messaging differ?

## Tools

Python · Pandas · NumPy · Matplotlib · Seaborn · Scikit-learn · Jupyter Notebook · unittest · GitHub Actions

## Skills demonstrated

Data cleaning · Data quality validation · Feature engineering · RFM analysis · Customer segmentation · Visualization · Automated testing · Business recommendations

---

Created by **Omkar S. Kshirsagar** | [GitHub Profile](https://github.com/osk25-xc)
