# A36 view-token attention common first-40 review

Both fixed stress folds reached epoch 40 normally on permitted RTX 5090
devices. Selection uses each fold's best DEV Macro-F1 inside the common
first-40 window.

| Fold | Best epoch | Macro-F1 | Accuracy | F1 A/B/C/D | QWK |
|---|---:|---:|---:|---|---:|
| 1 | 21 | 0.563194 | 0.863524 | 0.0000 / 0.6377 / 0.9151 / 0.7000 | 0.680339 |
| 3 | 35 | 0.739842 | 0.868812 | 0.6667 / 0.7368 / 0.9185 / 0.6374 | 0.703911 |

The two-fold mean is 0.651518, sample SD 0.124909 and minimum 0.563194.
A36 improves fold 3 substantially but fold 1 remains effectively unchanged
and still has F1_A=0. It therefore fails both registered expansion gates and
must not run folds 0/2/4.

Continue unchanged through epoch 50 for final checkpoint/prediction/W&B
audits. If the final result still fails, release the GPUs and run the already
preregistered A37 spatial-token real-cache preflight before any new launch.

