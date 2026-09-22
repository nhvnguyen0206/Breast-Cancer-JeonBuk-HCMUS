# A43 multi-scale four-view Transformer — common first 40 epochs

Both job-1041 tasks remain RUNNING on worker1 RTX 5090 and completed epoch 40.
Fold 3 improves again at epoch 35; fold 2 retains epoch 7.

| Fold | Selected epoch <=40 | Macro-F1 | Accuracy | QWK | F1 A/B/C/D |
|---:|---:|---:|---:|---:|---|
| 2 | 7 | 0.799443 | 0.836228 | 0.668040 | 1.0000 / 0.7158 / 0.8925 / 0.5895 |
| 3 | 35 | 0.719963 | 0.844059 | 0.668921 | 0.6667 / 0.7027 / 0.9010 / 0.6095 |

Aggregate mean is `0.7597029`, sample SD `0.0562008`, minimum `0.7199629`,
accuracy `0.8401438`, QWK `0.6684805`, and B/C/D F1 mean `0.7351594`. Both
registered screen gates pass. B/C/D is now within `0.0040` of A41 on these
folds while A43 uniquely repairs fold-2 A, making this a substantive combined
gain rather than only a rare-A artifact.

At epoch 40 itself, Macro-F1 falls to `0.5054981/0.5367140` with A F1 zero on
both folds, so convergence remains unstable. Finish the last ten epochs and
audit both folds; do not expand before final audit.
