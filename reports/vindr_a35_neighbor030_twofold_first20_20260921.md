# A35 two-fold first-20 review

Job 1002 folds 1 and 3 remain RUNNING on permitted RTX 5090 hardware, with
worker2/Vesta excluded and no restart/requeue. Both completed twenty epochs
with finite losses. This is selected DEV, not independent evaluation.

| Fold | Selected epoch | Macro-F1 | Accuracy | QWK | F1 A/B/C/D |
|---|---:|---:|---:|---:|---:|
| 1 | 2 | 0.559404 | 0.851117 | 0.675314 | 0.000000 / 0.695652 / 0.905600 / 0.636364 |
| 3 | 14 | 0.668136 | 0.836634 | 0.655531 | 0.500000 / 0.720000 / 0.898089 / 0.554455 |

The provisional two-fold mean is **0.6137700535**, sample SD 0.0768852772,
and minimum 0.5594039526. Both expansion gates remain unmet. Fold 1 has not
improved after epoch 2 and still has F1_A zero; fold 3 improved modestly but
remains below the 0.70 mean requirement when paired with fold 1.

Continue unchanged to the common first-40 horizon. A36 attention-fusion code
may be prepared and tested in parallel, but no A36 training is authorized
before A35 completes and is audited.
