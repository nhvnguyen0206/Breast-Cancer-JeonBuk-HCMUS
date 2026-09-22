"""Summarize independently selected DEV metrics within a common epoch horizon."""
import argparse
import json
import math
from pathlib import Path
import statistics


def read_history(path):
    path = Path(path)
    if path.name == "history.json":
        records = json.loads(path.read_text())
    else:
        records = []
        for line in path.read_text().splitlines():
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(record, dict) and "epoch" in record:
                records.append(record)
    if not records:
        raise ValueError(f"No epoch records found in {path}")
    epochs = [int(record["epoch"]) for record in records]
    if epochs != list(range(1, max(epochs) + 1)):
        raise ValueError(f"Epoch sequence is incomplete or duplicated in {path}")
    return records


def summarize(inputs, max_epoch, mean_threshold=0.72, sd_threshold=0.03,
              minimum_threshold=0.65):
    for threshold in (mean_threshold, sd_threshold, minimum_threshold):
        if not math.isfinite(threshold) or not 0 <= threshold <= 1:
            raise ValueError("Thresholds must be finite and in [0,1]")
    if len(inputs) < 2:
        raise ValueError("At least two folds are required for stability statistics")
    folds = []
    for fold, path in sorted(inputs.items()):
        history = read_history(path)
        eligible = [record for record in history if int(record["epoch"]) <= max_epoch]
        if len(eligible) != max_epoch:
            raise ValueError(f"Fold {fold} has not completed epoch {max_epoch}")
        best = max(eligible, key=lambda record: record["valid"]["macro_f1"])
        metrics = best["valid"]
        required = ("macro_f1", "accuracy", "qwk", "per_class_f1",
                    "confusion_matrix")
        if any(key not in metrics for key in required):
            raise ValueError(f"Fold {fold} is missing required metrics")
        numeric = [metrics["macro_f1"], metrics["accuracy"], metrics["qwk"],
                   *metrics["per_class_f1"]]
        if not all(math.isfinite(float(value)) for value in numeric):
            raise ValueError(f"Fold {fold} contains non-finite metrics")
        folds.append({"fold": fold, "selected_epoch": int(best["epoch"]),
                      **{key: metrics[key] for key in required}})
    scores = [record["macro_f1"] for record in folds]
    class_means = [statistics.mean(record["per_class_f1"][index]
                                   for record in folds) for index in range(4)]
    return {
        "selection": f"best DEV macro_f1 independently within epochs 1-{max_epoch}",
        "max_epoch": max_epoch,
        "criteria": {"mean_threshold": mean_threshold,
                     "sample_sd_threshold": sd_threshold,
                     "minimum_threshold": minimum_threshold},
        "folds": folds,
        "aggregate": {
            "macro_f1_mean": statistics.mean(scores),
            "macro_f1_sample_sd": statistics.stdev(scores),
            "macro_f1_min": min(scores),
            "accuracy_mean": statistics.mean(record["accuracy"] for record in folds),
            "qwk_mean": statistics.mean(record["qwk"] for record in folds),
            "per_class_f1_mean": class_means,
            "bcd_f1_mean": statistics.mean(class_means[1:]),
            "mean_gate_met": statistics.mean(scores) >= mean_threshold,
            "sample_sd_gate_met": statistics.stdev(scores) <= sd_threshold,
            "minimum_gate_met": min(scores) >= minimum_threshold,
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--fold", action="append", required=True,
                        help="FOLD=history.json-or-training.log")
    parser.add_argument("--max-epoch", type=int, required=True)
    parser.add_argument("--mean-threshold", type=float, default=0.72)
    parser.add_argument("--sd-threshold", type=float, default=0.03)
    parser.add_argument("--minimum-threshold", type=float, default=0.65)
    args = parser.parse_args()
    if args.max_epoch < 1:
        raise ValueError("max-epoch must be positive")
    inputs = {}
    for value in args.fold:
        key, separator, path = value.partition("=")
        if not separator or not key.isdigit() or int(key) in inputs:
            raise ValueError("Each --fold must be a unique FOLD=PATH pair")
        inputs[int(key)] = path
    print(json.dumps(summarize(inputs, args.max_epoch, args.mean_threshold,
                               args.sd_threshold, args.minimum_threshold), indent=2))


if __name__ == "__main__":
    main()
