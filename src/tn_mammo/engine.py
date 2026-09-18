import json
import random
from pathlib import Path
import numpy as np
import pandas as pd
import torch
from sklearn.metrics import accuracy_score, f1_score, cohen_kappa_score, confusion_matrix
from torch.utils.data import DataLoader
from .data import FourViewDataset, assert_disjoint
from .model import DensityModel
from .loss import MultiTaskLoss

ARCHITECTURE = "densenet121_hierarchical_bilateral_multitask_v1"


def metrics(truth, prediction):
    truth, prediction = np.asarray(truth), np.asarray(prediction)
    return {"num_samples": len(truth), "accuracy": float(accuracy_score(truth, prediction)),
            "macro_f1": float(f1_score(truth, prediction, labels=[0, 1, 2, 3],
                                       average="macro", zero_division=0)),
            "per_class_f1": f1_score(truth, prediction, labels=[0, 1, 2, 3],
                                      average=None, zero_division=0).tolist(),
            "qwk": float(cohen_kappa_score(truth, prediction, labels=[0, 1, 2, 3], weights="quadratic")),
            "severe_errors": int((np.abs(truth-prediction) >= 2).sum()),
            "confusion_matrix": confusion_matrix(truth, prediction, labels=[0, 1, 2, 3]).tolist()}


@torch.inference_mode()
def predict(model, loader, device):
    model.eval()
    rows = []
    for batch in loader:
        probabilities = model(batch["views"].to(device))["flat_logits"].float().softmax(1).cpu()
        for case, truth, prob in zip(batch["case_id"], batch["label"].tolist(), probabilities):
            pred = int(prob.argmax())
            rows.append({"case_id": case, "true_index": truth, "pred_index": pred,
                         "pred_label": "ABCD"[pred],
                         **{f"prob_{c}": float(prob[i]) for i, c in enumerate("ABCD")}})
    return pd.DataFrame(rows)


def train(config, train_manifest, valid_manifest, output, device):
    output = Path(output)
    if output.exists() and any(output.iterdir()):
        raise FileExistsError("Use a new empty output directory to preserve previous runs")
    seed = int(config["seed"])
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.backends.cudnn.benchmark = False
    torch.backends.cudnn.deterministic = True
    train_data = FourViewDataset(train_manifest, config["image_size"], training=True)
    valid_data = FourViewDataset(valid_manifest, config["image_size"])
    assert_disjoint(train_data, valid_data)
    counts = np.bincount(train_data.labels, minlength=4).tolist()
    criterion = MultiTaskLoss(counts, **config["loss"]).to(device)
    settings = config["training"]
    if int(settings["epochs"]) < 1 or int(settings["patience"]) < 1:
        raise ValueError("epochs and patience must be positive")
    loader_args = dict(batch_size=int(settings["batch_size"]), num_workers=int(settings["num_workers"]))
    train_loader = DataLoader(train_data, shuffle=True,
                              generator=torch.Generator().manual_seed(seed), **loader_args)
    valid_loader = DataLoader(valid_data, shuffle=False, **loader_args)
    model = DensityModel(**config["model"]).to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=settings["learning_rate"],
                                 weight_decay=settings["weight_decay"])
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=settings["epochs"])
    amp = bool(settings["amp"]) and device.type == "cuda"
    scaler = torch.amp.GradScaler("cuda", enabled=amp)
    output.mkdir(parents=True, exist_ok=True)
    best, stale, history = -1., 0, []
    for epoch in range(1, settings["epochs"] + 1):
        model.train()
        totals = dict(loss=0., focal=0., ordinal=0., binary=0., neighbor=0.)
        seen = 0
        for batch in train_loader:
            views, labels = batch["views"].to(device), batch["label"].to(device)
            optimizer.zero_grad(set_to_none=True)
            with torch.amp.autocast(device_type=device.type, enabled=amp):
                loss, parts = criterion(model(views), labels)
            if not torch.isfinite(loss):
                raise FloatingPointError("Non-finite training loss")
            scaler.scale(loss).backward()
            scaler.unscale_(optimizer)
            torch.nn.utils.clip_grad_norm_(model.parameters(), 5., error_if_nonfinite=True)
            scaler.step(optimizer)
            scaler.update()
            seen += len(labels)
            totals["loss"] += float(loss.detach()) * len(labels)
            for key, value in parts.items():
                totals[key] += float(value) * len(labels)
        scheduler.step()
        predictions = predict(model, valid_loader, device)
        report = metrics(predictions.true_index, predictions.pred_index)
        record = {"epoch": epoch, "train": {k: v / seen for k, v in totals.items()}, "valid": report}
        history.append(record)
        print(json.dumps(record), flush=True)
        if report["macro_f1"] > best:
            best, stale = report["macro_f1"], 0
            torch.save({"architecture": ARCHITECTURE, "config": config, "epoch": epoch,
                        "model_state_dict": model.state_dict(), "valid_metrics": report,
                        "class_counts": counts, "train_manifest": str(Path(train_manifest).resolve()),
                        "valid_manifest": str(Path(valid_manifest).resolve())}, output / "best.pt")
            predictions.to_csv(output / "valid_predictions.csv", index=False)
        else:
            stale += 1
        (output / "history.json").write_text(json.dumps(history, indent=2))
        if stale >= settings["patience"]:
            break


def load_model(checkpoint_path, device):
    checkpoint = torch.load(checkpoint_path, map_location="cpu", weights_only=True)
    if checkpoint.get("architecture") != ARCHITECTURE:
        raise ValueError("Checkpoint architecture is incompatible; train this pipeline first")
    options = dict(checkpoint["config"]["model"], pretrained=False)
    model = DensityModel(**options)
    model.load_state_dict(checkpoint["model_state_dict"], strict=True)
    return model.to(device).eval(), checkpoint["config"]
