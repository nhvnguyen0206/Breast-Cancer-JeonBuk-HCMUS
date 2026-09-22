# A32 completed CV5: dropout 0.45 with sampling power 0.25

A32 changes only dropout 0.40 -> 0.45 relative to A30. Fold 0 is retained
from job 987 and folds 1–4 are array job 988. All tasks completed 50 epochs
on permitted RTX 5090 nodes with exit code 0:0, no restart/requeue, and no
Vesta use. The full provenance/data/prediction/W&B audit passed; all five
source runs are `finished`, the 2,017-case union is exact, and assignment
SHA256 is unchanged.

| Fold | Best epoch | Macro-F1 |
|---|---:|---:|
| 0 | 4 | 0.7771719287 |
| 1 | 5 | 0.5566693818 |
| 2 | 7 | 0.5645674658 |
| 3 | 37 | 0.7015347952 |
| 4 | 13 | 0.7542818388 |

Selected-DEV aggregate: mean Macro-F1 **0.6708450821**, sample SD
**0.1043311692**, minimum **0.5566693818**, mean accuracy **0.8170650812**,
and mean QWK **0.6311131110**. Mean class F1 A/B/C/D is
0.577778/0.651162/0.882598/0.571843; mean B/C/D F1 is 0.701868. Epoch-50
mean Macro-F1 is 0.531456.

A32 fails the mean >=0.70, SD <=0.05, and minimum >=0.65 gates. Reject it:
dropout 0.45 worsens both mean and dispersion relative to A30. Results are
selected DEV on one seed, not independent test; only six A cases exist.

Audited W&B summary:
https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/qjxsgo3w

