# BestTN-Mammo4 (ENSEMBLE_E3_E7_SOTA)

> **SOTA Canonical DICOM Ensemble (E3 + E7)**

---

### 📊 Test Set Performance (Test-132, N = 132)

| Metric | Score | Note |
| :--- | :---: | :--- |
| **Macro-F1** | **`0.7384`** (~73.8%) | Official Baseline SOTA Benchmark |
| **BCD-F1** | **`0.7378`** | Dense Classes (B, C, D) |
| **Quadratic Weighted Kappa (QWK)** | **`0.7665`** | Ordinal Agreement |
| **Accuracy** | **`72.73%`** | Exact 4-Class Match |

#### 📈 Per-Class F1-Score Breakdown:
* **Class A (Almost Entirely Fatty):** `0.8000`
* **Class B (Scattered Fibroglandular):** `0.6667`
* **Class C (Heterogeneously Dense):** `0.7193`
* **Class D (Extremely Dense):** `0.7674`

---

### 💡 Architecture & Ensembling
* **E3 Model (50% weight):** DenseNet-121 @ 512x512 with Bilateral Gated Relational Fusion + Neighbor Penalty.
* **E7 Model (50% weight):** ConvNeXt-Tiny @ 1024x1024 with Bilateral Fusion + Safe Horizontal Flip TTA.
* **Formula:** `P_final = 0.50 * P_E3 + 0.50 * P_E7`

---

### 🚀 Quickstart (Inference)
```bash
python3 inference.py --config config/config.yaml --output-dir outputs/inference_results
```
