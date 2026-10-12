# Architecture

```text
Dataset CSVs -> Validation -> Preprocessing
                           -> Random Forest binary classifier
                           -> Random Forest multiclass classifier
                           -> Isolation Forest anomaly detector
                           -> Alert rules -> CSV reports and Streamlit dashboard
```

## Data flow
1. Read training/testing CSV files.
2. Separate predictor columns from labels.
3. Fit preprocessing on training/reference data only.
4. Train supervised classifiers and an unsupervised anomaly detector.
5. Evaluate on the held-out test file.
6. Produce predictions, anomaly scores, and investigation alerts.
7. Visualize results locally.

## Trust boundaries
This is a local educational prototype. It does not capture packets, block traffic, or connect to production systems.
