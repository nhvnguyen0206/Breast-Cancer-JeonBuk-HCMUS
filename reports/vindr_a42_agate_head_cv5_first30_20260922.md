# A42 A-gate CV5 — common first 30 epochs

Expansion job `1043` remains RUNNING on RTX 5090. At the common first-30
horizon, fold 2 improves at epoch 25 while the other selected checkpoints are
unchanged.

| Fold | Selected epoch <=30 | Macro-F1 | Accuracy | QWK | F1 A/B/C/D |
|---:|---:|---:|---:|---:|---|
| 0 | 4 | 0.824370 | 0.849010 | 0.712318 | 1.0000 / 0.7048 / 0.8988 / 0.6939 |
| 1 | 19 | 0.761529 | 0.851117 | 0.587921 | 1.0000 / 0.5862 / 0.9099 / 0.5500 |
| 2 | 25 | 0.677315 | 0.823821 | 0.605038 | 0.6667 / 0.6585 / 0.8899 / 0.4941 |
| 3 | 7 | 0.738565 | 0.851485 | 0.709429 | 0.6667 / 0.7579 / 0.9034 / 0.6263 |
| 4 | 6 | 0.794524 | 0.828784 | 0.661555 | 1.0000 / 0.7347 / 0.8867 / 0.5567 |

CV5 mean is `0.7592604`, sample SD `0.0561945`, minimum `0.6773145`, mean
accuracy `0.8408434`, mean QWK `0.6552521`, and B/C/D F1 mean `0.7234584`.
Mean and minimum gates pass; SD is only `0.0061945` above the final threshold.

Fold 2 now meets the minimum gate and reduces the principal stability failure,
but D F1 `0.4941` and QWK `0.6050` remain weak. This is the closest arm so far
to satisfying all registered CV5 gates, yet it is not accepted before full50
and five audits. Continue unchanged without post-hoc threshold tuning.
