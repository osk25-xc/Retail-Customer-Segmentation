# RFM Metric Definitions

This project uses the RFM framework to summarize customer purchasing behavior.

## Metric definitions

| Metric | Definition | Interpretation |
|---|---|---|
| Recency | Days since the customer's most recent purchase | Lower values indicate a more recent purchase |
| Frequency | Number of purchases in the selected observation period | Higher values indicate more frequent purchasing |
| Monetary | Total customer spend in the selected observation period | Higher values indicate greater recorded spend |

## Important implementation notes

- Define a single analysis date (snapshot date) before calculating recency.
- Define the transaction window used for frequency and monetary value.
- Calculate RFM from transaction-level data where possible; if using pre-aggregated customer data, document how each field was produced.
- Check duplicate customer IDs and missing values before scoring.
- Make sure higher scores consistently represent the intended behavior. Recency scoring is commonly reversed because fewer days since purchase is better.
- Avoid assigning business labels such as "VIP" or "At Risk" without documenting score thresholds.

## Business use

RFM segments can help prioritize retention experiments, customer engagement, and service outreach. Segment membership is descriptive; it does not prove why a customer behaves a certain way.

## Validation checklist

1. Confirm the snapshot date and observation window.
2. Confirm one row per customer after aggregation.
3. Check that frequency and monetary values are non-negative.
4. Verify that recency is measured in days and is not negative.
5. Reconcile total monetary value with the source transactions.
6. Record scoring boundaries so results can be reproduced.
