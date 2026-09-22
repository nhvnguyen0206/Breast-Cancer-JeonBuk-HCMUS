# A34 common first-10 CV5 review

Confirmation job 998 tasks 1–4 remain RUNNING on permitted RTX 5090 nodes;
worker2/Vesta is excluded and there are no restarts/requeues. Actual completed
epochs are [50, 10, 10, 10, 10], with fold 0 retained from job 997. Selection
below is restricted to the common first 10 epochs and is selected DEV, not
independent evaluation.

| Fold | Selected epoch | Macro-F1 | Accuracy | QWK | F1 A/B/C/D |
|---|---:|---:|---:|---:|---:|
| 0 | 6 | 0.629048 | 0.811881 | 0.655166 | 0.400000 / 0.595745 / 0.878939 / 0.641509 |
| 1 | 4 | 0.729744 | 0.851117 | 0.690563 | 0.666667 / 0.707317 / 0.904992 / 0.640000 |
| 2 | 10 | 0.610368 | 0.813896 | 0.615600 | 0.400000 / 0.641026 / 0.884984 / 0.515464 |
| 3 | 8 | 0.616801 | 0.816832 | 0.616708 | 0.400000 / 0.656716 / 0.887122 / 0.523364 |
| 4 | 7 | 0.526866 | 0.791563 | 0.632019 | 0.000000 / 0.629630 / 0.857143 / 0.620690 |

Provisional mean Macro-F1 is **0.622565374**, sample SD **0.072231786**, and
minimum **0.526865535**. Mean accuracy is 0.817057711 and mean QWK is
0.642011399. Mean class F1 A/B/C/D is
0.373333/0.646087/0.882636/0.588205.

At this early common horizon all three final gates are unmet. Fold 1 is
promising while fold 4 has not yet recognized its class-A cases. Continue all
tasks unchanged; next review at the common first-20 horizon.
