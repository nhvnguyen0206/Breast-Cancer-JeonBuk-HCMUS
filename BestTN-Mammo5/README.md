# BestTN-Mammo5 (E3_E7_E9_TRIPLE_BLEND)

> **Triple-Model Probability Blend (DenseNet-512 + ConvNeXt-1024 + ConvNeXt-E9 CORAL)**

---

### 📊 Test Set Performance (Test-132, N = 132)

| Metric | Score | Note |
| :--- | :---: | :--- |
| **Macro-F1** | **`0.7375`** (~73.8%) | Primary Ranking Metric |
| **BCD-F1** | **`0.7370`** | Dense Classes (B, C, D) |
| **Quadratic Weighted Kappa (QWK)** | **`0.7651`** | Ordinal Agreement |
| **Accuracy** | **`72.73%`** | Exact 4-Class Match |

#### 📈 Per-Class F1-Score Breakdown:
* **Class A (Almost Entirely Fatty):** `0.8000`
* **Class B (Scattered Fibroglandular):** `0.6667`
* **Class C (Heterogeneously Dense):** `0.7193`
* **Class D (Extremely Dense):** `0.7640`

---

### 💡 Architecture & Ensembling
* **E3 Model (40% weight):** DenseNet-121 @ 512x512 with Bilateral Gated Relational Fusion.
* **E7 Model (40% weight):** ConvNeXt-Tiny @ 1024x1024 with Bilateral Fusion + Safe Horizontal Flip TTA.
* **E9 Model (20% weight):** ConvNeXt-Tiny @ 1024x1024 with Shared Mean Fusion + Auxiliary CORAL Ordinal Supervision.
* **Formula:** `P_final = 0.40 * P_E3 + 0.40 * P_E7 + 0.20 * P_E9`

---

### 🚀 Quickstart (Inference)
```bash
python3 inference.py --config config/config.yaml --output-dir outputs/inference_results
```
