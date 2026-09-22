"""Launch one fresh density-CV fold with explicit manifest/protocol provenance."""
import argparse
import hashlib
import json
from pathlib import Path
import sys

import pandas as pd
import torch
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from tn_mammo.engine import train
from tn_mammo.tracking import start_run


def configure(config_path, split_root, fold):
    split_root = Path(split_root)
    audit = json.loads((split_root / "audit.json").read_text())
    if audit["schema"] != "tn_mammo.density_grouped_cv.v1" or not 0 <= fold < audit["n_splits"]:
        raise ValueError("Invalid density-CV protocol or fold")
    assignment_path = split_root / "assignments.csv"
    if hashlib.sha256(assignment_path.read_bytes()).hexdigest() != audit["assignments_sha256"]:
        raise ValueError("Assignment hash mismatch")
    assigned = pd.read_csv(assignment_path, dtype={"case_id": str})
    paths = [split_root / f"fold_{fold}" / f"{role}.csv" for role in ("fit", "dev")]
    for role, path in zip(("fit", "dev"), paths):
        actual = pd.read_csv(path, dtype=str).sort_values("case_id").reset_index(drop=True)
        expected = assigned[assigned.fold != fold] if role == "fit" else assigned[assigned.fold == fold]
        expected = expected.sort_values("case_id").reset_index(drop=True)
        columns = ["case_id", "label", "L_CC", "L_MLO", "R_CC", "R_MLO"]
        if not actual[columns].equals(expected[columns]):
            raise ValueError(f"{role} manifest differs from registered assignment")
    config = yaml.safe_load(Path(config_path).read_text())
    if config["training"]["epochs"] != 50 or config["training"].get("min_epochs") != 50:
        raise ValueError("This campaign requires a full 50 epochs")
    arm = config.get("experiment", {}).get("arm", "baseline")
    seed = config["seed"]
    suffix = "" if arm == "baseline" else f"-{arm}"
    config["wandb"]["name"] = f"vindr-densityCV5-v1{suffix}-fold{fold}-5090-seed{seed}-full50"
    config["wandb"]["group"] = f"vindr-densityCV5-v1{suffix}-seed{seed}-full50"
    config["experiment"] = {"protocol": audit["schema"], "fold": fold,
                            "split_seed": audit["seed"], "n_folds": audit["n_splits"],
                            "assignments_sha256": audit["assignments_sha256"],
                            "initialization": "fresh_imagenet", "independent_test": False,
                            "arm": arm}
    return config, paths


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/vindr_cache_5090_full50.yaml")
    parser.add_argument("--split-root", default="data/vindr_density_cv5_seed42_v1")
    parser.add_argument("--fold", required=True, type=int)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--device", default="cuda")
    args = parser.parse_args()
    config, (fit, dev) = configure(args.config, args.split_root, args.fold)
    print(json.dumps({"fold": args.fold, "config": config, "fit": str(fit), "dev": str(dev)}), flush=True)
    with start_run(config, args.output_dir) as tracker:
        train(config, fit, dev, args.output_dir, torch.device(args.device), tracker=tracker)
