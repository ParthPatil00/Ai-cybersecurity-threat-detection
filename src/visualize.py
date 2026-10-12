import matplotlib.pyplot as plt
import seaborn as sns

from src.config import FIGURE_DIR
from src.data_loader import load_train_test


def create_attack_distribution():
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    train_df, _ = load_train_test()
    counts = train_df["attack_cat"].fillna("Unknown").astype(str).value_counts()

    # Use Matplotlib's barh directly for broad compatibility.
    plt.figure(figsize=(10, 6))
    plt.barh(counts.index.astype(str), counts.values)
    plt.title("Distribution of Network Traffic Categories")
    plt.xlabel("Number of records")
    plt.ylabel("Dataset category")
    plt.tight_layout()

    output = FIGURE_DIR / "attack_distribution.png"
    plt.savefig(output, dpi=160)
    plt.close()
    print("Saved:", output)


if __name__ == "__main__":
    create_attack_distribution()
