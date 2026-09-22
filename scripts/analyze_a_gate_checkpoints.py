"""Compare A-vs-B behavior of registered checkpoints on a fixed manifest."""
import argparse
import json
from pathlib import Path
import sys
import tempfile

import numpy as np
import pandas as pd
import torch
from torch.utils.data import DataLoader

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from tn_mammo.data import FourViewDataset
from tn_mammo.engine import load_model, predict


def distribution(values):
    values = np.asarray(values, dtype=np.float64)
    return {
        "n": int(values.size),
        "min": float(values.min()),
        "median": float(np.median(values)),
        "max": float(values.max()),
        "mean": float(values.mean()),
    }


def summarize(predictions):
    result = {}
    for truth, label in enumerate("AB"):
        rows = predictions[predictions.true_index == truth]
        result[label] = {
            "prob_A": distribution(rows.prob_A),
            "a_minus_b": distribution(rows.prob_A - rows.prob_B),
            "predicted_counts": {
                name: int((rows.pred_index == index).sum())
                for index, name in enumerate("ABCD")
            },
        }
    a_rows = predictions[predictions.true_index == 0]
    result["A_cases"] = [
        {
            "case_id": row.case_id,
            "pred_label": row.pred_label,
            **{f"prob_{label}": float(getattr(row, f"prob_{label}"))
               for label in "ABCD"},
        }
        for row in a_rows.itertuples(index=False)
    ]
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--checkpoint", action="append", required=True,
                        help="ARM=/absolute/path/to/best.pt")
    parser.add_argument("--output", required=True)
    parser.add_argument("--device", default="cuda")
    args = parser.parse_args()
    device = torch.device(args.device)
    if device.type != "cuda" or not torch.cuda.is_available():
        raise RuntimeError("CUDA is required for the registered diagnostic")
    gpu = torch.cuda.get_device_name(device)
    if "5090" not in gpu:
        raise RuntimeError(f"RTX5090 required, got {gpu}")

    source = pd.read_csv(args.manifest, dtype={"case_id": str})
    subset = source[source.label.isin(["A", "B"])].copy()
    if subset.label.value_counts().reindex(["A", "B"], fill_value=0).min() <= 0:
        raise ValueError("Manifest must contain both A and B")

    report = {"gpu": gpu, "manifest": str(Path(args.manifest).resolve()),
              "manifest_rows": len(source), "subset_rows": len(subset),
              "class_counts": subset.label.value_counts().to_dict(),
              "checkpoints": {}}
    with tempfile.TemporaryDirectory() as directory:
        manifest = Path(directory) / "ab.csv"
        subset.to_csv(manifest, index=False)
        for specification in args.checkpoint:
            arm, separator, checkpoint = specification.partition("=")
            if not separator or not arm or not checkpoint or arm in report["checkpoints"]:
                raise ValueError("Each checkpoint must be unique ARM=/path/best.pt")
            model, config = load_model(checkpoint, device)
            data = FourViewDataset(
                manifest, int(config["image_size"]),
                input_mode=config.get("input_mode", "dicom"),
                resize_mode=config.get("resize_mode", "stretch"),
            )
            loader = DataLoader(data, batch_size=2, shuffle=False, num_workers=4)
            predictions = predict(model, loader, device)
            report["checkpoints"][arm] = {
                "architecture": model.architecture,
                "checkpoint": str(Path(checkpoint).resolve()),
                **summarize(predictions),
            }
            del model
            torch.cuda.empty_cache()
    Path(args.output).write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
