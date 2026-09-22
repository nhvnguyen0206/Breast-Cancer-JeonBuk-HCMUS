# A32 common first-20 CV5 review

Array job 988 tasks 1–4 remained RUNNING on permitted RTX 5090 nodes. Actual
epochs were [50, 20, 20, 21, 21], with fold 0 retained from job 987. All
reported training losses are finite. Selection is restricted to the common
first 20 epochs and is selected DEV, not independent evaluation.

| Fold | Selected epoch | Macro-F1 | Accuracy | QWK | F1 A/B/C/D |
|---|---:|---:|---:|---:|---:|
| 0 | 4 | 0.777172 | 0.787129 | 0.633969 | 1.000000 / 0.607143 / 0.851138 / 0.650407 |
| 1 | 5 | 0.556669 | 0.838710 | 0.670300 | 0.000000 / 0.717391 / 0.895425 / 0.613861 |
| 2 | 7 | 0.564567 | 0.828784 | 0.647142 | 0.222222 / 0.571429 / 0.902821 / 0.561798 |
| 3 | 9 | 0.690298 | 0.799505 | 0.630287 | 0.666667 / 0.701031 / 0.866221 / 0.527273 |
| 4 | 13 | 0.754282 | 0.803970 | 0.570183 | 1.000000 / 0.657143 / 0.874003 / 0.485981 |

Provisional mean Macro-F1 is **0.6685976759**, sample SD **0.1036234356**,
and minimum **0.5566693818**. Mean accuracy is 0.8116195366 and mean QWK is
0.6303760515. Mean class F1 A/B/C/D is
0.577778/0.650827/0.877922/0.567864.

Mean improved from first ten because fold 4 improved, but dispersion worsened
and folds 1–2 did not find new best checkpoints. All acceptance gates still
fail. Continue all tasks unchanged to the common first-40 review; do not
accept, stop, or alter the experiment based on this incomplete horizon.
