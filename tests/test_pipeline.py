import pandas as pd
from src.preprocessing import split_features_and_targets
from src.detect import generate_alerts


def test_target_columns_are_excluded():
    df = pd.DataFrame({
        "id": [1, 2, 3],
        "dur": [0.1, 0.2, 0.3],
        "proto": ["tcp", "udp", "tcp"],
        "label": [0, 1, 1],
        "attack_cat": ["Normal", "DoS", "Exploits"],
    })
    X, y_binary, y_multiclass = split_features_and_targets(df)
    assert "label" not in X.columns
    assert "attack_cat" not in X.columns
    assert "id" not in X.columns
    assert list(y_binary) == [0, 1, 1]
    assert list(y_multiclass) == ["Normal", "DoS", "Exploits"]


def test_alert_rule_output():
    alerts = generate_alerts(
        binary_predictions=[1, 0],
        multiclass_predictions=["DoS", "Normal"],
        anomaly_flags=[True, True],
        anomaly_scores=[0.8, 0.9],
    )
    assert len(alerts) == 2
    assert alerts.iloc[0]["severity"] == "HIGH"
    assert alerts.iloc[1]["severity"] == "MEDIUM"
    assert not alerts["is_confirmed_incident"].any()
