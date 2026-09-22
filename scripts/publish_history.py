"""Publish an existing run's aggregate history; never upload per-case records."""
import argparse
import json
from pathlib import Path
import sys
import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from tn_mammo.tracking import start_run, log_epoch


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--project", default="HCMUS-paper1")
    parser.add_argument("--entity", required=True)
    parser.add_argument("--name", default="vindr-fold0-pilot5-local4090-seed42")
    args = parser.parse_args()
    directory = Path(args.run_dir)
    receipt = directory / "published_wandb.json"
    if receipt.exists():
        raise FileExistsError(f"Already published: {receipt}")
    checkpoint = torch.load(directory / "best.pt", map_location="cpu", weights_only=True)
    config = checkpoint["config"]
    config["wandb"] = {"enabled": True, "mode": "online", "project": args.project,
                       "entity": args.entity, "name": args.name}
    history = json.loads((directory / "history.json").read_text())
    with start_run(config, directory) as run:
        run.summary.update({"historical_import": True, "training_gpu": "RTX 4090",
                            "cal_outer_used": False, "train_class_counts": checkpoint["class_counts"],
                            "valid_class_counts": [sum(row) for row in history[0]["valid"]["confusion_matrix"]],
                            "completed_epochs": len(history)})
        best = -1.
        for record in history:
            is_best = record["valid"]["macro_f1"] > best
            log_epoch(run, record, is_best)
            best = max(best, record["valid"]["macro_f1"])
        receipt.write_text(json.dumps({"id": run.id, "url": run.url}, indent=2))
