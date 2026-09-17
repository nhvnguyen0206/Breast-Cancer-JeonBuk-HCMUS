# BestTN-Mammo1 (REGION1_ENSEMBLE)

> **6-Model Multi-Seed Ensemble (3x DenseNet-121 @ 512 + 3x ConvNeXt-Tiny @ 1024)**

---

### 📊 Test Set Performance (Test-132, N = 132)

| Metric | Score | Note |
| :--- | :---: | :--- |
| **Macro-F1** | **`0.7496`** (~75.0%) | Primary Ranking Metric |
| **BCD-F1** | **`0.7478`** | Dense Classes (B, C, D) |
| **Quadratic Weighted Kappa (QWK)** | **`0.7749`** | Ordinal Agreement |
| **Accuracy** | **`71.21%`** | Exact 4-Class Match |

#### 📈 Per-Class F1-Score Breakdown:
* **Class A (Almost Entirely Fatty):** `0.8571`
* **Class B (Scattered Fibroglandular):** `0.7273`
* **Class C (Heterogeneously Dense):** `0.6783`
* **Class D (Extremely Dense):** `0.7356`

---

### 💡 Architecture & Ensembling
* **E3 Group (10% weight):** 3 seeds (42, 43, 44) of DenseNet-121 @ 512x512 with Bilateral Contralateral Region Attention.
* **E7 Group (90% weight):** 3 seeds (42, 43, 44) of ConvNeXt-Tiny @ 1024x1024 with Bilateral Fusion.
* **Formula:** `P_final = 0.10 * mean(P_E3_seeds) + 0.90 * mean(P_E7_seeds)`

---

### 🚀 Quickstart (Inference)
```bash
python3 inference.py --config config/config.yaml --output-dir outputs/inference_results
```
