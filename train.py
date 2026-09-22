import argparse
import sys
from pathlib import Path
import torch
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))
from tn_mammo.engine import train
from tn_mammo.tracking import start_run


def main():
    parser = argparse.ArgumentParser(description="Train the original four-view hierarchical model")
    parser.add_argument("--config", default=str(Path(__file__).parent / "configs/train.yaml"))
    parser.add_argument("--train-manifest", required=True)
    parser.add_argument("--valid-manifest", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    args = parser.parse_args()
    with open(args.config) as handle:
        config = yaml.safe_load(handle)
    with start_run(config, args.output_dir) as tracker:
        train(config, args.train_manifest, args.valid_manifest, args.output_dir,
              torch.device(args.device), tracker=tracker)


if __name__ == "__main__":
    main()
