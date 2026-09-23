# A53 folds2/3: matched first20

Array job1096 remains active on RTX5090 with worker2/Vesta excluded. Both runs
use the immutable v20 snapshot, frozen split/cache/seed42 and offline W&B
receipts `6irwuqqa`/`82som6u1`. This selected-DEV interim analysis is not an
independent test or final gate decision.

| Run | Selected epoch | Macro-F1 | Accuracy | QWK | F1 A/B/C/D | B/C/D mean | A-positive epochs | Longest A streak | Epochs Macro >= .72 |
|---|---:|---:|---:|---:|---|---:|---:|---:|---:|
| A53/f2 | 19 | .556355 | .856079 | .658714 | .000000/.736842/.910798/.577778 | .741806 | 0/20 | 0 | 0 |
| A53/f3 | 16 | .720535 | .836634 | .676824 | .666667/.747253/.893964/.574257 | .738491 | 9/20 | 7 | 1 |

Selected aggregate Macro-F1 is mean `.6384449`, sample SD `.1160933`, and
minimum `.5563545`; mean accuracy is `.8463565`, mean QWK `.6677687`, and mean
B/C/D `.7401487` with minimum `.7384914`.

Relative to first10, fold2 gains only `.0121879` Macro-F1 and still has no
positive-A epoch. Fold3 improves by `.0462486`, reaches the `.72` boundary once
and develops a seven-epoch positive-A streak. B/C/D mean/minimum and QWK
mean/minimum now pass their registered gates, isolating the failure to fold2's
A decision region: fold2 Macro-F1 and the resulting cross-fold SD still fail.

The result does not support a general representation collapse. It supports a
more specific mechanism: A53's multiscale representation is supervised only
through the A-vs-rest gate, whereas A43 trained the same representation to
separate B/C/D and solve ordinal/binary tasks as well. Continue A53 unchanged
to epoch40/50 and queued read-only audits1098/1099. Folds0/1/4 remain locked.

