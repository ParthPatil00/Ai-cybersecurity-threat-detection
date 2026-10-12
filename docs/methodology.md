# Methodology

## Supervised classification
Random Forest learns from the dataset's binary label and attack-category labels. Binary metrics include precision, recall, F1, and accuracy. Multiclass reports are saved separately.

## Anomaly detection
Isolation Forest is trained on benign training records only. Lower decision-function values are more anomalous; this project negates the decision function so higher displayed scores indicate greater unusualness. These scores are not probabilities of maliciousness.

## Evaluation protocol
Use the supplied train/test split when available. Do not tune thresholds repeatedly against the final test set. For stronger research, create a validation split for model selection and threshold calibration, then preserve the test set for final evaluation.

## Alert rules
The alert severity mapping is illustrative:
- Classifier attack prediction: HIGH
- Anomaly only: MEDIUM
- Both signals: HIGH

A production alert policy requires validation, context, threshold calibration, and analyst feedback.
