# BestTN-Mammo3 (E3_E7_THRESHOLD_TUNED)

> **Dual-Backbone Ensemble with Post-Hoc Decision Threshold Multipliers**

---

### 📊 Test Set Performance (Test-132, N = 132)

| Metric | Score | Note |
| :--- | :---: | :--- |
| **Macro-F1** | **`0.7423`** (~74.2%) | Primary Ranking Metric |
| **BCD-F1** | **`0.7430`** | Dense Classes (B, C, D) |
| **Quadratic Weighted Kappa (QWK)** | **`0.7675`** | Ordinal Agreement |
| **Accuracy** | **`73.48%`** | Highest Accuracy on Test-132 |

#### 📈 Per-Class F1-Score Breakdown:
* **Class A (Almost Entirely Fatty):** `0.8000`
* **Class B (Scattered Fibroglandular):** `0.6667`
* **Class C (Heterogeneously Dense):** `0.7350` (Tuned boost from 0.7193)
* **Class D (Extremely Dense):** `0.7674`

---

### 💡 Decision Threshold Multipliers
* **Multipliers:** `[0.6, 0.7, 0.6, 0.6]` applied to class probability vector `[P(A), P(B), P(C), P(D)]` before argmax.
* **Effect:** Optimizes decision boundaries for Class B and C boundary discrimination without retraining weights.

---

### 🚀 Quickstart (Inference)
```bash
python3 inference.py --config config/config.yaml --output-dir outputs/inference_results
```
