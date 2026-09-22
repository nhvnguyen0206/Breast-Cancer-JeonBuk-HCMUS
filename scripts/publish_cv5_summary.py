"""Publish audited CV5 aggregate results, without per-case records or model files."""
import argparse
import json
import math
from pathlib import Path
import statistics

import wandb


def publish(path, entity, project, mean_threshold=0.75, sd_threshold=None,
            minimum_threshold=None):
    report = json.loads(Path(path).read_text())
    if report.get("audit") != "PASS" or report.get("independent_test") is not False:
        raise ValueError("Expected an audited selected-DEV report")
    folds = report["folds"]
    if [f["fold"] for f in folds] != list(range(5)):
        raise ValueError("Expected all five folds in order")
    for fold in folds:
        if fold.get("wandb_state") != "finished":
            raise ValueError("All source runs must be verified finished")
    values = [f["best"]["macro_f1"] for f in folds]
    if not math.isclose(statistics.mean(values), report["aggregate"]["macro_f1_mean"], abs_tol=1e-12):
        raise ValueError("Aggregate mismatch")
    arm = report["arm"]
    key = "density-cv5-seed42-" + arm
    api = wandb.Api(timeout=30)
    existing = list(api.runs(entity + "/" + project, filters={"config.summary_key": key}))
    if existing:
        if len(existing) != 1 or existing[0].state != "finished":
            raise ValueError("Summary already exists but is not uniquely finished; inspect before retry")
        previous = existing[0]
        if (previous.config.get("assignments_sha256") != report["assignments_sha256"]
                or not math.isclose(previous.summary.get("cv5/macro_f1_mean", -1), statistics.mean(values), abs_tol=1e-12)):
            raise ValueError("Existing summary differs from supplied report")
        return {"id": previous.id, "url": previous.url, "reused": True}
    config = {"summary_key": key, "arm": arm, "training_seed": 42,
              "split_seed": 42, "n_folds": 5, "epochs_per_fold": 50,
              "independent_test": False, "selection": "best DEV Macro-F1 within each fold",
              "assignments_sha256": report["assignments_sha256"],
              "source_run_ids": [f["wandb_id"] for f in folds]}
    with wandb.init(entity=entity, project=project, job_type="cv5_summary",
                    name=key + "-summary", group="density-cv5-audited-summaries",
                    config=config, tags=["cv5", "audited", "selected-dev", arm]) as run:
        summary = {}
        for name, value in report["aggregate"].items():
            if isinstance(value, (int, float)):
                summary["cv5/" + name] = value
        for index, label in enumerate("ABCD"):
            summary["cv5/f1_" + label + "_mean"] = report["aggregate"]["per_class_f1_mean"][index]
            summary["cv5/support_" + label] = report["support"][index]
        mean_value = statistics.mean(values)
        sample_sd = statistics.stdev(values)
        minimum_value = min(values)
        mean_met = mean_value >= mean_threshold
        sd_met = sd_threshold is None or sample_sd <= sd_threshold
        minimum_met = (minimum_threshold is None
                       or minimum_value >= minimum_threshold)
        summary.update({"audit_passed": True, "independent_test": False,
                        "target_met_single_seed": mean_met and sd_met and minimum_met,
                        "criteria/mean_threshold": mean_threshold,
                        "criteria/mean_met": mean_met,
                        "criteria/sample_sd_threshold": sd_threshold,
                        "criteria/sample_sd_met": sd_met,
                        "criteria/minimum_threshold": minimum_threshold,
                        "criteria/minimum_met": minimum_met,
                        "multi_seed_verified": False,
                        "unique_cases": report["unique_cases"],
                        "pooled_descriptive/macro_f1": report["pooled_descriptive"]["macro_f1"]})
        run.summary.update(summary)
        columns = ["fold", "best_epoch", "macro_f1", "accuracy", "qwk",
                   "f1_A", "f1_B", "f1_C", "f1_D", "epoch50_macro_f1", "source_url"]
        data = [[f["fold"], f["best_epoch"], f["best"]["macro_f1"],
                 f["best"]["accuracy"], f["best"]["qwk"], *f["best"]["per_class_f1"],
                 f["epoch50"]["macro_f1"], f["wandb_url"]] for f in folds]
        run.log({"cv5/fold_results": wandb.Table(columns=columns, data=data)})
        artifact = wandb.Artifact(key + "-audit", type="cv5-audit")
        artifact.add_file(str(path), name="audit.json")
        run.log_artifact(artifact)
        receipt = {"id": run.id, "url": run.url, "reused": False}
    return receipt


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("reports", nargs="+")
    parser.add_argument("--entity", required=True)
    parser.add_argument("--project", default="HCMUS-paper1")
    parser.add_argument("--mean-threshold", type=float, default=0.75)
    parser.add_argument("--sd-threshold", type=float)
    parser.add_argument("--minimum-threshold", type=float)
    args = parser.parse_args()
    for filename in args.reports:
        print(json.dumps(publish(filename, args.entity, args.project,
                                 args.mean_threshold, args.sd_threshold,
                                 args.minimum_threshold)), flush=True)
