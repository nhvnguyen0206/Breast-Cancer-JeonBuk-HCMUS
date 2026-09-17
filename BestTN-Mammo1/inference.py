"""Inference script for BestTN-Mammo1 (REGION1_ENSEMBLE).

6-model ensemble (3x DenseNet-121 @ 512 + 3x ConvNeXt-Tiny @ 1024)
Reference Performance: Test Macro-F1 = 0.7496, QWK = 0.7749, Accuracy = 0.7121
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import torch
import yaml
from torch.utils.data import DataLoader

PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from tn_mammo.constants import INDEX_TO_LABEL
from tn_mammo.data.dicom_dataset import DicomFourViewDataset
from tn_mammo.metrics.classification import compute_classification_metrics
from tn_mammo.training.engine import build_model, seed_worker


def predict_model_group(ckpt_paths, test_manifest, dicom_root, image_size, source_representation, view_order):
    group_probs = []
    df = None
    
    for ckpt_path in ckpt_paths:
        ckpt_full = PROJECT_ROOT / ckpt_path
        if not ckpt_full.exists():
            raise FileNotFoundError(f"Checkpoint not found: {ckpt_full}")
            
        checkpoint = torch.load(ckpt_full, map_location="cpu", weights_only=False)
        cfg = checkpoint["config"]
        
        model, _ = build_model(cfg)
        model.load_state_dict(checkpoint.get("model_state_dict", checkpoint.get("model_state")))
        model.eval()
        
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        model.to(device)
        
        dataset = DicomFourViewDataset(
            test_manifest,
            dicom_root=dicom_root,
            image_size=image_size,
            training=False,
            source_representation=source_representation,
        )
        if df is None:
            df = dataset.dataframe
            
        g = torch.Generator()
        g.manual_seed(42)
        loader = DataLoader(
            dataset,
            batch_size=1,
            shuffle=False,
            num_workers=2,
            worker_init_fn=seed_worker,
            generator=g,
        )
        
        probs_list = []
        with torch.no_grad():
            for batch in loader:
                views = batch["views"].to(device)
                outputs = model(views)
                probs = torch.softmax(outputs["flat_logits"], dim=-1)
                probs_list.append(probs.cpu().numpy())
                
        model_probs = np.concatenate(probs_list, axis=0)
        group_probs.append(model_probs)
        
    return np.mean(group_probs, axis=0), df


def main():
    parser = argparse.ArgumentParser(description="BestTN-Mammo1 Inference")
    parser.add_argument("--config", type=str, default="config/config.yaml", help="Path to config.yaml")
    parser.add_argument("--output-dir", type=str, default="outputs/inference_results", help="Output directory")
    parser.add_argument("--dicom-root", type=str, default=None, help="Override dicom_root path")
    parser.add_argument("--test-manifest", type=str, default=None, help="Override test_manifest path")
    args = parser.parse_args()

    cfg_path = PROJECT_ROOT / args.config
    with open(cfg_path) as f:
        cfg = yaml.safe_load(f)

    out_dir = PROJECT_ROOT / args.output_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    dicom_root = args.dicom_root or cfg["data"]["dicom_root"]
    test_manifest = args.test_manifest or cfg["data"]["test_manifest"]
    view_order = cfg["data"]["view_order"]
    source_rep = cfg["data"]["source_representation"]

    # 1. E3 Group (3 seeds)
    e3_cfg = cfg["ensemble"]["e3_models"]
    print(f"[INFO] Running E3 Group (DenseNet121 + Region, {len(e3_cfg['checkpoints'])} seeds)...")
    p_e3, df = predict_model_group(
        e3_cfg["checkpoints"], test_manifest, dicom_root,
        e3_cfg["image_size"], source_rep, view_order
    )

    # 2. E7 Group (3 seeds)
    e7_cfg = cfg["ensemble"]["e7_models"]
    print(f"[INFO] Running E7 Group (ConvNeXt-Tiny @ 1024, {len(e7_cfg['checkpoints'])} seeds)...")
    p_e7, _ = predict_model_group(
        e7_cfg["checkpoints"], test_manifest, dicom_root,
        e7_cfg["image_size"], source_rep, view_order
    )

    # 3. Weighted Ensemble
    w_e3 = e3_cfg["weight"]
    w_e7 = e7_cfg["weight"]
    p_ens = w_e3 * p_e3 + w_e7 * p_e7
    pred_indices = np.argmax(p_ens, axis=1)

    # 4. Save results
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
            "prob_A": float(p_ens[i, 0]),
            "prob_B": float(p_ens[i, 1]),
            "prob_C": float(p_ens[i, 2]),
            "prob_D": float(p_ens[i, 3]),
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
        print("BestTN-Mammo1 INFERENCE RESULTS")
        print("==================================================")
        print(f"Macro-F1          : {metrics['macro_f1']:.4f}")
        print(f"Accuracy          : {metrics['accuracy']*100:.2f}%")
        print(f"QWK (Kappa)       : {metrics['qwk']:.4f}")
        print("==================================================\n")


if __name__ == "__main__":
    main()
