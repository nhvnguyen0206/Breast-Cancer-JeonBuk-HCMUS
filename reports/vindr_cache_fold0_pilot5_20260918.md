# VinDR frozen-cache pilot — 2026-09-18

## Scope and reproducibility

- Architecture unchanged: shared DenseNet121, ipsilateral and bilateral relational
  fusion, flat/CORAL/binary heads; inference uses the flat head only.
- Initialized from torchvision ImageNet DenseNet121 weights, not a TN-Mammo-trained
  checkpoint. This is training on VinDR FIT and selecting on VinDR DEV, **not**
  external testing of a TN-Mammo-trained model.
- Config: `configs/vindr_cache.yaml`; seed 42, five epochs, batch size 2,
  512×512 input, AdamW, initial LR 0.00005, cosine decay, CUDA FP16 AMP.
- Cache: `/home/tyler/datasets/VinDR_dicom_window16_cvatmask_v1`.
  Float32 values used directly; explicit packed mask validated; no repeated
  DICOM windowing, CLAHE, foreground crop or division by 65535.
- Labels: original VinDR `breast-level_annotations.csv`, `breast_density` field.
- Registered split: `inner_fold0_seed42.json` from
  `/home/tyler/Ngoc/BRM/LAS-GAM-Clone/datasets/onpe_coug/v1/nested5/`.
  This is the existing campaign split, not an assertion of the original VinDR
  train/test protocol or an independent patient-ID audit.
- Local manifests and source hashes: `data/vindr_cache_fold0/audit.json`.
- Local artifacts: `outputs/vindr_cache_fold0_pilot5_seed42_20260918/`:
  `best.pt`, `history.json`, `valid_predictions.csv`, and `dev_recheck/`.
  Data manifests, predictions and model weights are Git-ignored.

## Population

The cache contains 8,164 images in 2,048 studies, not the full VinDR population.
Excluded 14 studies without exactly four required views and 17 with inconsistent
density labels across views. No labels were reconciled or inferred from masks.

| Partition | A | B | C | D | Total |
|---|---:|---:|---:|---:|---:|
| FIT | 2 | 92 | 817 | 124 | 1,035 |
| DEV | 0 | 32 | 251 | 41 | 324 |
| CAL — unused | 1 | 27 | 188 | 38 | 254 |
| OUTER — unused | 3 | 45 | 300 | 56 | 404 |

Both breasts of every included study remain in the same registered partition.
The cache itself was not modified or rebuilt.

## DEV results

Checkpoint selection uses four-class Macro-F1, including zero for absent class A.

| Epoch | Train loss | Accuracy | Macro-F1 (A–D) | QWK |
|---|---:|---:|---:|---:|
| 1 | 0.9522 | 0.8117 | 0.4358 | 0.4455 |
| **2 — selected** | **0.8499** | **0.8642** | **0.5499** | **0.6447** |
| 3 | 0.7616 | 0.8457 | 0.5356 | 0.6393 |
| 4 | 0.6692 | 0.8364 | 0.5393 | 0.6362 |
| 5 | 0.5971 | 0.8333 | 0.5395 | 0.6388 |

Selected checkpoint per-class F1: A **not estimable** (reported numerically as
0 by the metric), B 0.6071, C 0.9160, D 0.6765. Descriptive B/C/D-only Macro-F1
is 0.7332; this is not the four-class selection metric.

Confusion matrix, rows = true labels, columns = predictions:

| True / predicted | A | B | C | D |
|---|---:|---:|---:|---:|
| A | 0 | 0 | 0 | 0 |
| B | 0 | 17 | 15 | 0 |
| C | 0 | 7 | 240 | 4 |
| D | 0 | 0 | 18 | 23 |

Always predicting C gives accuracy 0.7747, four-class Macro-F1 0.2183, QWK 0.
The selected model exceeds this baseline. All 44 errors are adjacent-class
errors, but the absence of A limits interpretation of severe-error performance.

## Interpretation and checks

- B recall is 17/32 (53.1%); D recall is 23/41 (56.1%). The main remaining
  failure is confusing B/D with C, not total collapse to the majority class.
- FIT has only two A studies and DEV has none. This experiment cannot establish
  useful A-class performance or general four-class clinical performance.
- Train loss continues falling after epoch 2 while DEV Macro-F1 does not improve.
  This short run does not prove convergence or overfitting; longer training is
  not guaranteed to improve validation performance.
- Five local unit/integration tests passed, including cache scale/mask checks,
  split/label preparation, model backward/512px forward, and checkpoint inference.
- Reloading the selected checkpoint through the inference CLI reproduced all
  324 predicted labels and the same DEV metrics.
- One real FIT tensor was compared to its uint16 PNG / 65535 and matched exactly;
  this parity test is not an exhaustive PNG audit. Every loaded FIT/DEV tensor
  is checked for dtype, range, mask shape and zero background.
- Initial FP16 scale overflow caused the first launch to stop before a completed
  epoch. The restarted run lets GradScaler skip overflowing updates and reduce
  scale: four skipped updates in epoch 1, zero in epochs 2–5. No architecture or
  loss change was made for this recovery.
- CAL and OUTER were not evaluated. These are DEV-selected pilot scores, not
  final held-out test results; do not compare them directly to old ensemble scores.
