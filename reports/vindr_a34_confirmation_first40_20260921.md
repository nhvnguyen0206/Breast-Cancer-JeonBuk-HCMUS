# A34 common first-40 CV5 review

Confirmation job 998 tasks 1–4 remain RUNNING on permitted RTX 5090 nodes;
worker2/Vesta is excluded and there are no restarts/requeues. Actual completed
epochs are [50, 40, 40, 42, 42], with fold 0 retained from job 997. Selection
below is restricted to the common first 40 epochs and is selected DEV, not
independent evaluation.

| Fold | Selected epoch | Macro-F1 | Accuracy | QWK | F1 A/B/C/D |
|---|---:|---:|---:|---:|---:|
| 0 | 33 | 0.777913 | 0.839109 | 0.613854 | 1.000000 / 0.589744 / 0.899687 / 0.622222 |
| 1 | 4 | 0.729744 | 0.851117 | 0.690563 | 0.666667 / 0.707317 / 0.904992 / 0.640000 |
| 2 | 35 | 0.658355 | 0.831266 | 0.565168 | 0.666667 / 0.626866 / 0.898331 / 0.441558 |
| 3 | 8 | 0.616801 | 0.816832 | 0.616708 | 0.400000 / 0.656716 / 0.887122 / 0.523364 |
| 4 | 18 | 0.551079 | 0.846154 | 0.656351 | 0.000000 / 0.647059 / 0.902711 / 0.654545 |

Provisional mean Macro-F1 is **0.666778426**, sample SD **0.089820172**, and
minimum **0.551078900**. Mean accuracy is 0.836895315 and mean QWK is
0.628528840. Mean class F1 A/B/C/D is
0.546667/0.645540/0.898569/0.576338.

Fold 4 remains worst and fold 3 second-worst. Fold 2 improved its Macro-F1
but its selected D F1 fell to 0.441558. All three final acceptance gates are
currently unmet. Continue unchanged to epoch 50 for the registered audit.

Under the later two-weakest-fold screening revision, A34 would not expand:
historically fixed screen fold 1 reaches 0.729744, but fold 3 reaches only
0.616801, making their mean 0.673272 and violating both the two-fold mean
>=0.70 and minimum >=0.65 gates. This is a retrospective protocol diagnostic,
not a change to the already-running A34 experiment.
