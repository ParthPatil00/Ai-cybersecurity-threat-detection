import joblib
import pandas as pd

from src.config import (
    BINARY_MODEL_FILE, MULTICLASS_MODEL_FILE, ANOMALY_MODEL_FILE,
    ANOMALY_PREPROCESSOR_FILE, ALERT_DIR, REPORT_DIR,
)
from src.data_loader import load_train_test
from src.preprocessing import split_features_and_targets


def load_detection_models():
    paths = [
        BINARY_MODEL_FILE, MULTICLASS_MODEL_FILE,
        ANOMALY_MODEL_FILE, ANOMALY_PREPROCESSOR_FILE,
    ]
    missing = [str(p) for p in paths if not p.exists()]
    if missing:
        raise FileNotFoundError(
            "Trained model files are missing. Run `python main.py train` first.\n"
            + "\n".join(missing)
        )
    return {
        "binary": joblib.load(BINARY_MODEL_FILE),
        "multiclass": joblib.load(MULTICLASS_MODEL_FILE),
        "anomaly": joblib.load(ANOMALY_MODEL_FILE),
        "anomaly_preprocessor": joblib.load(ANOMALY_PREPROCESSOR_FILE),
    }


def generate_alerts(binary_predictions, multiclass_predictions, anomaly_flags, anomaly_scores):
    alerts = []
    for i, (attack, category, anomaly, score) in enumerate(zip(
        binary_predictions, multiclass_predictions, anomaly_flags, anomaly_scores
    ), start=1):
        is_attack = int(attack) == 1
        is_anomaly = bool(anomaly)
        if not is_attack and not is_anomaly:
            continue
        if is_attack and is_anomaly:
            severity = "HIGH"
            reason = "Classifier and anomaly detector both flagged the record"
        elif is_attack:
            severity = "HIGH"
            reason = "Attack classifier flagged the record"
        else:
            severity = "MEDIUM"
            reason = "Anomaly detector flagged the record"
        alerts.append({
            "event_id": f"EVENT-{i:06d}",
            "predicted_label": "Attack" if is_attack else "Benign",
            "predicted_attack_category": str(category),
            "is_anomaly": is_anomaly,
            "anomaly_score": float(score),
            "severity": severity,
            "reason": reason,
            "status": "REQUIRES_INVESTIGATION",
            "is_confirmed_incident": False,
        })
    return pd.DataFrame(alerts, columns=[
        "event_id", "predicted_label", "predicted_attack_category",
        "is_anomaly", "anomaly_score", "severity", "reason",
        "status", "is_confirmed_incident"
    ])


def run_detection(input_df=None):
    ALERT_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    if input_df is None:
        _, input_df = load_train_test()

    X, _, _ = split_features_and_targets(input_df)
    models = load_detection_models()

    # Reindex defensively to match the feature schema captured at training.
    expected = list(models["binary"].named_steps["preprocessor"].feature_names_in_)
    missing = set(expected) - set(X.columns)
    extra = set(X.columns) - set(expected)
    if missing or extra:
        raise ValueError(
            f"Input feature schema differs from training. Missing={sorted(missing)}; "
            f"extra={sorted(extra)}"
        )
    X = X[expected]

    binary_pred = models["binary"].predict(X)
    multiclass_pred = models["multiclass"].predict(X)
    transformed = models["anomaly_preprocessor"].transform(X)
    anomaly_pred = models["anomaly"].predict(transformed)
    anomaly_flags = anomaly_pred == -1
    anomaly_scores = -models["anomaly"].decision_function(transformed)

    results = input_df.copy()
    results["predicted_label"] = ["Attack" if int(x) == 1 else "Benign" for x in binary_pred]
    results["predicted_attack_category"] = multiclass_pred
    results["is_anomaly"] = anomaly_flags
    results["anomaly_score"] = anomaly_scores
    results.to_csv(REPORT_DIR / "detection_results.csv", index=False)

    alerts = generate_alerts(binary_pred, multiclass_pred, anomaly_flags, anomaly_scores)
    alerts.to_csv(ALERT_DIR / "security_alerts.csv", index=False)

    print("\nDetection summary")
    print("-----------------")
    print(f"Records analyzed: {len(results):,}")
    print(f"Attack predictions: {(binary_pred == 1).sum():,}")
    print(f"Anomaly flags: {anomaly_flags.sum():,}")
    print(f"Alerts generated: {len(alerts):,}")
    print("Detection results:", REPORT_DIR / "detection_results.csv")
    print("Security alerts:", ALERT_DIR / "security_alerts.csv")
    if not alerts.empty:
        print("\nTop alerts:")
        print(alerts.head(10).to_string(index=False))
    return results, alerts


if __name__ == "__main__":
    run_detection()
