# A46 fold1: matched first40

Job 1057_1 remains RUNNING on `slurm-b20a-master-0` with an RTX5090. Its
history contains complete epochs 1--40 with finite losses. Selection below is
best DEV Macro-F1 within the identical first-40-epoch horizon on frozen
fold1, window16 cache and seed42.

| Arm | Selected epoch | Macro-F1 | Accuracy | QWK | B/C/D mean F1 | A-positive epochs |
|---|---:|---:|---:|---:|---:|---:|
| A43 | 4 | .5850244052 | .8114143921 | .6936709874 | .7133658737 | 1/40 |
| A44 | 19 | .7641791946 | .8337468983 | .5916055358 | .6855722594 | 1/40 |
| A45 | 20 | .5572461406 | .8486352357 | .6671180382 | .7429948541 | 0/40 |
| A46 | 25 | .5475738683 | .8610421836 | .6585365854 | .7300984910 | 0/40 |

A46 selected F1 A/B/C/D is
`[0,.6764705882,.9185867896,.5952380952]`. Its confusion matrix, true rows
and predicted columns A/B/C/D, is
`[[0,1,0,0],[2,23,14,0],[0,5,299,8],[0,0,26,25]]`.

The best checkpoint moves from epoch15 at first20 to epoch25, but Macro-F1
increases by only .0011645. A46 has the highest accuracy among A43--A46 at
this horizon, yet trails A45 by .0096723 Macro-F1, .0128964 B/C/D mean and
.0085815 QWK. Relative to A43, B/C/D mean is .0167326 higher but Macro-F1 is
.0374505 lower. No epoch has positive A F1 or Macro-F1 >= .72; longest
positive-A streak is zero. A46 passes only B/C/D preservation and fails the
Macro-F1/QWK expansion gates.

At epoch40 A46 Macro-F1 is .5381235, accuracy .8436725, QWK .6208390 and F1
`[0,.6865672,.9034268,.5625]`. Total AMP skipped updates are 19 and all
losses are finite. This remains selected DEV, not independent evidence.
Finish the registered 50 epochs unchanged, run the read-only audit and apply
all gates; do not expand or tune from first40.

W&B: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/2rzbst10
