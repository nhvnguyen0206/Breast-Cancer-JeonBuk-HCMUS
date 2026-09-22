# A42 final audited CV5 — stability gate failed

All five runs completed50 and the combined CV5 audit PASS, including
identical learning configuration, frozen assignment/manifests, complete DEV
coverage, saved predictions, checkpoint selection and finished W&B runs.
Raw audit: `vindr_a42_cv5_audit_20260922.json` contains per-class metrics,
confusion matrices and source-run links. Audit reconstructs metrics from
saved predictions; it does not rerun image inference from checkpoints.

| Fold | Best epoch | Selected DEV Macro-F1 |
|---:|---:|---:|
| 0 | 4 | .824370 |
| 1 | 19 | .761529 |
| 2 | 25 | .677315 |
| 3 | 7 | .738565 |
| 4 | 6 | .794524 |

Mean Macro-F1 .7592604420; sample SD .0561944716; minimum .6773145015.
Accuracy mean .8408434268; QWK mean .6552521266.
Mean class F1 A/B/C/D: .866667/.688419/.897765/.584192.
Mean B/C/D F1 .7234583671; epoch50 Macro-F1 mean .5202417755.
Mean and minimum gates pass, but SD exceeds .05. A42 is rejected as the
final stable solution. Six A exams and DEV checkpoint selection limit claims
of generalization. This is one model per fold, not an inference ensemble.

Audited W&B summary published and synced:
https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/8niae7gz
The summary explicitly records target_met_single_seed=false, thresholds
.70/.05/.65 and independent_test=false.

A43 remains pending final50 and CV5 audit. Its first40 mean/SD/min are
.7392163/.0935366/.5850244; no architecture acceptance yet.
