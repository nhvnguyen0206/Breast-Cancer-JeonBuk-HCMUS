# A46 fold1: matched first20

Job 1057_1 remains RUNNING on `slurm-b20a-master-0` with an RTX5090. Its
history contains complete epochs 1--20 with finite losses. Selection below is
independently best DEV Macro-F1 within the same first-20-epoch horizon on the
frozen fold1, window16 cache and seed42.

| Arm | Selected epoch | Macro-F1 | Accuracy | QWK | B/C/D mean F1 | A-positive epochs |
|---|---:|---:|---:|---:|---:|---:|
| A43 | 4 | .5850244052 | .8114143921 | .6936709874 | .7133658737 | 1/20 |
| A44 | 19 | .7641791946 | .8337468983 | .5916055358 | .6855722594 | 1/20 |
| A45 | 20 | .5572461406 | .8486352357 | .6671180382 | .7429948541 | 0/20 |
| A46 | 15 | .5464094091 | .8312655087 | .6426932304 | .7285458789 | 0/20 |

A46 selected F1 A/B/C/D is
`[0,.7058823529,.8935483871,.5862068966]`. Its confusion matrix, true rows
and predicted columns A/B/C/D, is
`[[0,1,0,0],[1,24,14,0],[0,4,277,31],[0,0,17,34]]`.

A46 trails A45 by .0108367 Macro-F1, .0144490 B/C/D mean and .0244248 QWK.
Relative to A43 it is .0386150 lower in Macro-F1 while B/C/D mean is .0151800
higher. It has no positive-A epoch, no Macro-F1 >= .72 epoch and longest
positive-A streak zero. It currently passes only the B/C/D preservation gate;
Macro-F1 .5464094 < .72 and QWK .6426932 < .6936710 fail. Total AMP skipped
updates are 12, matching A45 at first20, and losses are finite.

Epoch20 itself reaches Macro-F1 .5427101, accuracy .8411911, QWK .6514218
and F1 `[0,.6756757,.9033281,.5918367]`; the selected checkpoint is not the
horizon boundary. This remains selected DEV, not independent evidence.
Continue the registered full50 unchanged; do not expand or retune from
first20. The next scheduled comparison is epoch40, then completed50 audit.

W&B: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/2rzbst10
