from pathlib import Path
import numpy as np
import pandas as pd

from src.config import RAW_DATA_DIR, RANDOM_STATE


def make_synthetic_dataset(n_rows=4000, seed=RANDOM_STATE):
    """Create illustrative synthetic flow records; NOT real network traffic."""
    rng = np.random.default_rng(seed)
    attack = rng.binomial(1, 0.32, size=n_rows)
    proto = rng.choice(["tcp", "udp", "icmp"], size=n_rows, p=[0.65, 0.30, 0.05])
    service = rng.choice(["http", "dns", "ssh", "ftp", "other"], size=n_rows)
    state = rng.choice(["CON", "FIN", "INT", "REQ"], size=n_rows, p=[0.4, 0.3, 0.2, 0.1])

    # Attacks have shifted distributions so the demo can exercise the pipeline.
    duration = rng.gamma(shape=2.0, scale=1.2, size=n_rows)
    src_bytes = rng.lognormal(mean=6.2, sigma=1.1, size=n_rows)
    dst_bytes = rng.lognormal(mean=6.0, sigma=1.0, size=n_rows)
    packets = rng.poisson(lam=18, size=n_rows) + 1
    sload = rng.lognormal(mean=4.2, sigma=0.8, size=n_rows)
    dload = rng.lognormal(mean=4.0, sigma=0.9, size=n_rows)

    duration[attack == 1] *= rng.choice([0.15, 1.0, 3.5], size=(attack == 1).sum())
    src_bytes[attack == 1] *= rng.choice([0.2, 1.0, 5.0], size=(attack == 1).sum())
    packets[attack == 1] += rng.poisson(lam=25, size=(attack == 1).sum())

    attack_names = np.array(["Normal", "DoS", "Reconnaissance", "Exploits", "Generic"])
    attack_cat = np.full(n_rows, "Normal", dtype=object)
    if (attack == 1).any():
        attack_cat[attack == 1] = rng.choice(
            attack_names[1:], size=(attack == 1).sum(),
            p=[0.35, 0.25, 0.20, 0.20]
        )

    return pd.DataFrame({
        "id": np.arange(1, n_rows + 1),
        "dur": duration.round(5),
        "proto": proto,
        "service": service,
        "state": state,
        "spkts": packets,
        "sbytes": src_bytes.round(2),
        "dbytes": dst_bytes.round(2),
        "sload": sload.round(3),
        "dload": dload.round(3),
        "label": attack,
        "attack_cat": attack_cat,
    })


def create_demo_files(n_train=3000, n_test=1000):
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
    train = make_synthetic_dataset(n_train, RANDOM_STATE)
    test = make_synthetic_dataset(n_test, RANDOM_STATE + 1)
    train_path = RAW_DATA_DIR / "UNSW_NB15_training-set.csv"
    test_path = RAW_DATA_DIR / "UNSW_NB15_testing-set.csv"
    train.to_csv(train_path, index=False)
    test.to_csv(test_path, index=False)
    print("Created synthetic demo files:")
    print(" ", train_path, train.shape)
    print(" ", test_path, test.shape)
    print("NOTE: These are synthetic illustrative records, not UNSW-NB15 data.")
    return train_path, test_path
