# A35 two-fold first-40 review

Job 1002 folds 1 and 3 remain RUNNING on permitted RTX 5090 hardware, with
worker2/Vesta excluded and no restart/requeue. Both completed forty epochs
with finite losses. This is selected DEV, not independent evaluation.

| Fold | Selected epoch | Macro-F1 | Accuracy | QWK | F1 A/B/C/D |
|---|---:|---:|---:|---:|---:|
| 1 | 2 | 0.559404 | 0.851117 | 0.675314 | 0.000000 / 0.695652 / 0.905600 / 0.636364 |
| 3 | 21 | 0.704229 | 0.834158 | 0.641540 | 0.666667 / 0.734177 / 0.895238 / 0.520833 |

The provisional two-fold mean is **0.6318163901**, sample SD 0.1024066512,
and minimum 0.5594039526. Fold 3 now exceeds 0.70, but fold 1 remains
unchanged since epoch 2 with F1_A zero. Both registered expansion gates fail.

Continue unchanged to epoch 50 for audit. Do not expand A35. After the final
audit, proceed to the already-prepared A36 view-token attention architecture.
