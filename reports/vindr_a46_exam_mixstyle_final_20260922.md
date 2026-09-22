# A46 fold1 final audit: rejected before CV5 expansion

Job 1057_1 completed all 50 epochs on `slurm-b20a-master-0` with an RTX5090.
The read-only audit PASS verifies the frozen five-fold manifests and assignment
SHA256, A46 v13 architecture/provenance, complete history, selected checkpoint,
saved predictions, probability normalization and finished W&B run.

| Metric | Selected epoch 25 | Epoch 50 | Registered screen gate |
|---|---:|---:|---:|
| Macro-F1 | .547574 | .529056 | >= .72 |
| Accuracy | .861042 | .836228 | reported |
| QWK | .658537 | .605745 | >= .693671 |
| B/C/D F1 mean | .730098 | .705408 | >= .713366 |
| A F1 | 0 | 0 | diagnostic only |

Selected F1 A/B/C/D is
`[0,.6764705882,.9185867896,.5952380952]`. Selected confusion matrix, true
rows and predicted columns A/B/C/D, is
`[[0,1,0,0],[2,23,14,0],[0,5,299,8],[0,0,26,25]]`.

Across all 50 epochs, zero epochs have Macro-F1 >= .72 and zero have positive
A F1; the longest positive-A streak is zero. Total AMP skipped updates are 21
and all losses are finite. Maximum saved probability-sum error is 1.350e-7.
W&B state is finished.

A46 passes only the selected-checkpoint B/C/D preservation gate and fails both
Macro-F1 and QWK gates. Relative to A45 it improves selected accuracy but loses
Macro-F1, QWK and B/C/D mean; MixStyle does not solve the rare-A generalization
failure. A46 is therefore rejected and must not expand to the remaining folds.
These are DEV-selected results, not an independent test estimate.

W&B: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/2rzbst10

The negative result narrows the next architectural hypothesis: style-statistic
randomization alone is insufficient. A successor should change the learned
representation or supervision target more fundamentally while retaining a
single deployable inference path, and must be separately preregistered before
another fold1 screen.
