# A32 common first-40 CV5 review

Array job 988 tasks 1–4 remained RUNNING on permitted RTX 5090 nodes. Actual
epochs were [50, 40, 40, 42, 42], with fold 0 retained from job 987. All
reported training losses are finite. Selection is restricted to the common
first 40 epochs and is selected DEV, not independent evaluation.

| Fold | Selected epoch | Macro-F1 | Accuracy | QWK | F1 A/B/C/D |
|---|---:|---:|---:|---:|---:|
| 0 | 4 | 0.777172 | 0.787129 | 0.633969 | 1.000000 / 0.607143 / 0.851138 / 0.650407 |
| 1 | 5 | 0.556669 | 0.838710 | 0.670300 | 0.000000 / 0.717391 / 0.895425 / 0.613861 |
| 2 | 7 | 0.564567 | 0.828784 | 0.647142 | 0.222222 / 0.571429 / 0.902821 / 0.561798 |
| 3 | 37 | 0.701535 | 0.826733 | 0.633973 | 0.666667 / 0.702703 / 0.889600 / 0.547170 |
| 4 | 13 | 0.754282 | 0.803970 | 0.570183 | 1.000000 / 0.657143 / 0.874003 / 0.485981 |

Provisional mean Macro-F1 is **0.6708450821**, sample SD **0.1043311692**,
and minimum **0.5566693818**. Mean accuracy is 0.8170650812 and mean QWK is
0.6311131110. Mean class F1 A/B/C/D is
0.577778/0.651162/0.882598/0.571843.

Only fold 3 improved after the first-20 review. Mean, SD, and minimum all
remain outside their acceptance limits, with folds 1–2 still near 0.56.
Continue all tasks unchanged through epoch 50 and run the full audit before
formally rejecting A32. No acceptance claim is supported at this horizon.
