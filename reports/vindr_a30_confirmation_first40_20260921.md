# A30 common first40-epoch review

Array 982 tasks 1–4 remained RUNNING on permitted RTX 5090 nodes; actual
epochs were [50, 40, 40, 42, 42]. Evidence is the remote `history.json` for
each fold, including the original job 981 for fold 0. Selection below is
restricted to the common first 40 epochs. These are selected DEV results,
not an independent evaluation and not the final audit.

| Fold | Selected epoch | Macro-F1 | Accuracy | QWK | A F1 |
|---|---:|---:|---:|---:|---:|
| 0 | 11 | 0.7025951909 | 0.8391089109 | 0.6494927923 | 0.6666666667 |
| 1 | 20 | 0.7584943371 | 0.8312655087 | 0.5920688321 | 1.0000000000 |
| 2 | 27 | 0.6402752997 | 0.8238213400 | 0.6223055295 | 0.5000000000 |
| 3 | 2 | 0.6864294858 | 0.8514851485 | 0.6698490116 | 0.5000000000 |
| 4 | 37 | 0.7564616179 | 0.8163771712 | 0.5887641689 | 1.0000000000 |

Mean Macro-F1 is **0.7088511863**, sample SD is **0.0499392580**, and the
minimum fold score is **0.6402752997**. The mean threshold (>= 0.70) and SD
threshold (<= 0.05) pass at this checkpoint. The minimum-fold threshold
(>= 0.65) does not pass. The four-class per-fold values remain sensitive to
the six-case class A, so this checkpoint is not a success claim.

Continue the same immutable A30 run through epoch 50. Do not submit a new
arm before the completed run is audited and the final five-fold summary is
published.
