# RFM Segmentation Methodology

## Snapshot design
Choose and record a snapshot date and observation window. Use only transactions that occurred on or before the snapshot date.

## Customer metrics
- Recency: snapshot date minus most recent eligible purchase date.
- Frequency: distinct eligible purchases in the observation window.
- Monetary: total eligible spend in the same window, using a consistent returns/refunds policy.

## Scoring
Document quantile boundaries, tie handling, and score direction. Lower recency is better; higher frequency and monetary values generally indicate more observed activity. Recompute boundaries when the observation window changes.

## Validation
Check customer ID coverage, duplicate transactions, negative/zero monetary values, date parsing, and customers with no eligible purchases. Reconcile customer-level monetary totals to transaction totals.

## Interpretation
RFM is a descriptive segmentation technique, not a prediction of intent. Validate segment stability and test campaigns before making business claims.
