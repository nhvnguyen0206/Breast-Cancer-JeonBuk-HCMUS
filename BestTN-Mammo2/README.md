# BestTN-Mammo2 (E3_E7_CLEAN_RETEST_131)

> **Dual-Backbone Probability Blend on Clean Test Cohort (N = 131)**

---

### 📊 Test Set Performance (Clean Test-131, N = 131)

| Metric | Score | Note |
| :--- | :---: | :--- |
| **Macro-F1** | **`0.7438`** (~74.4%) | Primary Ranking Metric |
| **BCD-F1** | **`0.7450`** | Dense Classes (B, C, D) |
| **Quadratic Weighted Kappa (QWK)** | **`0.7862`** | Highest Kappa across all models |
| **Accuracy** | **`73.28%`** | Exact 4-Class Match |

#### 📈 Per-Class F1-Score Breakdown:
* **Class A (Almost Entirely Fatty):** `0.8000`
* **Class B (Scattered Fibroglandular):** `0.6792`
* **Class C (Heterogeneously Dense):** `0.7193`
* **Class D (Extremely Dense):** `0.7765`

---

### 💡 Architecture & Ensembling
* **E3 Model (50% weight):** DenseNet-121 @ 512x512 with Bilateral Gated Relational Fusion + Neighbor Penalty Loss.
* **E7 Model (50% weight):** ConvNeXt-Tiny @ 1024x1024 with Bilateral Fusion + Safe Horizontal Flip TTA.
* **Cohort Note:** Evaluated on clean cohort of 131 complete four-view DICOM cases.

---

### 🚀 Quickstart (Inference)
```bash
python3 inference.py --config config/config.yaml --output-dir outputs/inference_results
```
