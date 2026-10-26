# Python Data Quality Audit Workflow

## Audit sequence

1. Load the dataset and record its row and column counts.
2. Inspect column names, data types, and missing-value counts.
3. Check duplicate rows and duplicate business keys separately.
4. Validate numeric ranges and category values against expected rules.
5. Check date parsing and impossible date values.
6. Summarize findings before deciding whether to drop, impute, or flag records.
7. Save an auditable summary of issues and transformations.

## Reporting rules

- Never silently remove rows without recording the reason and count.
- Preserve a raw copy before transformations.
- Distinguish missing values from valid zero values.
- Use business rules to define outliers rather than deleting every statistical outlier.
- If data is synthetic, label it as sample data.
- Test the script on a small known example and document the expected result.

## Suggested quality metrics

| Check | Example metric |
|---|---|
| Completeness | Non-null cells / expected cells |
| Uniqueness | Duplicate business keys |
| Validity | Values that pass defined rules / non-null values |
| Consistency | Records that satisfy cross-column rules |
| Timeliness | Latest valid date compared with the expected refresh date |

The audit describes data quality issues; it does not automatically prove that the data is fit for every use case.