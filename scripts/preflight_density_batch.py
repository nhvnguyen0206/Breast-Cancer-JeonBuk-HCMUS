"""Run one real cached batch through forward, backward, and optimizer update."""
import argparse
import json
from pathlib import Path
import sys

import numpy as np
import torch
from torch.utils.data import DataLoader
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from tn_mammo.data import FourViewDataset
from tn_mammo.loss import MultiTaskLoss
from tn_mammo.model import DensityModel


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--manifest", required=True)
    args = parser.parse_args()

    if not torch.cuda.is_available():
        raise RuntimeError("CUDA GPU is required")
    device = torch.device("cuda")
    gpu = torch.cuda.get_device_name(0)
    if "5090" not in gpu:
        raise RuntimeError(f"RTX 5090 required, got {gpu}")

    config = yaml.safe_load(Path(args.config).read_text())
    data = FourViewDataset(
        args.manifest,
        image_size=int(config["image_size"]),
        training=True,
        input_mode=config.get("input_mode", "dicom"),
        resize_mode=config.get("resize_mode", "stretch"),
        augmentation=config.get("augmentation"),
    )
    counts = np.bincount(data.labels, minlength=4).tolist()
    loader = DataLoader(
        data,
        batch_size=int(config["training"]["batch_size"]),
        shuffle=False,
        num_workers=0,
    )
    model = DensityModel(**config["model"]).to(device).train()
    criterion = MultiTaskLoss(counts, **config["loss"]).to(device)
    settings = config["training"]
    optimizer = torch.optim.AdamW(
        model.parameters(),
        lr=float(settings["learning_rate"]),
        weight_decay=float(settings["weight_decay"]),
    )
    amp = bool(config["training"].get("amp", False))
    scaler = torch.amp.GradScaler("cuda", enabled=amp)
    torch.cuda.reset_peak_memory_stats(device)
    skipped_updates = 0
    successful_update = False
    for attempt, batch in enumerate(loader, start=1):
        views, labels = batch["views"].to(device), batch["label"].to(device)
        optimizer.zero_grad(set_to_none=True)
        with torch.amp.autocast(device_type="cuda", enabled=amp):
            outputs = model(views)
            loss, parts = criterion(outputs, labels)
        if not torch.isfinite(loss) or not all(torch.isfinite(v).all() for v in outputs.values()):
            raise FloatingPointError("Non-finite output or loss")
        scaler.scale(loss).backward()
        scaler.unscale_(optimizer)
        grad_norm = torch.nn.utils.clip_grad_norm_(
            model.parameters(), 5.0, error_if_nonfinite=not amp
        )
        scale_before = scaler.get_scale()
        scaler.step(optimizer)
        scaler.update()
        if torch.isfinite(grad_norm) and scaler.get_scale() >= scale_before:
            successful_update = True
            break
        skipped_updates += 1
        if attempt == 8:
            break
    if not successful_update:
        raise FloatingPointError("AMP failed to recover within eight real batches")
    torch.cuda.synchronize(device)

    print(json.dumps({
        "preflight": "PASS",
        "gpu": gpu,
        "architecture": model.architecture,
        "batch_shape": list(views.shape),
        "labels": labels.tolist(),
        "loss": float(loss.detach()),
        "loss_parts": {key: float(value) for key, value in parts.items()},
        "grad_norm": float(grad_norm),
        "skipped_updates_before_success": skipped_updates,
        "peak_memory_gib": torch.cuda.max_memory_allocated(device) / 2**30,
        "amp": amp,
    }, indent=2))


if __name__ == "__main__":
    main()
