# A44 fold1 final audit: rejected before CV5 expansion

Job `1050_1` completed all 50 epochs on master RTX 5090. The read-only audit
PASS verifies the frozen five-fold manifests and assignment SHA256, complete
history, selected checkpoint, saved predictions, probability normalization,
and finished W&B run.

| Metric | Selected epoch 19 | Epoch 50 | Registered screen gate |
|---|---:|---:|---:|
| Macro-F1 | 0.764179 | 0.525676 | >= 0.72 |
| Accuracy | 0.833747 | 0.836228 | reported |
| QWK | 0.591606 | 0.606212 | >= 0.693671 |
| B/C/D F1 mean | 0.685572 | 0.700901 | >= 0.713366 |
| A F1 | 1.000000 | 0.000000 | diagnostic only |

Selected F1 A/B/C/D is `1.000000 / 0.612903 / 0.896445 / 0.547368`.
Selected confusion matrix, true rows and predicted columns A/B/C/D:
`[[1,0,0,0],[0,19,20,0],[0,4,290,18],[0,0,25,26]]`.
Only one of 50 epochs has Macro-F1 >= 0.75 and only one epoch has positive
A F1. Total AMP skipped updates are 19; all recorded losses are finite.

A44 passes the primary Macro-F1 threshold at one DEV-selected checkpoint but
fails both preregistered common-class/QWK preservation gates. The gain is
dominated by the single class-A DEV case and is not persistent. A44 is
therefore rejected and must not expand to the remaining folds. These are DEV
selection results, not an independent test estimate.

W&B: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/2031sdoy

The next structural hypothesis may retain local/global fusion but add
training-only per-view density supervision so each local summary is directly
constrained before exam-level fusion. This requires a new preregistration and
must be screened again on fold1; A44 results do not authorize CV5 expansion.
