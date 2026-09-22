"""Optional W&B tracking: aggregate metrics only, no medical images or case IDs."""
from contextlib import nullcontext
from pathlib import Path


def start_run(config, output):
    options = config.get("wandb", {})
    if not options.get("enabled", False):
        return nullcontext(None)
    import wandb
    directory = Path(output).parent / "wandb"
    directory.mkdir(parents=True, exist_ok=True)
    run = wandb.init(project=options["project"], entity=options.get("entity"),
                     name=options.get("name"), group=options.get("group"), config=config, dir=str(directory),
                     mode=options.get("mode", "online"),
                     settings=wandb.Settings(disable_git=True, disable_code=True, console="off"))
    run.define_metric("epoch")
    run.define_metric("train/*", step_metric="epoch")
    run.define_metric("valid/*", step_metric="epoch")
    run.define_metric("runtime/*", step_metric="epoch")
    print(f"W&B run: {run.url}", flush=True)
    return run


def log_epoch(run, record, is_best):
    if run is None:
        return
    import wandb
    report = record["valid"]
    values = {"epoch": record["epoch"],
              **{f"train/{k}": v for k, v in record["train"].items()},
              **{f"valid/{k}": report[k] for k in
                 ("accuracy", "macro_f1", "qwk", "severe_errors", "num_samples")},
              **{f"valid/f1_{c}": v for c, v in zip("ABCD", report["per_class_f1"])},
              "runtime/amp_skipped_updates": record.get("amp_skipped_updates", 0)}
    for key in ("seconds", "learning_rate"):
        if key in record:
            values[f"runtime/{key}"] = record[key]
    if "sampled_class_counts" in record:
        values.update({f"train/sampled_{label}": count for label, count in
                       zip("ABCD", record["sampled_class_counts"])})
    if "backbone_frozen" in record:
        values["runtime/backbone_frozen"] = int(record["backbone_frozen"])
    matrix = report["confusion_matrix"]
    values["valid/confusion_matrix"] = wandb.plot_table(
        "wandb/confusion_matrix/v1",
        wandb.Table(columns=["Actual", "Predicted", "nPredictions"],
                    data=[[a, b, matrix[i][j]] for i, a in enumerate("ABCD")
                          for j, b in enumerate("ABCD")]),
        {"Actual": "Actual", "Predicted": "Predicted", "nPredictions": "nPredictions"})
    run.log(values)
    if is_best:
        run.summary.update({"best_epoch": record["epoch"],
                            **{f"best/{k}": v for k, v in report.items()}})
