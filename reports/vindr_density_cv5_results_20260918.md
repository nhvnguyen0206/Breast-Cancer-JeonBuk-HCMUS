# VinDR density-CV5: completed results

All five active runs completed 50 epochs, without early stopping, on RTX 5090.
No run used Vesta (worker-2). Folds 0/1 used master-0; folds 2/3/4 used worker-1.
The three failed initial worker attempts are excluded; only their successful
replacements are included. See [launch record](vindr_density_cv5_launch_20260918.md).

## DEV-selected checkpoints

| Fold | Selected epoch | Accuracy | Macro-F1 | QWK | Epoch-50 Macro-F1 |
|---|---:|---:|---:|---:|---:|
| 0 | 23 | 76.73% | 0.6828 | 0.6185 | 0.5387 |
| 1 | 5 | 84.37% | 0.5625 | 0.6726 | 0.5209 |
| 2 | 22 | 82.63% | 0.5790 | 0.6271 | 0.5183 |
| 3 | 20 | 85.40% | 0.5475 | 0.6557 | 0.5227 |
| 4 | 17 | 80.15% | 0.6344 | 0.5280 | 0.4924 |

Mean ± sample standard deviation across five folds:

- Accuracy: 81.86% ± 3.49 percentage points.
- Macro-F1: 0.6012 ± 0.0562.
- QWK: 0.6204 ± 0.0560.

At fixed epoch 50, mean Macro-F1 is 0.5186 ± 0.0167,
accuracy 83.24%, and QWK 0.5972.
These standard deviations are descriptive fold variability, not confidence intervals.

## Pooled selected-DEV predictions

All 2,017 studies appear exactly once in the pooled DEV predictions.
Accuracy 81.85%, Macro-F1 0.6156,
QWK 0.6217. Pooling recomputes metrics across cases;
it is not the same as averaging five per-fold metrics.

| Class | Support | Pooled F1 |
|---|---:|---:|
| A | 6 | 0.3750 |
| B | 196 | 0.6220 |
| C | 1556 | 0.8851 |
| D | 259 | 0.5801 |

Confusion matrix (true rows, predicted columns):

| True / predicted | A | B | C | D |
|---|---:|---:|---:|---:|
| A | 3 | 3 | 0 | 0 |
| B | 6 | 130 | 60 | 0 |
| C | 1 | 89 | 1375 | 91 |
| D | 0 | 0 | 116 | 143 |

## Interpretation

The best epoch precedes epoch 50 in every fold. Training longer did not yield a
higher final-epoch Macro-F1 in this campaign. Accuracy and Macro-F1 can favor
different checkpoints: fold 0 selects epoch 23 with 76.73% accuracy because
its Macro-F1 is higher, while epoch 50 has 84.41% accuracy but lower Macro-F1.

Only six A studies exist (one or two per DEV fold). Correct classification of
one A example can substantially change fold Macro-F1 and checkpoint selection.
Pooled A recall is 3/6, with 7 false-A predictions; estimates remain very unstable.
D remains difficult: 116/259 D studies are classified as C. The split balances
density proportions across folds, but it does not fix population class imbalance.

These checkpoints were selected on the same DEV folds used for these scores.
This is development cross-validation, **not independent final-test performance**.
Some studies were exposed in prior development. Do not compare these values
as a controlled improvement over the old BI-RADS-derived split.

## Verification and artifacts

- Exactly 50 sequential history entries per fold; W&B reports finished,
  completed_epochs=50 and stopped_early=false for all five active run IDs.
- Each best.pt epoch/metrics matches the maximum DEV Macro-F1 history record.
- Saved prediction probabilities are finite, sum to one, and agree with argmax.
- Prediction labels and membership match the registered per-fold DEV manifests.
- No duplicate case IDs in the pooled predictions; all 2,017 assigned studies covered.
- Metrics recomputed from prediction CSVs match checkpoint and W&B summaries.
- FP16 skipped updates per fold: 17, 15, 15, 17, 16; all runs completed.

Remote output roots:
`/slurmshared/Ngoc/runs/hcmus-density-cv5-v1-712-fold0`,
`/slurmshared/Ngoc/runs/hcmus-density-cv5-v1-712-fold1`, and
`/slurmshared/Ngoc/runs/hcmus-density-cv5-v1-717-fold{2,3,4}`.

Full aggregate metrics: [JSON](vindr_density_cv5_results_20260918.json).
No case identifiers or image data are included in this report or JSON.

