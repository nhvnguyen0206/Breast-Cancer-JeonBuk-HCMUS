"""Inference script for BestTN-Mammo5 (E3_E7_E9_TRIPLE_BLEND).

Weights: 0.40 * E3 + 0.40 * E7 + 0.20 * E9
Reference Performance: N=132, Macro-F1 = 0.7375, QWK = 0.7651, Accuracy = 0.7273
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import torch
import torch.nn.functional as F
import yaml
from torch.utils.data import DataLoader

PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from tn_mammo.constants import INDEX_TO_LABEL
from tn_mammo.data.dicom_dataset import DicomFourViewDataset
from tn_mammo.metrics.classification import compute_classification_metrics
from tn_mammo.models.density_model import FourViewDensityModel, ModelOptions


def load_checkpoint_model(ckpt_path: Path, device: torch.device):
    ckpt = torch.load(ckpt_path, map_location="cpu", weights_only=False)
    cfg = ckpt.get("config", {}).get("model", {})
    options = ModelOptions(
        backbone=cfg.get("backbone", "densenet121"),
        fusion=cfg.get("fusion", "mean"),
        fusion_dropout=float(cfg.get("fusion_dropout", 0.1)),
        control_hidden_dim=int(cfg.get("control_hidden_dim", 608)),
        bilateral_bottleneck_dim=int(cfg.get("bilateral_bottleneck_dim", 256)),
        use_cbam=bool(cfg.get("use_cbam", False)),
        use_fpn=bool(cfg.get("use_fpn", False)),
        use_ordinal_head=bool(cfg.get("use_ordinal_head", False)),
        use_binary_head=bool(cfg.get("use_binary_head", False)),
        use_cd_head=bool(cfg.get("use_cd_head", False)),
        imagenet_init=False,
    )
    model = FourViewDensityModel(options)
    state_dict = ckpt.get("model_state_dict", ckpt)
    if "backbone.classifier.weight" in state_dict and state_dict["backbone.classifier.weight"].shape[0] == 4:
        state_dict["flat_head.weight"] = state_dict.pop("backbone.classifier.weight")
        state_dict["flat_head.bias"] = state_dict.pop("backbone.classifier.bias")
    model.load_state_dict(state_dict, strict=False)
    model.to(device)
    model.eval()
    return model


def get_model_probs(model, loader, device, use_tta=False):
    all_probs = []
    with torch.no_grad():
        for batch in loader:
            views = batch["views"].to(device)
            out = model(views)
            flat_logits = out["flat_logits"]
            if use_tta:
                views_hflip = torch.flip(views, dims=[-1])
                out_hflip = model(views_hflip)
                flat_logits = (flat_logits + out_hflip["flat_logits"]) / 2.0
            probs = F.softmax(flat_logits.float(), dim=1).cpu().numpy()
            all_probs.append(probs)
    return np.vstack(all_probs)


def main():
    parser = argparse.ArgumentParser(description="BestTN-Mammo5 Triple Blend Inference")
    parser.add_argument("--config", type=str, default="config/config.yaml", help="Path to config.yaml")
    parser.add_argument("--output-dir", type=str, default="outputs/inference_results", help="Output directory")
    parser.add_argument("--dicom-root-raw", type=str, default=None, help="Path to raw DICOM root")
    parser.add_argument("--dicom-root-breast-only", type=str, default=None, help="Path to breast-only DICOM root")
    parser.add_argument("--test-manifest", type=str, default=None, help="Override test_manifest")
    args = parser.parse_args()

    cfg_path = PROJECT_ROOT / args.config
    with open(cfg_path) as f:
        cfg = yaml.safe_load(f)

    out_dir = PROJECT_ROOT / args.output_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    dicom_raw = args.dicom_root_raw or cfg["data"].get("dicom_root_raw", "data/dicoms")
    dicom_bo = args.dicom_root_breast_only or cfg["data"].get("dicom_root_breast_only", dicom_raw)
    test_manifest = args.test_manifest or cfg["data"]["test_manifest"]

    e3_ckpt = PROJECT_ROOT / cfg["ensemble"]["checkpoints"]["e3"]
    e7_ckpt = PROJECT_ROOT / cfg["ensemble"]["checkpoints"]["e7"]
    e9_ckpt = PROJECT_ROOT / cfg["ensemble"]["checkpoints"]["e9"]

    print(f"[INFO] Loading E3: {e3_ckpt}")
    m_e3 = load_checkpoint_model(e3_ckpt, device)
    print(f"[INFO] Loading E7: {e7_ckpt}")
    m_e7 = load_checkpoint_model(e7_ckpt, device)
    print(f"[INFO] Loading E9: {e9_ckpt}")
    m_e9 = load_checkpoint_model(e9_ckpt, device)

    # Datasets
    ds_e3 = DicomFourViewDataset(test_manifest, dicom_root=dicom_raw, image_size=512, training=False)
    ds_e7 = DicomFourViewDataset(test_manifest, dicom_root=dicom_raw, image_size=1024, training=False)
    ds_e9 = DicomFourViewDataset(test_manifest, dicom_root=dicom_bo, image_size=1024, training=False, source_representation="breast_only_dicom")

    loader_e3 = DataLoader(ds_e3, batch_size=1, shuffle=False, num_workers=2)
    loader_e7 = DataLoader(ds_e7, batch_size=1, shuffle=False, num_workers=2)
    loader_e9 = DataLoader(ds_e9, batch_size=1, shuffle=False, num_workers=2)

    print("[INFO] Inferring E3 @ 512...")
    probs_e3 = get_model_probs(m_e3, loader_e3, device, use_tta=False)

    print("[INFO] Inferring E7 @ 1024 with Safe Horizontal Flip TTA...")
    probs_e7 = get_model_probs(m_e7, loader_e7, device, use_tta=True)

    print("[INFO] Inferring E9 @ 1024...")
    probs_e9 = get_model_probs(m_e9, loader_e9, device, use_tta=False)

    w_e3 = cfg["ensemble"]["weights"]["e3"]
    w_e7 = cfg["ensemble"]["weights"]["e7"]
    w_e9 = cfg["ensemble"]["weights"]["e9"]
    probs_ens = w_e3 * probs_e3 + w_e7 * probs_e7 + w_e9 * probs_e9
    pred_indices = np.argmax(probs_ens, axis=1)

    df = ds_e3.dataframe
    if "label_idx" in df.columns:
        y_true = df["label_idx"].values.astype(int)
    elif "target" in df.columns:
        y_true = df["target"].values.astype(int)
    elif "density" in df.columns:
        y_true = df["density"].values.astype(int)
    else:
        y_true = None

    pred_rows = []
    for i, row in df.iterrows():
        case_id = row.get("case_id", f"case_{i}")
        t_idx = int(y_true[i]) if y_true is not None else -1
        t_lbl = INDEX_TO_LABEL.get(t_idx, "N/A")
        p_idx = int(pred_indices[i])
        p_lbl = INDEX_TO_LABEL[p_idx]
        pred_rows.append({
            "case_id": case_id,
            "true_index": t_idx,
            "true_label": t_lbl,
            "pred_index": p_idx,
            "pred_label": p_lbl,
            "prob_A": float(probs_ens[i, 0]),
            "prob_B": float(probs_ens[i, 1]),
            "prob_C": float(probs_ens[i, 2]),
            "prob_D": float(probs_ens[i, 3]),
        })

    pred_df = pd.DataFrame(pred_rows)
    pred_csv_path = out_dir / "test_predictions.csv"
    pred_df.to_csv(pred_csv_path, index=False)
    print(f"[INFO] Saved predictions to {pred_csv_path}")

    if y_true is not None:
        metrics = compute_classification_metrics(y_true, pred_indices)
        metrics_path = out_dir / "test_metrics.json"
        with open(metrics_path, "w") as f:
            json.dump(metrics, f, indent=2, default=str)
        print("\n==================================================")
        print("BestTN-Mammo5 INFERENCE RESULTS (TRIPLE BLEND)")
        print("==================================================")
        print(f"Macro-F1          : {metrics['macro_f1']:.4f}")
        print(f"Accuracy          : {metrics['accuracy']*100:.2f}%")
        print(f"QWK (Kappa)       : {metrics['qwk']:.4f}")
        print("==================================================\n")


if __name__ == "__main__":
    main()
