#!/usr/bin/env python3
"""Generate comparison plots, representative Grad-CAMs and tonghop.pdf."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import cv2
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
import pandas as pd
import torch
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tn_mammo.constants import INDEX_TO_LABEL, VIEW_ORDER  # noqa: E402
from tn_mammo.data.dataset import FourViewManifestDataset  # noqa: E402
from tn_mammo.models.density_model import FourViewDensityModel  # noqa: E402


def load_runs(run_specs):
    runs = []
    for name, run_dir, checkpoint, config_path in run_specs:
        run_dir = Path(run_dir)
        metrics = json.loads((run_dir / "best_metrics.json").read_text())
        predictions = pd.read_csv(run_dir / "best_predictions.csv")
        runs.append({
            "name": name, "dir": run_dir, "metrics": metrics,
            "predictions": predictions, "checkpoint": Path(checkpoint),
            "config_path": Path(config_path) if config_path else None,
        })
    return runs


def add_title(fig, title, subtitle=""):
    fig.suptitle(title, fontsize=16, fontweight="bold")
    if subtitle:
        fig.text(0.5, 0.94, subtitle, ha="center", fontsize=9)


def metric_table_page(pdf, runs):
    columns = [
        ("accuracy", "Accuracy"), ("balanced_accuracy", "BalAcc"),
        ("macro_f1", "Macro-F1"), ("weighted_f1", "Weighted-F1"),
        ("auc_macro_ovr", "Macro AUC"), ("qwk", "QWK"),
        ("within_one", "Within-1"), ("ordinal_mae", "Ordinal MAE"),
        ("severe_error_count", "Severe errors"),
    ]
    fig, ax = plt.subplots(figsize=(11.7, 8.3))
    ax.axis("off")
    cells = []
    for run in runs:
        row = [run["name"]]
        for key, _ in columns:
            value = run["metrics"].get(key)
            row.append(f"{value:.4f}" if isinstance(value, float) else str(value))
        cells.append(row)
    table = ax.table(
        cellText=cells, colLabels=["Run", *[x[1] for x in columns]],
        loc="center", cellLoc="center",
    )
    table.auto_set_font_size(False); table.set_fontsize(8); table.scale(1, 1.7)
    add_title(fig, "TN-Mammo experiment comparison", "Validation set only; model selection never uses locked test")
    pdf.savefig(fig, bbox_inches="tight"); plt.close(fig)


def training_page(pdf, runs):
    fig, axes = plt.subplots(2, 2, figsize=(11.7, 8.3))
    keys = [("train_loss", "Train loss"), ("valid_macro_f1", "Macro-F1"),
            ("valid_accuracy", "Accuracy"), ("valid_qwk", "QWK")]
    for run in runs:
        history_path = run["dir"] / "history.jsonl"
        if not history_path.exists():
            continue
        history = pd.read_json(history_path, lines=True)
        for ax, (key, title) in zip(axes.flat, keys):
            if key in history:
                ax.plot(history["epoch"], history[key], label=run["name"])
            ax.set_title(title); ax.set_xlabel("Epoch"); ax.grid(alpha=.2)
    axes[0, 0].legend(fontsize=7)
    add_title(fig, "Training and validation curves")
    fig.tight_layout(rect=(0, 0, 1, .93)); pdf.savefig(fig); plt.close(fig)


def diagnostics_pages(pdf, run):
    metrics = run["metrics"]
    cm = np.asarray(metrics["confusion_matrix"])
    fig, axes = plt.subplots(1, 2, figsize=(11.7, 5.5))
    for ax, matrix, title in [
        (axes[0], cm, "Counts"),
        (axes[1], cm / np.maximum(cm.sum(1, keepdims=True), 1), "Row normalized"),
    ]:
        image = ax.imshow(matrix, cmap="Blues")
        for i in range(4):
            for j in range(4):
                ax.text(j, i, f"{matrix[i,j]:.2f}" if title != "Counts" else str(matrix[i,j]),
                        ha="center", va="center")
        ax.set_xticks(range(4), list("ABCD")); ax.set_yticks(range(4), list("ABCD"))
        ax.set_xlabel("Predicted"); ax.set_ylabel("True"); ax.set_title(title)
        fig.colorbar(image, ax=ax, fraction=.046)
    add_title(fig, f"Confusion matrices — {run['name']}")
    fig.tight_layout(rect=(0, 0, 1, .92)); pdf.savefig(fig); plt.close(fig)

    fig, axes = plt.subplots(1, 2, figsize=(11.7, 5.5))
    for label, curve in metrics.get("roc_curves", {}).items():
        axes[0].plot(curve["fpr"], curve["tpr"], label=f"{label} AUC={metrics['auc_per_class'][label]:.3f}")
    axes[0].plot([0, 1], [0, 1], "--", color="gray")
    axes[0].set(xlabel="False-positive rate", ylabel="True-positive rate", title="One-vs-rest ROC")
    axes[0].legend(); axes[0].grid(alpha=.2)
    per_class = pd.DataFrame(metrics["per_class"]).T[["precision", "recall", "f1"]]
    heat = axes[1].imshow(per_class.values, vmin=0, vmax=1, cmap="YlGn")
    axes[1].set_xticks(range(3), per_class.columns); axes[1].set_yticks(range(4), per_class.index)
    for i in range(4):
        for j in range(3):
            axes[1].text(j, i, f"{per_class.iloc[i,j]:.3f}", ha="center", va="center")
    axes[1].set_title("Per-class metrics"); fig.colorbar(heat, ax=axes[1])
    add_title(fig, f"ROC/AUC and class heatmap — {run['name']}")
    fig.tight_layout(rect=(0, 0, 1, .92)); pdf.savefig(fig); plt.close(fig)


def gradcam_pages(pdf, run, manifest):
    checkpoint = torch.load(run["checkpoint"], map_location="cpu", weights_only=True)
    config = checkpoint.get("config", {})
    if run["config_path"]:
        config = yaml.safe_load(run["config_path"].read_text())
    data = config.get("data", {})
    dataset = FourViewManifestDataset(
        manifest, int(data.get("image_size", 224)), training=False,
        transform_options=data.get("preprocessing"),
    )
    model = FourViewDensityModel(bool(config.get("model", {}).get("use_ordinal_head", True)))
    model.load_state_dict(checkpoint["model_state_dict"], strict=True)
    model.eval()
    activations, gradients = [], []
    layer = model.backbone.features.denseblock4
    forward_handle = layer.register_forward_hook(lambda _m, _i, out: activations.append(out))
    backward_handle = layer.register_full_backward_hook(lambda _m, _gi, go: gradients.append(go[0]))

    pred = run["predictions"]
    chosen = []
    for label in range(4):
        match = pred[(pred.y_true == label) & (pred.y_pred == label)]
        if len(match): chosen.append(int(match.index[0]))
    errors = pred[pred.y_true != pred.y_pred].copy()
    errors["distance"] = (errors.y_true - errors.y_pred).abs()
    chosen.extend(int(i) for i in errors.sort_values("distance", ascending=False).index[:4])

    for index in dict.fromkeys(chosen):
        sample = dataset[index]
        views = sample["views"].unsqueeze(0).requires_grad_(True)
        activations.clear(); gradients.clear(); model.zero_grad(set_to_none=True)
        output = model(views)
        predicted = int(output["flat_logits"].argmax(1))
        output["flat_logits"][0, predicted].backward()
        activation, gradient = activations[-1].detach(), gradients[-1].detach()
        weights = gradient.mean(dim=(2, 3), keepdim=True)
        cams = torch.relu((weights * activation).sum(1)).numpy()

        fig, axes = plt.subplots(1, 4, figsize=(11.7, 3.5))
        for view_index, ax in enumerate(axes):
            image = views[0, view_index].detach().permute(1, 2, 0).numpy()
            image = image * np.array([.229, .224, .225]) + np.array([.485, .456, .406])
            image = np.clip(image, 0, 1)
            cam = cv2.resize(cams[view_index], (image.shape[1], image.shape[0]))
            cam = cam / max(float(cam.max()), 1e-8)
            ax.imshow(image); ax.imshow(cam, cmap="jet", alpha=.40, vmin=0, vmax=1)
            ax.set_title(VIEW_ORDER[view_index]); ax.axis("off")
        truth = int(sample["label"])
        add_title(
            fig, f"Grad-CAM — {run['name']} — case {sample['case_id']}",
            f"True={INDEX_TO_LABEL[truth]}  Pred={INDEX_TO_LABEL[predicted]}  "
            f"{'CORRECT' if truth == predicted else 'ERROR'}",
        )
        fig.tight_layout(rect=(0, 0, 1, .86)); pdf.savefig(fig); plt.close(fig)
    forward_handle.remove(); backward_handle.remove()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--output", default=str(ROOT / "tonghop.pdf"))
    parser.add_argument("--run", action="append", nargs=4, metavar=("NAME", "DIR", "CHECKPOINT", "CONFIG"))
    args = parser.parse_args()
    specs = [(name, directory, checkpoint, None if config == "-" else config)
             for name, directory, checkpoint, config in args.run]
    runs = load_runs(specs)
    with PdfPages(args.output) as pdf:
        metric_table_page(pdf, runs)
        training_page(pdf, runs)
        for run in runs:
            diagnostics_pages(pdf, run)
            gradcam_pages(pdf, run, Path(args.manifest))
    print(f"REPORT_OK {args.output}", flush=True)


if __name__ == "__main__":
    main()
