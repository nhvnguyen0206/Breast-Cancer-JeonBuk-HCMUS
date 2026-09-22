# A34 common first-20 CV5 review

Confirmation job 998 tasks 1–4 remain RUNNING on permitted RTX 5090 nodes;
worker2/Vesta is excluded and there are no restarts/requeues. Actual completed
epochs are [50, 20, 20, 21, 21], with fold 0 retained from job 997. Selection
below is restricted to the common first 20 epochs and is selected DEV, not
independent evaluation.

| Fold | Selected epoch | Macro-F1 | Accuracy | QWK | F1 A/B/C/D |
|---|---:|---:|---:|---:|---:|
| 0 | 6 | 0.629048 | 0.811881 | 0.655166 | 0.400000 / 0.595745 / 0.878939 / 0.641509 |
| 1 | 4 | 0.729744 | 0.851117 | 0.690563 | 0.666667 / 0.707317 / 0.904992 / 0.640000 |
| 2 | 16 | 0.639288 | 0.853598 | 0.640334 | 0.400000 / 0.666667 / 0.912173 / 0.578313 |
| 3 | 8 | 0.616801 | 0.816832 | 0.616708 | 0.400000 / 0.656716 / 0.887122 / 0.523364 |
| 4 | 18 | 0.551079 | 0.846154 | 0.656351 | 0.000000 / 0.647059 / 0.902711 / 0.654545 |

Provisional mean Macro-F1 is **0.633191993**, sample SD **0.064007498**, and
minimum **0.551078900**. Mean accuracy is 0.835916272 and mean QWK is
0.651824612. Mean class F1 A/B/C/D is
0.373333/0.654701/0.897187/0.607547.

Fold 4 remains the current worst fold because its only A case is never
recognized during epochs 1–20; its B/C/D mean at the selected checkpoint is
0.734772. Fold 3 is next-worst and combines unstable A recognition with low
D F1. Continue all tasks unchanged to the common first-40 horizon.
