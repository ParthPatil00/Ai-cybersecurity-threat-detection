from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = ROOT_DIR / "data" / "raw"
PROCESSED_DATA_DIR = ROOT_DIR / "data" / "processed"
MODEL_DIR = ROOT_DIR / "models"
OUTPUT_DIR = ROOT_DIR / "outputs"
REPORT_DIR = OUTPUT_DIR / "reports"
ALERT_DIR = OUTPUT_DIR / "alerts"
FIGURE_DIR = OUTPUT_DIR / "figures"

TRAIN_FILE = RAW_DATA_DIR / "UNSW_NB15_training-set.csv"
TEST_FILE = RAW_DATA_DIR / "UNSW_NB15_testing-set.csv"

BINARY_MODEL_FILE = MODEL_DIR / "binary_model.joblib"
MULTICLASS_MODEL_FILE = MODEL_DIR / "multiclass_model.joblib"
ANOMALY_MODEL_FILE = MODEL_DIR / "anomaly_model.joblib"
ANOMALY_PREPROCESSOR_FILE = MODEL_DIR / "anomaly_preprocessor.joblib"
FEATURES_FILE = MODEL_DIR / "feature_names.json"

RANDOM_STATE = 42
MAX_TRAIN_ROWS = 50000
MAX_TEST_ROWS = 20000

TARGET_COLUMN = "label"
ATTACK_COLUMN = "attack_cat"
DROP_COLUMNS = ["id", "label", "attack_cat"]
