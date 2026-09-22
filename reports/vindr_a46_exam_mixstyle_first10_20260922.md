# A46 fold1: matched first10

Job 1057_1 is RUNNING on `slurm-b20a-master-0` with an RTX5090. Its history
contains complete epochs 1--10 with finite losses. Each arm below is selected
independently by best DEV Macro-F1 within the same first-ten-epoch horizon on
the frozen fold1, window16 cache and seed42.

| Arm | Selected epoch | Macro-F1 | Accuracy | QWK | B/C/D mean F1 | A-positive epochs |
|---|---:|---:|---:|---:|---:|---:|
| A43 | 4 | .5850244052 | .8114143921 | .6936709874 | .7133658737 | 1/10 |
| A44 | 4 | .5418260416 | .7965260546 | .6321601104 | .7224347221 | 0/10 |
| A45 | 4 | .5472872527 | .8089330025 | .6438008655 | .7297163369 | 0/10 |
| A46 | 8 | .5321024419 | .8387096774 | .6145923757 | .7094699226 | 0/10 |

A46 selected F1 A/B/C/D is
`[0,.6849315068,.9,.5434782609]`. Its confusion matrix, true rows and
predicted columns A/B/C/D, is
`[[0,1,0,0],[0,25,14,0],[0,8,288,16],[0,0,26,25]]`.

At this horizon A46 has the highest accuracy but trails A45 by .0151848
Macro-F1 and .0202464 B/C/D mean, and trails A43 by .0529220 Macro-F1. It
has no positive-A epoch, no Macro-F1 >= .72 epoch and its longest positive-A
streak is zero. All three preregistered expansion gates currently fail:
Macro-F1 .5321024 < .72, B/C/D .7094699 < .7133659 and QWK .6145924 <
.6936710. Total AMP skipped updates are nine and losses are finite.

This is an interim selected-DEV comparison, not independent evidence. Continue
the registered 50 epochs unchanged; do not expand or retune from first10.

W&B: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/2rzbst10
