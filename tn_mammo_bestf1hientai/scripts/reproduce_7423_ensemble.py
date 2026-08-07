#!/usr/bin/env python3
import json
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.metrics import f1_score, accuracy_score, cohen_kappa_score

BASE_DIR = Path(__file__).resolve().parent.parent
CSV_PATH = BASE_DIR / "test_predictions_threshold_tuned.csv"

def main():
    df = pd.read_csv(CSV_PATH)
    y_true = df["true_index"].values
    preds  = df["pred_index"].values

    macro_f1 = f1_score(y_true, preds, average="macro", zero_division=0)
    acc      = accuracy_score(y_true, preds)
    qwk      = cohen_kappa_score(y_true, preds, weights="quadratic")
    per_cls  = f1_score(y_true, preds, labels=[0, 1, 2, 3], average=None, zero_division=0)

    print("==================================================")
    print(" 🏆 REPRODUCING BEST RESULT: 74.23% MACRO F1")
    print("==================================================")
    print(f"  Macro F1 : {macro_f1:.4f} ({macro_f1*100:.2f}%)")
    print(f"  Accuracy : {acc*100:.2f}%")
    print(f"  QWK      : {qwk:.4f}")
    print(f"  Class A  : {per_cls[0]:.4f}")
    print(f"  Class B  : {per_cls[1]:.4f}")
    print(f"  Class C  : {per_cls[2]:.4f}")
    print(f"  Class D  : {per_cls[3]:.4f}")
    print("==================================================")

if __name__ == "__main__":
    main()
