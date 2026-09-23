import json
import random
import time
from pathlib import Path
import numpy as np
import pandas as pd
import torch
from sklearn.metrics import accuracy_score, f1_score, cohen_kappa_score, confusion_matrix
from torch.utils.data import DataLoader
from .data import FourViewDataset, assert_disjoint
from .model import (ATTENTION_ARCHITECTURE, RELATIONAL_ARCHITECTURE,
                    SPATIAL_ATTENTION_ARCHITECTURE,
                    ORDINAL_PRIMARY_ARCHITECTURE,
                    ORDINAL_PRIMARY_WIDE_ARCHITECTURE,
                    CONVNEXT_RELATIONAL_ARCHITECTURE,
                    CONVNEXT_HYBRID_SPATIAL_ARCHITECTURE,
                    CONVNEXT_HYBRID_A_GATE_ARCHITECTURE,
                    CONVNEXT_MULTISCALE_ARCHITECTURE,
                    CONVNEXT_MULTISCALE_A_GATE_ARCHITECTURE,
                    CONVNEXT_LOCAL_GLOBAL_A_GATE_ARCHITECTURE,
                    CONVNEXT_LOCAL_GLOBAL_PERVIEW_AUX_ARCHITECTURE,
                    CONVNEXT_LOCAL_GLOBAL_PERVIEW_AUX_MIXSTYLE_ARCHITECTURE,
                    CONVNEXT_DUAL_ENDPOINT_GATE_ARCHITECTURE,
                    CONVNEXT_FINE_D_EXPERT_ARCHITECTURE,
                    CONVNEXT_RNG_ISOLATED_FINE_D_EXPERT_ARCHITECTURE,
                    CONVNEXT_PROJECTION_ADAPTER_ARCHITECTURE,
                    CONVNEXT_BILATERAL_RELATION_ARCHITECTURE,
                    CONVNEXT_MULTISCALE_A_EXPERT_ARCHITECTURE,
                    DensityModel)
from .loss import MultiTaskLoss
from .tracking import log_epoch
from .sampling import training_sampler
from .optim import build_optimizer

ARCHITECTURE = RELATIONAL_ARCHITECTURE
SUPPORTED_ARCHITECTURES = {
    RELATIONAL_ARCHITECTURE, ATTENTION_ARCHITECTURE,
    SPATIAL_ATTENTION_ARCHITECTURE, ORDINAL_PRIMARY_ARCHITECTURE,
    ORDINAL_PRIMARY_WIDE_ARCHITECTURE, CONVNEXT_RELATIONAL_ARCHITECTURE,
    CONVNEXT_HYBRID_SPATIAL_ARCHITECTURE,
    CONVNEXT_HYBRID_A_GATE_ARCHITECTURE,
    CONVNEXT_MULTISCALE_ARCHITECTURE,
    CONVNEXT_MULTISCALE_A_GATE_ARCHITECTURE,
    CONVNEXT_LOCAL_GLOBAL_A_GATE_ARCHITECTURE,
    CONVNEXT_LOCAL_GLOBAL_PERVIEW_AUX_ARCHITECTURE,
    CONVNEXT_LOCAL_GLOBAL_PERVIEW_AUX_MIXSTYLE_ARCHITECTURE,
    CONVNEXT_DUAL_ENDPOINT_GATE_ARCHITECTURE,
    CONVNEXT_FINE_D_EXPERT_ARCHITECTURE,
    CONVNEXT_RNG_ISOLATED_FINE_D_EXPERT_ARCHITECTURE,
    CONVNEXT_PROJECTION_ADAPTER_ARCHITECTURE,
    CONVNEXT_BILATERAL_RELATION_ARCHITECTURE,
    CONVNEXT_MULTISCALE_A_EXPERT_ARCHITECTURE,
}


def set_training_phase(model, epoch, freeze_backbone_epochs=0,
                       freeze_backbone_batchnorm=False):
    """Configure backbone warm-up and optional fixed BatchNorm statistics."""
    model.train()
    frozen = epoch <= freeze_backbone_epochs
    model.features.requires_grad_(not frozen)
    if frozen:
        model.features.eval()
    elif freeze_backbone_batchnorm:
        # Keep pretrained running statistics fixed for small training batches,
        # while retaining gradients for convolution and BatchNorm affine terms.
        for module in model.features.modules():
            if isinstance(module, torch.nn.modules.batchnorm._BatchNorm):
                module.eval()
    return frozen


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


def train(config, train_manifest, valid_manifest, output, device, tracker=None):
    output = Path(output)
    if output.exists() and any(output.iterdir()):
        raise FileExistsError("Use a new empty output directory to preserve previous runs")
    seed = int(config["seed"])
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.backends.cudnn.benchmark = False
    torch.backends.cudnn.deterministic = True
    input_mode = config.get("input_mode", "dicom")
    resize_mode = config.get("resize_mode", "stretch")
    train_data = FourViewDataset(train_manifest, config["image_size"], training=True,
                                 input_mode=input_mode, resize_mode=resize_mode,
                                 augmentation=config.get("augmentation"))
    valid_data = FourViewDataset(valid_manifest, config["image_size"], input_mode=input_mode,
                                 resize_mode=resize_mode)
    assert_disjoint(train_data, valid_data)
    counts = np.bincount(train_data.labels, minlength=4).tolist()
    criterion = MultiTaskLoss(counts, **config["loss"]).to(device)
    settings = config["training"]
    sampler, sampling_probabilities = training_sampler(
        train_data.labels, float(settings.get("sampling_power", 0)), seed)
    if int(settings["epochs"]) < 1 or int(settings["patience"]) < 1:
        raise ValueError("epochs and patience must be positive")
    min_epochs = int(settings.get("min_epochs", 1))
    freeze_epochs = int(settings.get("freeze_backbone_epochs", 0))
    freeze_backbone_batchnorm = bool(settings.get("freeze_backbone_batchnorm", False))
    if not 0 <= freeze_epochs < int(settings["epochs"]):
        raise ValueError("freeze_backbone_epochs must be in [0, epochs)")
    if not 1 <= min_epochs <= int(settings["epochs"]):
        raise ValueError("min_epochs must be between 1 and epochs")
    if tracker is not None:
        tracker.summary.update({"train_class_counts": counts,
                                "sampling_class_probabilities": sampling_probabilities,
                                "valid_class_counts": np.bincount(valid_data.labels, minlength=4).tolist(),
                                "selection_metric": "four_class_macro_f1", "cal_outer_used": False,
                                "gpu": torch.cuda.get_device_name(device) if device.type == "cuda" else "cpu",
                                "torch_version": str(torch.__version__)})
        (output.parent / (output.name + "_wandb.json")).write_text(
            json.dumps({"id": tracker.id, "url": tracker.url}))
    loader_args = dict(batch_size=int(settings["batch_size"]), num_workers=int(settings["num_workers"]))
    train_loader = DataLoader(train_data, shuffle=sampler is None, sampler=sampler,
                              generator=torch.Generator().manual_seed(seed), **loader_args)
    valid_loader = DataLoader(valid_data, shuffle=False,
                              **{**loader_args, "num_workers": int(settings.get(
                                  "valid_num_workers", loader_args["num_workers"]))})
    model = DensityModel(**config["model"]).to(device)
    optimizer = build_optimizer(model, settings)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=settings["epochs"])
    amp = bool(settings["amp"]) and device.type == "cuda"
    scaler = torch.amp.GradScaler("cuda", enabled=amp)
    output.mkdir(parents=True, exist_ok=True)
    best, stale, history = -1., 0, []
    for epoch in range(1, settings["epochs"] + 1):
        started = time.monotonic()
        learning_rate = optimizer.param_groups[0]["lr"]
        backbone_frozen = set_training_phase(
            model, epoch, freeze_epochs, freeze_backbone_batchnorm)
        totals = dict(loss=0., focal=0., ordinal=0., binary=0., neighbor=0.)
        seen = 0
        sampled_counts = np.zeros(4, dtype=np.int64)
        skipped_updates = 0
        for batch in train_loader:
            sampled_counts += np.bincount(batch["label"].numpy(), minlength=4)
            views, labels = batch["views"].to(device), batch["label"].to(device)
            optimizer.zero_grad(set_to_none=True)
            with torch.amp.autocast(device_type=device.type, enabled=amp):
                loss, parts = criterion(model(views), labels)
            if not torch.isfinite(loss):
                raise FloatingPointError("Non-finite training loss")
            scaler.scale(loss).backward()
            scaler.unscale_(optimizer)
            # GradScaler skips overflowing FP16 updates and lowers its scale.
            # Raising here would prevent that normal recovery on the first batches.
            norm = torch.nn.utils.clip_grad_norm_(model.parameters(), 5., error_if_nonfinite=not amp)
            skipped_updates += int(not torch.isfinite(norm))
            scaler.step(optimizer)
            scaler.update()
            seen += len(labels)
            totals["loss"] += float(loss.detach()) * len(labels)
            for key, value in parts.items():
                totals.setdefault(key, 0.)
                totals[key] += float(value) * len(labels)
        scheduler.step()
        predictions = predict(model, valid_loader, device)
        report = metrics(predictions.true_index, predictions.pred_index)
        record = {"epoch": epoch, "train": {k: v / seen for k, v in totals.items()},
                  "sampled_class_counts": sampled_counts.tolist(),
                  "backbone_frozen": backbone_frozen,
                  "backbone_batchnorm_frozen": freeze_backbone_batchnorm,
                  "amp_skipped_updates": skipped_updates, "valid": report,
                  "seconds": time.monotonic() - started, "learning_rate": learning_rate}
        history.append(record)
        print(json.dumps(record), flush=True)
        is_best = report["macro_f1"] > best
        if is_best:
            best, stale = report["macro_f1"], 0
            torch.save({"architecture": model.architecture, "config": config, "epoch": epoch,
                        "model_state_dict": model.state_dict(), "valid_metrics": report,
                        "class_counts": counts, "train_manifest": str(Path(train_manifest).resolve()),
                        "valid_manifest": str(Path(valid_manifest).resolve())}, output / "best.pt")
            predictions.to_csv(output / "valid_predictions.csv", index=False)
        else:
            stale += 1
        (output / "history.json").write_text(json.dumps(history, indent=2))
        log_epoch(tracker, record, is_best)
        if epoch >= min_epochs and stale >= settings["patience"]:
            break
    if tracker is not None:
        tracker.summary.update({"completed_epochs": epoch,
                                "stopped_early": epoch < settings["epochs"]})


def load_model(checkpoint_path, device):
    checkpoint = torch.load(checkpoint_path, map_location="cpu", weights_only=True)
    if checkpoint.get("architecture") not in SUPPORTED_ARCHITECTURES:
        raise ValueError("Checkpoint architecture is incompatible; train this pipeline first")
    options = dict(checkpoint["config"]["model"], pretrained=False)
    model = DensityModel(**options)
    if checkpoint["architecture"] != model.architecture:
        raise ValueError("Checkpoint architecture and model configuration differ")
    model.load_state_dict(checkpoint["model_state_dict"], strict=True)
    return model.to(device).eval(), checkpoint["config"]
