# A45 fold1 final audit: rejected before CV5 expansion

Job 1053_1 completed all 50 epochs on the master RTX5090. The read-only audit
PASS verifies the frozen five-fold manifests and assignment SHA256, A45 v12
architecture/provenance, complete history, selected checkpoint, saved
predictions, probability normalization and finished W&B run.

| Metric | Selected epoch 20 | Epoch 50 | Registered screen gate |
|---|---:|---:|---:|
| Macro-F1 | .557246 | .521716 | >= .72 |
| Accuracy | .848635 | .838710 | reported |
| QWK | .667118 | .602075 | >= .693671 |
| B/C/D F1 mean | .742995 | .695622 | >= .713366 |
| A F1 | 0 | 0 | diagnostic only |

Selected F1 A/B/C/D is
[0,.7441860465,.9041533546,.5806451613]. Selected confusion matrix, true rows
and predicted columns A/B/C/D, is
[[0,1,0,0],[0,32,7,0],[0,14,283,15],[0,0,24,27]].

Across all 50 epochs, zero epochs have Macro-F1 >= .72 and zero have positive
A F1; the longest positive-A streak is zero. Total AMP skipped updates are
18 and all losses are finite. Maximum saved probability-sum error is
1.293e-7. W&B state is finished.

A45 passes the B/C/D preservation gate but fails both Macro-F1 and QWK gates.
The auxiliary per-view objective improves common-class performance relative
to A44, but does not recover the rare A decision and does not improve the
four-class screen score over A43. A45 is therefore rejected and must not
expand to the remaining folds. These are DEV-selected results, not an
independent test estimate.

W&B: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/1k59zmph

Before registering a successor, compare saved A-class probabilities and
decision margins across A43/A44/A45. The next experiment should target the
identified failure mechanism rather than merely increasing auxiliary-loss
weight.
