# A45 fold1: matched first40

Job 1053_1 remains RUNNING on the master RTX5090. Its history contains
complete epochs 1--40 with finite losses. Selection is best DEV Macro-F1
within the identical first-40-epoch horizon on frozen fold1/cache/seed42.

| Arm | Selected epoch | Macro-F1 | Accuracy | QWK | B/C/D mean F1 | A-positive epochs |
|---|---:|---:|---:|---:|---:|---:|
| A43 | 4 | .5850244052 | .8114143921 | .6936709874 | .7133658737 | 1/40 |
| A44 | 19 | .7641791946 | .8337468983 | .5916055358 | .6855722594 | 1/40 |
| A45 | 20 | .5572461406 | .8486352357 | .6671180382 | .7429948541 | 0/40 |

A45 selected F1 A/B/C/D remains
[0,.7441860465,.9041533546,.5806451613], with confusion matrix
[[0,1,0,0],[0,32,7,0],[0,14,283,15],[0,0,24,27]].

The selected checkpoint is unchanged from first20. A45 retains the strongest
B/C/D mean of the three arms, but has no positive-A epoch and no epoch with
Macro-F1 >= .72. It therefore passes only the common-class preservation gate
and fails the Macro-F1/QWK gates.

At epoch40 A45 Macro-F1 is .5167716, accuracy .8362283, QWK .5930912 and
F1 A/B/C/D [0,.6133333,.8995363,.5542169]. This is close to A44's epoch40
behavior and does not indicate late generalization improvement despite the
continued decrease in training loss. View auxiliary loss is .0025349 at
epoch40; total AMP skipped updates are 18 and all losses remain finite.

Finish the preregistered 50 epochs unchanged, then run the read-only audit and
apply all gates. Do not expand or tune on fold1. These are DEV selection
results, not independent test estimates.

W&B: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/1k59zmph
