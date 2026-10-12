import json
import joblib
import numpy as np
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.pipeline import Pipeline

from src.config import (
    MODEL_DIR, BINARY_MODEL_FILE, MULTICLASS_MODEL_FILE,
    ANOMALY_MODEL_FILE, ANOMALY_PREPROCESSOR_FILE, FEATURES_FILE,
    RANDOM_STATE,
)
from src.data_loader import load_train_test
from src.preprocessing import split_features_and_targets, build_preprocessor


def train_models():
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    train_df, test_df = load_train_test()

    X_train, y_binary, y_multiclass = split_features_and_targets(train_df)
    X_test, _, _ = split_features_and_targets(test_df)

    # Align test columns to training columns; fail on unexpected schema drift.
    missing = set(X_train.columns) - set(X_test.columns)
    extra = set(X_test.columns) - set(X_train.columns)
    if missing or extra:
        raise ValueError(
            f"Feature schema mismatch. Missing in test: {sorted(missing)}; "
            f"extra in test: {sorted(extra)}"
        )
    X_test = X_test[X_train.columns]

    binary_model = Pipeline([
        ("preprocessor", build_preprocessor(X_train)),
        ("classifier", RandomForestClassifier(
            n_estimators=120, max_depth=20, class_weight="balanced",
            random_state=RANDOM_STATE, n_jobs=-1
        )),
    ])
    print("Training binary Random Forest...")
    binary_model.fit(X_train, y_binary)
    joblib.dump(binary_model, BINARY_MODEL_FILE)

    multiclass_model = Pipeline([
        ("preprocessor", build_preprocessor(X_train)),
        ("classifier", RandomForestClassifier(
            n_estimators=120, max_depth=20, class_weight="balanced",
            random_state=RANDOM_STATE, n_jobs=-1
        )),
    ])
    print("Training multiclass Random Forest...")
    multiclass_model.fit(X_train, y_multiclass)
    joblib.dump(multiclass_model, MULTICLASS_MODEL_FILE)

    # Fit anomaly preprocessing only on benign training records.
    benign_X = X_train.loc[y_binary.eq(0)]
    if len(benign_X) < 2:
        raise ValueError("Need at least two benign training rows for Isolation Forest.")
    anomaly_preprocessor = build_preprocessor(X_train)
    benign_transformed = anomaly_preprocessor.fit_transform(benign_X)

    # Bound memory use for sparse/dense transformed features.
    if benign_transformed.shape[0] > 20000:
        rng = np.random.default_rng(RANDOM_STATE)
        chosen = rng.choice(benign_transformed.shape[0], 20000, replace=False)
        benign_transformed = benign_transformed[chosen]

    anomaly_model = IsolationForest(
        n_estimators=120, contamination="auto",
        random_state=RANDOM_STATE, n_jobs=-1
    )
    print("Training Isolation Forest on benign reference records...")
    anomaly_model.fit(benign_transformed)

    joblib.dump(anomaly_model, ANOMALY_MODEL_FILE)
    joblib.dump(anomaly_preprocessor, ANOMALY_PREPROCESSOR_FILE)
    with open(FEATURES_FILE, "w", encoding="utf-8") as f:
        json.dump(list(X_train.columns), f, indent=2)

    print("\nTraining complete.")
    print(f"Training rows: {len(X_train):,}")
    print(f"Testing rows:  {len(X_test):,}")
    print(f"Benign reference rows: {len(benign_X):,}")
    print(f"Models saved in: {MODEL_DIR}")


if __name__ == "__main__":
    train_models()
