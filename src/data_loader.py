from pathlib import Path
import pandas as pd

from src.config import TRAIN_FILE, TEST_FILE, MAX_TRAIN_ROWS, MAX_TEST_ROWS


def load_dataset(path: Path, max_rows=None) -> pd.DataFrame:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(
            f"Dataset file not found: {path}\n"
            "Download UNSW-NB15 training/testing CSV files and put them in data/raw/, "
            "or run `python main.py demo` to create a clearly labelled synthetic demo."
        )
    df = pd.read_csv(path, nrows=max_rows, low_memory=False)
    df.columns = [str(c).strip().lower() for c in df.columns]
    if df.empty:
        raise ValueError(f"Dataset is empty: {path}")
    return df


def load_train_test(train_path=TRAIN_FILE, test_path=TEST_FILE,
                    max_train_rows=MAX_TRAIN_ROWS, max_test_rows=MAX_TEST_ROWS):
    train_df = load_dataset(train_path, max_train_rows)
    test_df = load_dataset(test_path, max_test_rows)
    required = {"label", "attack_cat"}
    for name, df in (("training", train_df), ("testing", test_df)):
        missing = required - set(df.columns)
        if missing:
            raise ValueError(
                f"{name} data is missing columns {sorted(missing)}. "
                "This project expects UNSW-NB15 CSVs with label and attack_cat."
            )
    return train_df, test_df


if __name__ == "__main__":
    train_df, test_df = load_train_test()
    print("Training shape:", train_df.shape)
    print("Testing shape:", test_df.shape)
    print("\nColumns:", train_df.columns.tolist())
    print("\nTraining labels:\n", train_df["label"].value_counts(dropna=False))
    print("\nAttack categories:\n", train_df["attack_cat"].value_counts(dropna=False).head(15))
