import json
import joblib
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    classification_report, confusion_matrix,
)

from src.config import (
    BINARY_MODEL_FILE, MULTICLASS_MODEL_FILE, ANOMALY_MODEL_FILE,
    ANOMALY_PREPROCESSOR_FILE, REPORT_DIR, FIGURE_DIR,
)
from src.data_loader import load_train_test
from src.preprocessing import split_features_and_targets


def evaluate_models():
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    _, test_df = load_train_test()
    X_test, y_binary, y_multiclass = split_features_and_targets(test_df)

    binary_model = joblib.load(BINARY_MODEL_FILE)
    binary_pred = binary_model.predict(X_test)
    metrics = {
        "accuracy": float(accuracy_score(y_binary, binary_pred)),
        "precision_attack": float(precision_score(y_binary, binary_pred, zero_division=0)),
        "recall_attack": float(recall_score(y_binary, binary_pred, zero_division=0)),
        "f1_attack": float(f1_score(y_binary, binary_pred, zero_division=0)),
        "test_rows": int(len(y_binary)),
    }
    print("\nBinary classification metrics")
    for key, value in metrics.items():
        print(f"{key}: {value:.4f}" if isinstance(value, float) else f"{key}: {value}")

    binary_report = classification_report(
        y_binary, binary_pred, labels=[0, 1],
        target_names=["Benign", "Attack"], zero_division=0, output_dict=True
    )
    with open(REPORT_DIR / "binary_metrics.json", "w", encoding="utf-8") as f:
        json.dump({"metrics": metrics, "classification_report": binary_report}, f, indent=2)

    cm = confusion_matrix(y_binary, binary_pred, labels=[0, 1])
    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
                xticklabels=["Benign", "Attack"], yticklabels=["Benign", "Attack"])
    plt.title("Binary Classification Confusion Matrix")
    plt.xlabel("Predicted label")
    plt.ylabel("True label")
    plt.tight_layout()
    plt.savefig(FIGURE_DIR / "confusion_matrix.png", dpi=160)
    plt.close()

    multiclass_model = joblib.load(MULTICLASS_MODEL_FILE)
    multiclass_pred = multiclass_model.predict(X_test)
    multiclass_report = classification_report(
        y_multiclass, multiclass_pred, output_dict=True, zero_division=0
    )
    with open(REPORT_DIR / "multiclass_report.json", "w", encoding="utf-8") as f:
        json.dump(multiclass_report, f, indent=2)

    preprocessor = joblib.load(ANOMALY_PREPROCESSOR_FILE)
    anomaly_model = joblib.load(ANOMALY_MODEL_FILE)
    X_transformed = preprocessor.transform(X_test)
    anomaly_pred = anomaly_model.predict(X_transformed)
    anomaly_score = -anomaly_model.decision_function(X_transformed)
    anomaly_df = pd.DataFrame({
        "true_label": y_binary.to_numpy(),
        "true_category": y_multiclass.to_numpy(),
        "is_anomaly": anomaly_pred == -1,
        "anomaly_score": anomaly_score,
    })
    anomaly_df.to_csv(REPORT_DIR / "anomaly_evaluation.csv", index=False)

    plt.figure(figsize=(8, 5))
    plot_df = anomaly_df.copy()
    plot_df["traffic_type"] = plot_df["true_label"].map({0: "Benign", 1: "Attack"})
    sns.histplot(data=plot_df, x="anomaly_score", hue="traffic_type",
                 bins=40, element="step", stat="density", common_norm=False)
    plt.title("Isolation Forest Anomaly Scores by Ground-Truth Label")
    plt.xlabel("Anomaly score (higher = more unusual)")
    plt.ylabel("Density")
    plt.tight_layout()
    plt.savefig(FIGURE_DIR / "anomaly_distribution.png", dpi=160)
    plt.close()

    print("\nMulticlass report saved to:", REPORT_DIR / "multiclass_report.json")
    print("Anomaly outliers:", int((anomaly_pred == -1).sum()))
    print("Reports:", REPORT_DIR)
    print("Figures:", FIGURE_DIR)


if __name__ == "__main__":
    evaluate_models()
