# A47 folds2/3 final audit: rejected before CV5 expansion

Both job1061 tasks completed all 50 epochs on `slurm-b20a-master-0` RTX5090.
Separate read-only local audits PASS for fold2 and fold3, verifying the frozen
five-fold manifests and assignment SHA256, v14 architecture/provenance,
complete histories, selected checkpoints, saved predictions, probability
normalization and recomputed metrics. Training logs independently show both
W&B runs completed 50 epochs and finished syncing; the local auditor did not
call the external W&B API.

| Fold | Best epoch | Macro-F1 | Accuracy | QWK | F1 A/B/C/D | B/C/D mean |
|---:|---:|---:|---:|---:|---|---:|
| 2 | 3 | .653592 | .823821 | .644387 | .5/.636364/.888530/.589474 | .704789 |
| 3 | 5 | .702931 | .846535 | .644497 | .666667/.692308/.905132/.547619 | .715020 |

Two-fold selected Macro-F1 mean/sample-SD/minimum are
`.6782616/.0348884/.6535918`. B/C/D mean/minimum are
`.7099044/.7047891`; QWK mean/minimum are `.6444421/.6443867`.

Registered gate results:

- each fold Macro-F1 >= .72: FAIL on both folds;
- two-fold Macro sample SD <= .03: FAIL;
- B/C/D mean >= .7216976: FAIL; minimum >= .6808638: PASS;
- QWK mean >= .6572337: FAIL; minimum >= .6050383: PASS.

Fold2 has one positive-A epoch (epoch3), longest streak one. Fold3 has five
positive-A epochs (1,2,3,5,13), longest streak three. Neither fold has any
epoch with Macro-F1 >= .72. At epoch50 Macro-F1 is .5123024/.5284322 with A
F1 zero on both. Total AMP skipped updates are 18 per fold; all recorded losses
are finite. Maximum probability-sum errors are 1.324e-7 and 1.445e-7.

The dual-endpoint head improves early fold2 D F1 and reduces the two-fold
spread relative to A42, but lowers mean/minimum Macro-F1 and mean B/C/D/QWK.
A47 is rejected and folds0/1/4 must not be launched. These are selected DEV
results, not independent evaluation.

W&B:

- fold2: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/109017w9
- fold3: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/zja66x7p
