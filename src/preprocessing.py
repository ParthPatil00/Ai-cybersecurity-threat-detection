import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

from src.config import DROP_COLUMNS


def clean_dataframe(dataframe: pd.DataFrame) -> pd.DataFrame:
    df = dataframe.copy()
    df.columns = [str(c).strip().lower() for c in df.columns]
    numeric = df.select_dtypes(include=["number"]).columns
    df[numeric] = df[numeric].replace([np.inf, -np.inf], np.nan)
    return df.drop_duplicates().reset_index(drop=True)


def split_features_and_targets(dataframe: pd.DataFrame):
    df = clean_dataframe(dataframe)
    required = {"label", "attack_cat"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing target columns: {sorted(missing)}")

    y_binary = pd.to_numeric(df["label"], errors="coerce")
    if y_binary.isna().any():
        raise ValueError("The label column contains non-numeric or missing values.")
    y_binary = y_binary.astype(int)
    if not set(y_binary.unique()).issubset({0, 1}):
        raise ValueError("The binary label column must contain only 0 and 1.")

    attack_categories = df["attack_cat"].fillna("Unknown").astype(str).str.strip()
    attack_categories = attack_categories.replace({"": "Unknown", "-": "Unknown"})
    # Dataset convention: label 0 is benign. Do not rely on the attack_cat
    # value for benign rows; force a stable class name.
    y_multiclass = attack_categories.where(y_binary.eq(1), "Normal")

    drop = [c for c in DROP_COLUMNS if c in df.columns]
    X = df.drop(columns=drop)
    if X.empty:
        raise ValueError("No predictor columns remain after removing labels/identifiers.")
    assert "label" not in X.columns and "attack_cat" not in X.columns
    return X, y_binary, y_multiclass


def build_preprocessor(X: pd.DataFrame):
    categorical = X.select_dtypes(include=["object", "category", "bool"]).columns.tolist()
    numerical = [c for c in X.columns if c not in categorical]

    numeric_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
    ])
    categorical_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore")),
    ])
    return ColumnTransformer([
        ("numeric", numeric_pipeline, numerical),
        ("categorical", categorical_pipeline, categorical),
    ], remainder="drop")
