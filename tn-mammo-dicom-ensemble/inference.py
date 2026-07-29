"""Inference & Evaluation Script for TN-Mammo DICOM Ensemble (SOTA Macro F1 = 0.7384).

Runs 4-view ensemble inference combining:
  1. E3 Model: DenseNet121 @ 512x512 + Bilateral Fusion + Neighbor Penalty (Weight: 0.5)
  2. E7 Model: ConvNeXt-Tiny @ 1024x1024 + Bilateral Fusion + Safe TTA (Weight: 0.5)

Usage:
    python3 inference.py --config config.yaml --output-dir outputs/ensemble_results
"""

import argparse
import json
from pathlib import Path
import sys

# Ensure src is on sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

import numpy as np
import pandas as pd
import torch
import torch.nn.functional as F
from torch.utils.data import DataLoader
import yaml

from tn_mammo.data.dicom_dataset import DicomFourViewDataset
from tn_mammo.metrics.classification import compute_classification_metrics
from tn_mammo.models.density_model import FourViewDensityModel, ModelOptions

INDEX_TO_LABEL = {0: "A", 1: "B", 2: "C", 3: "D"}


def load_model_from_checkpoint(checkpoint_path: Path, device: torch.device):
    """Load model architecture and weights from checkpoint file."""
    checkpoint = torch.load(checkpoint_path, map_location="cpu", weights_only=True)
    config = checkpoint.get("config", {})["model"]

    options = ModelOptions(
        use_ordinal_head=bool(config.get("use_ordinal_head", False)),
        use_binary_head=bool(config.get("use_binary_head", False)),
        use_cd_head=bool(config.get("use_cd_head", False)),
        imagenet_init=False,
        fusion=str(config.get("fusion", "mean")),
        fusion_dropout=float(config.get("fusion_dropout", 0.1)),
        control_hidden_dim=int(config.get("control_hidden_dim", 608)),
        bilateral_bottleneck_dim=int(config.get("bilateral_bottleneck_dim", 256)),
        use_cbam=bool(config.get("use_cbam", False)),
        use_fpn=bool(config.get("use_fpn", False)),
        freeze_early_layers=bool(config.get("freeze_early_layers", False)),
        backbone=str(config.get("backbone", "densenet121")),
    )

    model = FourViewDensityModel(options)
    state_dict = checkpoint.get("model_state_dict", checkpoint)
    model.load_state_dict(state_dict, strict=True)
    model.to(device)
    model.eval()
    return model


def get_model_probs(model, loader, device, use_tta=False):
    """Get output probability distribution [N, 4] for a dataset."""
    all_probs = []
    with torch.no_grad():
        for batch in loader:
            views = batch["views"].to(device, non_blocking=True)
            with torch.amp.autocast(device_type=device.type, dtype=torch.float16):
                out = model(views)
                if use_tta:
                    views_hflip = torch.flip(views, dims=[-1])
                    out_hflip = model(views_hflip)
                    out["flat_logits"] = (out["flat_logits"] + out_hflip["flat_logits"]) / 2.0

            probs = F.softmax(out["flat_logits"].float(), dim=1).cpu().numpy()
            all_probs.append(probs)
    return np.vstack(all_probs)


def main():
    parser = argparse.ArgumentParser(description="Ensemble Inference for TN-Mammo DICOM")
    parser.add_argument("--config", type=str, default="config.yaml", help="Path to config.yaml")
    parser.add_argument("--output-dir", type=str, default="outputs/ensemble_results", help="Output directory")
    args = parser.parse_args()

    with open(args.config, "r") as f:
        cfg = yaml.safe_load(f)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"[INFO] Running Ensemble Inference on device: {device}")

    # Root base path
    base_dir = Path(__file__).resolve().parent
    e3_ckpt_path = base_dir / cfg["ensemble"]["checkpoints"]["e3"]
    e7_ckpt_path = base_dir / cfg["ensemble"]["checkpoints"]["e7"]

    # 1. Load Models
    print(f"[INFO] Loading E3 Model (DenseNet-512): {e3_ckpt_path}")
    model_e3 = load_model_from_checkpoint(e3_ckpt_path, device)

    print(f"[INFO] Loading E7 Model (ConvNeXt-1024): {e7_ckpt_path}")
    model_e7 = load_model_from_checkpoint(e7_ckpt_path, device)

    # 2. Setup DataLoaders for 512 and 1024 resolutions
    dicom_root = cfg["data"]["dicom_root"]
    test_manifest = cfg["data"]["test_manifest"]

    dataset_512 = DicomFourViewDataset(
        manifest_path=test_manifest,
        dicom_root=dicom_root,
        image_size=512,
        is_train=False,
    )
    dataset_1024 = DicomFourViewDataset(
        manifest_path=test_manifest,
        dicom_root=dicom_root,
        image_size=1024,
        is_train=False,
    )

    loader_512 = DataLoader(dataset_512, batch_size=2, shuffle=False, num_workers=4)
    loader_1024 = DataLoader(dataset_1024, batch_size=2, shuffle=False, num_workers=4)

    # 3. Compute Probabilities
    print("[INFO] Inferring E3 (512x512)...")
    probs_e3 = get_model_probs(model_e3, loader_512, device, use_tta=False)

    print("[INFO] Inferring E7 (1024x1024 + Safe Horizontal Flip TTA)...")
    probs_e7 = get_model_probs(model_e7, loader_1024, device, use_tta=True)

    # 4. Ensemble Probability Averaging (50% E3 + 50% E7)
    w_e3 = cfg["ensemble"]["weights"]["e3"]
    w_e7 = cfg["ensemble"]["weights"]["e7"]
    probs_ensemble = w_e3 * probs_e3 + w_e7 * probs_e7
    preds_ensemble = np.argmax(probs_ensemble, axis=1)

    # Get Ground Truth
    y_true = np.array([sample["label"] for sample in dataset_512.samples])

    # 5. Compute Metrics
    metrics = compute_classification_metrics(y_true, preds_ensemble)

    print("\n" + "=" * 60)
    print(" 🏆 ENSEMBLE TEST RESULTS (SOTA)")
    print("=" * 60)
    print(f"  Macro F1:           {metrics['macro_f1']:.4f}")
    print(f"  Accuracy:           {metrics['accuracy']:.4f}")
    print(f"  Weighted F1:        {metrics['weighted_f1']:.4f}")
    print(f"  QWK:                {metrics['qwk']:.4f}")
    print(f"  Within-One:         {metrics['within_one']:.4f}")
    print(f"  Severe Error Count: {metrics['severe_error_count']}")
    print("\nPer-Class F1:")
    for cls_name, f1_val in metrics["per_class"].items():
        print(f"  Class {cls_name}: F1={f1_val['f1']:.4f} (Prec={f1_val['precision']:.4f}, Rec={f1_val['recall']:.4f})")

    # 6. Save Predictions & Metrics
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    with open(output_dir / "test_metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)

    pred_rows = []
    for i, sample in enumerate(dataset_512.samples):
        pred_rows.append({
            "case_id": sample["case_id"],
            "source": sample["source"],
            "true_index": y_true[i],
            "true_label": INDEX_TO_LABEL[y_true[i]],
            "pred_index": preds_ensemble[i],
            "pred_label": INDEX_TO_LABEL[preds_ensemble[i]],
            "prob_A": float(probs_ensemble[i, 0]),
            "prob_B": float(probs_ensemble[i, 1]),
            "prob_C": float(probs_ensemble[i, 2]),
            "prob_D": float(probs_ensemble[i, 3]),
        })

    pd.DataFrame(pred_rows).to_csv(output_dir / "test_predictions.csv", index=False)
    print(f"\n[DONE] Saved ensemble metrics to {output_dir / 'test_metrics.json'}")
    print(f"[DONE] Saved ensemble predictions to {output_dir / 'test_predictions.csv'}")


if __name__ == "__main__":
    main()
