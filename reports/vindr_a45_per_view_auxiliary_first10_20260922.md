# A45 fold1: matched first10 against A43/A44

Job 1053_1 is RUNNING on the master RTX5090. Its history contains complete
epochs 1--10 with finite losses. Each arm below is independently selected by
best DEV Macro-F1 within the same first-ten-epoch horizon on the same frozen
fold1, cache and seed42.

| Arm | Selected epoch | Macro-F1 | Accuracy | QWK | B/C/D mean F1 | A-positive epochs |
|---|---:|---:|---:|---:|---:|---:|
| A43 | 4 | .5850244052 | .8114143921 | .6936709874 | .7133658737 | 1/10 |
| A44 | 4 | .5418260416 | .7965260546 | .6321601104 | .7224347221 | 0/10 |
| A45 | 4 | .5472872527 | .8089330025 | .6438008655 | .7297163369 | 0/10 |

A45 selected F1 A/B/C/D is
[0,.7123287671,.8711864407,.6056338028]. Its confusion matrix, true rows and
predicted columns A/B/C/D, is
[[0,1,0,0],[0,26,13,0],[0,7,257,48],[0,0,8,43]].

Relative to A44 at the matched horizon, A45 improves Macro-F1 by .0054612,
accuracy by .0124070, QWK by .0116408, and B/C/D mean by .0072816. The
training-only view auxiliary loss decreases from .0671709 at epoch1 to
.0104573 at epoch10, confirming optimization of the added head. These small
differences do not yet establish a generalization improvement: A45 remains
.0377372 below A43 Macro-F1, its QWK remains below A43, and it has no
positive A epoch.

A45 passes only the B/C/D preservation gate at this horizon. It fails the
Macro-F1 >= .72 and QWK >= .693671 screen gates. Epoch10 Macro-F1 is .5008251
with QWK .5833255. AMP skipped-update total is nine and all losses are finite.

Continue the preregistered 50 epochs unchanged. Do not expand to other folds
or tune on fold1 before completed50 and the read-only audit. These are DEV
selection results, not independent test estimates; the single A exam makes
A behavior case-level evidence.

W&B: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/1k59zmph
