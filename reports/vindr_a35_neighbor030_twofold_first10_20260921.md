# A35 two-fold first-10 review

Job 1002 folds 1 and 3 remain RUNNING on permitted RTX 5090 hardware, with
worker2/Vesta excluded and no restart/requeue. Both completed ten epochs with
finite losses. This is selected DEV, not independent evaluation.

| Fold | Selected epoch | Macro-F1 | Accuracy | QWK | F1 A/B/C/D |
|---|---:|---:|---:|---:|---:|
| 1 | 2 | 0.559404 | 0.851117 | 0.675314 | 0.000000 / 0.695652 / 0.905600 / 0.636364 |
| 3 | 1 | 0.662866 | 0.826733 | 0.636655 | 0.500000 / 0.674699 / 0.888530 / 0.588235 |

The provisional two-fold mean is **0.6111349733**, sample SD 0.0731587111,
and minimum 0.5594039526. Both the mean >=0.70 and minimum >=0.65 expansion
gates are currently unmet. Fold 1 again fails to recognize its sole A case.
Continue unchanged; next review at the common first-20 horizon.

This scalar-loss control will finish as registered. Under the later goal
revision, a failure here triggers the first substantive architecture arm
rather than another sequence of small hyperparameter edits.
