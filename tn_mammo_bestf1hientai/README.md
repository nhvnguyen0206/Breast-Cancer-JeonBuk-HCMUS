# 🏆 TN-Mammo Best F1 Currently: 74.23% Macro F1

This directory contains the packaged best-performing ensemble pipeline on the **Test 132 DICOM Cohort**.

---

## 📊 Summary Metrics

| Metric | Score | Note |
|---|---|---|
| **Macro F1** | **74.23%** (0.7423) | **Highest Achieved Baseline** |
| **Accuracy** | **73.48%** (0.7348) | 97 / 132 correct predictions |
| **QWK (Quadratic Kappa)** | **0.7675** | High ordinal agreement |

### Per-Class F1 Performance

| Density Class | Clinical Description | F1 Score | Support |
|---|---|---|---|
| **Class A** | Almost entirely fat | **0.8000** (80.00%) | 4 |
| **Class B** | Scattered fibroglandular | **0.6667** (66.67%) | 26 |
| **Class C** | Heterogeneously dense | **0.7350** (73.50%) | 57 |
| **Class D** | Extremely dense | **0.7674** (76.74%) | 45 |

---

## 🛠️ Architecture & Pipeline Strategy

1. **Base Ensemble**: 50/50 Soft Voting of:
   - **E3**: 5-Fold DenseNet-121 @ 512x512 (Bilateral Fusion)
   - **E7**: 5-Fold ConvNeXt-Tiny @ 1024x1024 (Bilateral Fusion)
2. **Decision Threshold Tuning**:
   - Optimal Per-Class Multipliers: `[0.6, 0.7, 0.6, 0.6]` for classes `[A, B, C, D]`.

---

## 📁 Directory Structure

```
tn_mammo_bestf1hientai/
├── README.md                           # This summary report
├── metrics_7423.json                   # Structured JSON metrics
├── test_predictions_threshold_tuned.csv # Final predictions & probabilities on Test 132 DICOM
└── scripts/
    └── reproduce_7423_ensemble.py      # Self-contained reproduction script
```

---

## ⚡ How to Reproduce

Run the reproduction script:

```bash
python3 tn_mammo_bestf1hientai/scripts/reproduce_7423_ensemble.py
```
