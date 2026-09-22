# A32 common first-10 CV5 review

Array job 988 tasks 1–4 remained RUNNING on permitted RTX 5090 nodes. Actual
epochs were [50, 10, 10, 11, 11], with fold 0 retained from job 987. All
reported training losses are finite. Selection below is restricted to the
common first ten epochs and is selected DEV, not independent evaluation.

| Fold | Selected epoch | Macro-F1 | Accuracy | QWK | F1 A/B/C/D |
|---|---:|---:|---:|---:|---:|
| 0 | 4 | 0.777172 | 0.787129 | 0.633969 | 1.000000 / 0.607143 / 0.851138 / 0.650407 |
| 1 | 5 | 0.556669 | 0.838710 | 0.670300 | 0.000000 / 0.717391 / 0.895425 / 0.613861 |
| 2 | 7 | 0.564567 | 0.828784 | 0.647142 | 0.222222 / 0.571429 / 0.902821 / 0.561798 |
| 3 | 9 | 0.690298 | 0.799505 | 0.630287 | 0.666667 / 0.701031 / 0.866221 / 0.527273 |
| 4 | 9 | 0.624800 | 0.799007 | 0.592294 | 0.500000 / 0.607595 / 0.872375 / 0.519231 |

Provisional mean Macro-F1 is **0.6427013333**, sample SD **0.0924318836**,
and minimum **0.5566693818**. Mean accuracy is 0.8106269808 and mean QWK is
0.6347982713. Mean class F1 A/B/C/D is
0.477778/0.640918/0.877596/0.574514.

All three acceptance gates currently fail. Fold 0 is not representative of
the confirmation folds, and rare-A sensitivity remains pronounced. This is
an incomplete horizon, so continue all tasks unchanged to the common
first-20 review; do not accept or stop based on first ten epochs.
