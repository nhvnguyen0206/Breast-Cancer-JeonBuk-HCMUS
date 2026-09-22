# A43 final audited CV5: rejected for instability

All five runs completed50 and combined CV5 audit PASS. Raw evidence in
`vindr_a43_cv5_audit_20260922.json` includes confusion matrices, per-class
metrics, assignment hash and finished W&B run links. This checks saved
predictions against histories/checkpoint metrics, not fresh image inference.

| Fold | Selected epoch | DEV Macro-F1 |
|---:|---:|---:|
| 0 | 6 | .816001 |
| 1 | 4 | .585024 |
| 2 | 7 | .799443 |
| 3 | 35 | .719963 |
| 4 | 35 | .775651 |

Mean .7392162928; sample SD .0935365942; minimum .5850244052.
Mean accuracy .8269550156, QWK .6668580236; mean class F1 A/B/C/D
.773333/.683503/.887969/.612059. B/C/D mean .7278439459.
Epoch50 mean Macro-F1 .5216278507; A F1 zero in all five final epochs.
Weakest folds are1 and3. Frozen grouped split contains2017 cases with
support [6,196,1556,259]. These are selected DEV scores, not independent
test estimates; rare-A generalization remains unproven.

Active thresholds updated by user: mean>=.72, sample SD<=.03; retain
minimum>=.65. A43 passes mean only and is rejected. A42 likewise remains
rejected under the new thresholds; its earlier W&B summary retains the
historical .70/.05 registration, and is not evidence of current success.

W&B summary published with NEW thresholds and synced:
https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/bfcspx52

A44 local/global fusion is preregistered in
`vindr_a44_local_global_fusion_preregistration_20260922.md`, with one-fold
screen on fold1 before expansion per the latest goal. Implementation,
tests, real-cache preflight and launch remain to be done.
