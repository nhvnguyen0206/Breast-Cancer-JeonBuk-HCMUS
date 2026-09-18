import argparse
import json
import sys
from pathlib import Path
import torch
from torch.utils.data import DataLoader

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))
from tn_mammo.data import FourViewDataset
from tn_mammo.engine import load_model, predict, metrics


def main():
    parser = argparse.ArgumentParser(description="Predict A/B/C/D using the flat head")
    parser.add_argument("--checkpoint", required=True)
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--batch-size", type=int, default=1)
    parser.add_argument("--num-workers", type=int, default=0)
    parser.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    args = parser.parse_args()
    output = Path(args.output_dir)
    if output.exists() and any(output.iterdir()):
        raise FileExistsError("Use a new empty output directory")
    device = torch.device(args.device)
    model, config = load_model(args.checkpoint, device)
    dataset = FourViewDataset(args.manifest, config["image_size"], require_labels=False)
    rows = predict(model, DataLoader(dataset, batch_size=args.batch_size,
                                    num_workers=args.num_workers), device)
    output.mkdir(parents=True, exist_ok=True)
    rows.to_csv(output / "predictions.csv", index=False)
    if dataset.labels is not None:
        report = metrics(rows.true_index, rows.pred_index)
        (output / "metrics.json").write_text(json.dumps(report, indent=2))
        print(json.dumps(report, indent=2))
    print(f"Predictions: {output / 'predictions.csv'}")


if __name__ == "__main__":
    main()
