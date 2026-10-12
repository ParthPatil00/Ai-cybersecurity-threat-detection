# AI-Powered Cybersecurity Threat Detection System

A defensive machine-learning prototype that analyzes network-flow records, classifies potential attacks, detects unusual observations, and generates structured security alerts.

**Dataset:** UNSW-NB15 (when supplied by the user)  
**Models:** Random Forest classification + Isolation Forest anomaly detection  
**Dashboard:** Streamlit  
**GPU:** Not required for the baseline

> This is an educational dataset-driven prototype, not a production IDS/SIEM. Predictions are investigation signals, not proof of malicious activity.

## Features
- CSV loading and schema validation
- Binary benign/attack classification
- Multiclass attack-category classification
- Isolation Forest trained on benign reference records
- Accuracy, precision, recall, F1 and confusion matrix
- Anomaly score visualization
- CSV detection results and security alerts
- Streamlit dashboard
- Synthetic demo mode so the pipeline can be tested before downloading a public dataset

## Quick start: run the synthetic demo

Python 3.11 is recommended.

### Windows
```powershell
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python main.py demo
streamlit run dashboard/app.py
```

### macOS/Linux
```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python main.py demo
streamlit run dashboard/app.py
```

The demo generates **synthetic illustrative records**. Synthetic demo results must not be described as UNSW-NB15 results or as evidence of real-world detection performance.

## Use UNSW-NB15
1. Download the appropriate training and testing CSVs from the [official UNSW-NB15 dataset page](https://research.unsw.edu.au/projects/unsw-nb15-dataset).
2. Place them at:
   - `data/raw/UNSW_NB15_training-set.csv`
   - `data/raw/UNSW_NB15_testing-set.csv`
3. Confirm both files include `label` and `attack_cat`.
4. Run:

```bash
python main.py train
python main.py evaluate
python main.py detect
python main.py visualize
python main.py simulate
streamlit run dashboard/app.py
```

`python main.py demo` creates synthetic files with the same expected paths, so use actual UNSW-NB15 files instead when conducting public-dataset experiments.

## Project structure
```text
data/raw/              Local dataset CSVs (not committed)
src/                   Loading, preprocessing, training, detection, evaluation
models/                Locally saved model artifacts (not committed)
outputs/reports/       Metrics and detection results
outputs/alerts/        Structured security alerts
outputs/figures/       Generated graphs
dashboard/app.py       Streamlit dashboard
tests/                 Basic automated tests
docs/                  Methodology, architecture, dataset card, limitations
main.py                CLI entry point
```

## Commands
```bash
python main.py demo       # Generate synthetic data, train, evaluate, detect, graph
python main.py train      # Train on local CSV files
python main.py evaluate   # Evaluate saved models on test data
python main.py detect     # Predict on test data and generate alerts
python main.py simulate   # Replay up to 500 test records through detection
python main.py visualize  # Create traffic-category distribution chart
pytest -q                 # Run basic tests
```

## Architecture
```text
CSV dataset -> validation -> preprocessing
                            -> Random Forest binary classifier
                            -> Random Forest multiclass classifier
                            -> Isolation Forest anomaly detector
                            -> alert rules -> CSV reports and dashboard
```

## Outputs
- `outputs/reports/binary_metrics.json`
- `outputs/reports/multiclass_report.json`
- `outputs/reports/anomaly_evaluation.csv`
- `outputs/reports/detection_results.csv`
- `outputs/reports/simulation_comparison.csv` (dataset replay)
- `outputs/alerts/security_alerts.csv`
- `outputs/figures/confusion_matrix.png`
- `outputs/figures/anomaly_distribution.png`
- `outputs/figures/attack_distribution.png`

Exact metrics depend on the actual dataset, selected sample size, and model configuration. Record measured results after running; do not invent metrics.

## Screenshots
After running the project, add screenshots you personally captured:
- `images/dataset_preview.png`
- `images/confusion_matrix.png`
- `images/anomaly_distribution.png`
- `images/dashboard.png`
- `images/alert_output.png`

## Evaluation
The binary classifier is evaluated using accuracy, precision, recall, F1, and a confusion matrix. The multiclass model has a per-class report. Isolation Forest produces anomaly flags and scores; those scores are not calibrated probabilities.

## Limitations
- The system analyzes offline CSV records, not live packets.
- Dataset patterns may not represent current production networks.
- False positives and false negatives are possible.
- Anomaly does not necessarily mean attack.
- Phishing email and executable malware detection are not implemented.
- Synthetic data is for pipeline demonstration only.
- This project does not block or prevent attacks.

## Future improvements
- Validation-based threshold calibration
- Feature importance / SHAP explanations
- FastAPI prediction endpoint
- Database-backed event storage
- Controlled event replay
- Docker and GitHub Actions
- Additional authentication-log dataset for brute-force analysis

## Responsible use
Use data and systems you are authorized to analyze. Do not deploy this prototype as a production security control without further validation.

## Author
- Name: `parth patil`
- GitHub: `ParthPatil00`
- Repository: `YOUR_REPOSITORY_URL`
