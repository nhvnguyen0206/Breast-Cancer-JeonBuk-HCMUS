# A30 completed CV5: dropout 0.4 with sampling power 0.25

A30 changes only model dropout from 0.3 to 0.4 relative to A6. Shared
DenseNet121, hierarchical fusion, sampling power 0.25, augmentation, losses,
optimizer, seed 42, cache, and frozen grouped split are unchanged. Inference
uses one flat-head checkpoint per fold; there is no ensemble.

Fold 0 is the original completed screen from job 981. Folds 1–4 are the
unchanged confirmation from array job 982. Every task completed 50 epochs on
permitted RTX 5090 nodes with exit code 0:0. No Vesta node was used. The
read-only audit passed, the assignment digest remained
`43daa86936ee7b1bae1b200836fb1afdfe0c8294c7c865d8f5758bf989f12a9a`,
and all five source W&B runs were independently read back as `finished`.

| Fold | Best epoch | Macro-F1 | Accuracy | QWK | F1 A/B/C/D |
|---|---:|---:|---:|---:|---:|
| 0 | 11 | 0.7025951909 | 0.8391089109 | 0.6494927923 | 0.666667 / 0.578313 / 0.898734 / 0.666667 |
| 1 | 20 | 0.7584943371 | 0.8312655087 | 0.5920688321 | 1.000000 / 0.658228 / 0.894737 / 0.481013 |
| 2 | 27 | 0.6402752997 | 0.8238213400 | 0.6223055295 | 0.500000 / 0.658824 / 0.890650 / 0.511628 |
| 3 | 2 | 0.6864294858 | 0.8514851485 | 0.6698490116 | 0.500000 / 0.727273 / 0.906200 / 0.612245 |
| 4 | 43 | 0.7618615908 | 0.8213399504 | 0.5953815261 | 1.000000 / 0.623377 / 0.886435 / 0.537634 |

Selected-DEV aggregate: mean Macro-F1 **0.7099311809**, sample SD
**0.0512670358**, minimum **0.6402752997**, mean accuracy **0.8334041717**,
and mean QWK **0.6258195383**. Mean class F1 A/B/C/D is
0.733333/0.649203/0.895351/0.561837; mean B/C/D F1 is 0.702130. The pooled
descriptive Macro-F1 is 0.693851 over 2,017 cases.

The mean threshold (>= 0.70) passes. The sample-SD threshold (<= 0.05) and
minimum-fold threshold (>= 0.65) narrowly fail, so A30 is not accepted as a
stable solution. The epoch-50 mean is only 0.518622, while selected epochs
range from 2 to 43; checkpoint selection sensitivity remains substantial.
Only six class-A cases exist, so the class-A mean is not robust evidence.
These are repeatedly selected DEV results, not an independent test.

Audited W&B summary:
https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/n8yrk899

