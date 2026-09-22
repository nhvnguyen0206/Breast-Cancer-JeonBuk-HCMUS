# A45 fold1: matched first20

Job 1053_1 remains RUNNING on the master RTX5090. Its history contains
complete epochs 1--20 with finite losses. Selection below is independently
best DEV Macro-F1 within the same first-20-epoch horizon on frozen fold1,
cache and seed42.

| Arm | Selected epoch | Macro-F1 | Accuracy | QWK | B/C/D mean F1 | A-positive epochs |
|---|---:|---:|---:|---:|---:|---:|
| A43 | 4 | .5850244052 | .8114143921 | .6936709874 | .7133658737 | 1/20 |
| A44 | 19 | .7641791946 | .8337468983 | .5916055358 | .6855722594 | 1/20 |
| A45 | 20 | .5572461406 | .8486352357 | .6671180382 | .7429948541 | 0/20 |

A45 selected F1 A/B/C/D is
[0,.7441860465,.9041533546,.5806451613]. Its confusion matrix, true rows and
predicted columns A/B/C/D, is
[[0,1,0,0],[0,32,7,0],[0,14,283,15],[0,0,24,27]].

A45 has the strongest common-class mean of these three arms at this horizon.
Relative to A44 it raises B/C/D mean by .0574226 and QWK by .0755125 while
avoiding severe errors, but lacks A44's one-epoch rare-A recovery and
therefore trails its selected Macro-F1. Relative to A43, A45 raises B/C/D
mean by .0296290 and accuracy by .0372208, while Macro-F1 is .0277783 lower
and QWK .0265530 lower.

The training-only view auxiliary loss is .0062985 at epoch20 and all training
losses remain finite. Total AMP skipped updates are 12. No epoch has positive
A F1 or Macro-F1 >= .72. At this horizon A45 passes only the B/C/D gate and
fails the Macro-F1/QWK gates.

The selected epoch is the horizon boundary, so continue the preregistered
training unchanged. Do not expand or tune on fold1. Next scheduled comparison
is epoch40, followed by completed50 audit and gate decision. These remain DEV
selection results, not an independent test estimate.

W&B: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/1k59zmph
