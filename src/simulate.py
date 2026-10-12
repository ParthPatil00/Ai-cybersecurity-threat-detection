import pandas as pd
from src.config import REPORT_DIR, TEST_FILE
from src.data_loader import load_dataset
from src.detect import run_detection


def run_virtual_simulation(rows=500):
    if not TEST_FILE.exists():
        raise FileNotFoundError(
            "No test CSV found. Run `python main.py demo` for synthetic demo data "
            "or add UNSW-NB15 test data to data/raw/."
        )
    dataset = load_dataset(TEST_FILE, max_rows=rows)
    print("Virtual dataset-replay simulation")
    print("=================================")
    print(f"Records replayed: {len(dataset):,}")
    results, alerts = run_detection(dataset)
    if "label" in dataset.columns:
        comparison = pd.DataFrame({
            "true_label": pd.to_numeric(dataset["label"], errors="coerce").astype("Int64"),
            "predicted_label": results["predicted_label"].map({"Benign": 0, "Attack": 1}),
            "is_anomaly": results["is_anomaly"].astype(bool),
        })
        comparison.to_csv(REPORT_DIR / "simulation_comparison.csv", index=False)
    print("Simulation finished. This is dataset replay, not live packet capture.")
    return results, alerts


if __name__ == "__main__":
    run_virtual_simulation()
