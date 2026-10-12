from src.detect import generate_alerts


def main():
    # These flags are manually specified to unit-test alert logic.
    # This is NOT a machine-learning detection result.
    alerts = generate_alerts(
        binary_predictions=[1, 1, 0],
        multiclass_predictions=["DoS", "Reconnaissance", "Normal"],
        anomaly_flags=[True, False, True],
        anomaly_scores=[0.8, 0.2, 0.9],
    )
    print("Synthetic alert-rule test (manually supplied flags):")
    print(alerts.to_string(index=False))


if __name__ == "__main__":
    main()
