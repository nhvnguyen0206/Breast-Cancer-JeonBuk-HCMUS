# A36 view-token attention common first-10 review

Both fixed stress-screen folds reached epoch 10 normally on the master RTX
5090. Selection below uses the best DEV Macro-F1 within the identical first
10 epochs for each fold.

| Fold | Best epoch | Macro-F1 | Accuracy | F1 A/B/C/D | QWK |
|---|---:|---:|---:|---|---:|
| 1 | 6 | 0.562825 | 0.841191 | 0.0000 / 0.7222 / 0.9020 / 0.6271 | 0.687210 |
| 3 | 8 | 0.726706 | 0.849010 | 0.6667 / 0.7089 / 0.9038 / 0.6275 | 0.683353 |

Two-fold mean is 0.644766, sample SD 0.115881 and minimum 0.562825. Compared
at the same first-10 horizon, A36 is above A35 on both folds (A35: 0.559404
and 0.662866), especially fold 3, but fold 1 remains the limiting fold and
still has F1_A=0. This does not meet the expansion gates.

Continue unchanged to the common epoch-20 checkpoint. Do not expand to folds
0/2/4 and do not interpret the one/two class-A DEV cases as stable evidence.

