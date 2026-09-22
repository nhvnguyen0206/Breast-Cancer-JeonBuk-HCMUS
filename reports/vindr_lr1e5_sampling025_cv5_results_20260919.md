# O2: low LR plus mild balanced sampling, completed CV5

Fixed grouped density split seed 42, training seed 42, 50 epochs per fold.
Only sampling power changes from 0 to 0.25 relative to O1 (LR 1e-5).
Architecture and single-model inference are unchanged; no ensemble.

| Fold | Selected epoch | Macro-F1 | Accuracy | QWK |
|---|---:|---:|---:|---:|
| 0 | 6 | 0.819667 | 0.853960 | 0.696743 |
| 1 | 1 | 0.557441 | 0.836228 | 0.669179 |
| 2 | 4 | 0.546928 | 0.853598 | 0.646244 |
| 3 | 3 | 0.565851 | 0.799505 | 0.664644 |
| 4 | 2 | 0.539459 | 0.799007 | 0.648020 |

Mean Macro-F1 **0.6058691026**, sample SD **0.1199382836**.
Mean accuracy 0.8284598187; mean QWK 0.6649660571.
Mean class F1 A/B/C/D: [0.240000,0.672919,0.889779,0.620779].
Mean B/C/D F1: 0.7278254701. Epoch-50 mean Macro-F1: 0.4856450521.

Compared with O1 (0.6351955762), O2 loses 0.0293264736 Macro-F1.
It exceeds baseline (0.6012497557) by only 0.0046193469 and remains below
the best completed A1 result (0.6799754745). It fails the 0.75 CV5 target;
do not advance this arm to multi-seed confirmation.

Pooled descriptive confusion matrix, rows true A/B/C/D:

```
   2   4    0   0
   8 144   44   0
   0  86 1357 113
   0   0   91 168
```

Only 2/6 A cases are recognized; 8 B cases are predicted as A. Fold-0
success does not generalize across folds. Pooled Macro-F1 0.6081024029 is
descriptive only, not the protocol's mean-fold metric or an ensemble score.

All five runs finished 50 epochs on RTX 5090, excluding Vesta. Final task
749_4 completed exit 0 after 1h04m53s on worker-1. Full read-only audit
passed checkpoint/history selection, configuration consistency, frozen
assignment hash, FIT/DEV manifests, unique prediction IDs and labels,
finite normalized probabilities/argmax, recomputed metrics, and finished
W&B runs. DEV union is exactly 2,017 cases with support [6,196,1556,259].
Machine-readable evidence is in the adjacent JSON report.

Checkpoints were selected on DEV; this is not independent-test evidence.
Only seed 42 was evaluated, and the six A cases limit stability claims.

Verified finished W&B summary (fold table and audit artifact included):
https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/x7sraegv
