# A42 expansion partial audit

On 2026-09-22, read-only audits from the immutable A42 snapshot PASS for
completed50 folds 0 and 2. Frozen manifests, assignment hash, selected
checkpoint epoch, metrics recomputed from saved predictions and finished
W&B summaries all match. Image inference was not rerun by this audit.

| Fold | Selected epoch | Selected DEV Macro-F1 | Epoch50 Macro-F1 | W&B ID |
|---:|---:|---:|---:|---|
| 0 | 4 | 0.8243696484 | 0.5035518381 | k5fx8np4 |
| 2 | 25 | 0.6773145015 | 0.5331754062 | dla18fu9 |

Selected fold0 accuracy/QWK: .849010/.712318; F1 A/B/C/D:
1.000000/.704762/.898839/.693878. Selected fold2 accuracy/QWK:
.823821/.605038; F1 A/B/C/D: .666667/.658537/.889937/.494118.
Both have A F1 zero at epoch50. Best-checkpoint DEV scores do not establish
sustained training stability or independent test performance.

Latest scheduler check: job1043 fold4 is RUNNING at43 epochs; job1046
folds0/1/4 are RUNNING at35, all on worker1 RTX5090. Final CV5 is pending.
Local CV5 audit now recognizes architectures v7--v10, matching the per-fold
auditor. Syntax compilation and whitespace checks pass; end-to-end CV5
verification remains pending. Immutable training snapshots are unchanged.
