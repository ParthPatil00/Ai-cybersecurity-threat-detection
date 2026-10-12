import argparse

from src.config import TRAIN_FILE, TEST_FILE
from src.train import train_models
from src.evaluate import evaluate_models
from src.detect import run_detection
from src.simulate import run_virtual_simulation
from src.visualize import create_attack_distribution
from src.demo_data import create_demo_files


def main():
    parser = argparse.ArgumentParser(
        description="AI-Powered Cybersecurity Threat Detection System"
    )
    parser.add_argument(
        "command",
        choices=["demo", "train", "evaluate", "detect", "simulate", "visualize", "all"],
        help="Pipeline stage to run.",
    )
    args = parser.parse_args()

    if args.command == "demo":
        create_demo_files()
        train_models()
        evaluate_models()
        run_detection()
        create_attack_distribution()
        print("\nSynthetic demo completed. Do not describe synthetic metrics as UNSW-NB15 results.")
    elif args.command == "train":
        train_models()
    elif args.command == "evaluate":
        evaluate_models()
    elif args.command == "detect":
        run_detection()
    elif args.command == "simulate":
        run_virtual_simulation()
    elif args.command == "visualize":
        create_attack_distribution()
    elif args.command == "all":
        if not TRAIN_FILE.exists() or not TEST_FILE.exists():
            raise FileNotFoundError(
                "Dataset files not found. Download UNSW-NB15 into data/raw/ "
                "or run `python main.py demo`."
            )
        train_models()
        evaluate_models()
        run_detection()
        create_attack_distribution()


if __name__ == "__main__":
    main()
