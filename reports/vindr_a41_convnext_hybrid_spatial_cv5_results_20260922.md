# A41 completed CV5: ConvNeXt hybrid relational-spatial fusion

A41 preserves A40's ConvNeXt global hierarchical relational path and adds a
learned spatial/view-token Transformer as a residual correction. Backbone,
heads, losses, optimizer, sampling, augmentation, cache, grouped split and
seed 42 remain fixed. Each fold uses one model/checkpoint and one inference
path; there is no ensemble.

All five runs completed 50 epochs on permitted RTX 5090 nodes. No task used
worker2/Vesta. All five read-only audits PASS, validating histories,
checkpoints, prediction files, probability normalization, frozen manifests,
assignment SHA256
`43daa86936ee7b1bae1b200836fb1afdfe0c8294c7c865d8f5758bf989f12a9a`
and finished W&B state/summary.

| Fold | Best epoch | Macro-F1 | Accuracy | QWK | F1 A/B/C/D |
|---|---:|---:|---:|---:|---:|
| 0 | 4 | 0.8280128668 | 0.8465346535 | 0.7183085920 | 1.000000 / 0.720000 / 0.895623 / 0.696429 |
| 1 | 16 | 0.8321319993 | 0.8808933002 | 0.7111887485 | 1.000000 / 0.783784 / 0.925697 / 0.619048 |
| 2 | 3 | 0.5583275293 | 0.8486352357 | 0.6571265185 | 0.000000 / 0.732394 / 0.904762 / 0.596154 |
| 3 | 7 | 0.7170961423 | 0.8341584158 | 0.6654802511 | 0.666667 / 0.708861 / 0.892857 / 0.600000 |
| 4 | 32 | 0.8259769927 | 0.8560794045 | 0.7007783297 | 1.000000 / 0.809524 / 0.906149 / 0.588235 |

Selected-DEV aggregate: mean Macro-F1 **0.7523091061**, sample SD
**0.1187418588**, minimum **0.5583275293**, mean accuracy **0.8532602020**,
and mean QWK **0.6905764880**. Mean class F1 A/B/C/D is
0.733333/0.750913/0.905017/0.619973. Mean epoch-50 Macro-F1 is
0.5303260639.

The mean exceeds both the 0.70 requirement and 0.75 stretch target, but SD
and minimum fail decisively. A41 is therefore **rejected** as the stable
solution. The architecture improves A40's mean, B/C/D balance, accuracy and
QWK, but fold 2 remains an isolated failure.

Across all 50 fold-2 epochs, A40 and A41 never achieve positive class-A F1,
while A30 DenseNet achieves positive A F1 in 47/50 epochs. At A41's selected
checkpoint, B/C/D mean F1 is 0.744437, higher than A40 and A30. This localizes
the remaining fold-2 failure to loss of the rare A decision region after the
ConvNeXt replacement, rather than a general B/C/D representation failure.
Only one A case occurs in this DEV fold, so the observation is fragile but
consistent across every epoch.

W&B IDs: twd1bi2e, o1khepub, f12x7ilg, jms2mbgl and ysfrdx6l in project
`TN_Mammo_BreastDensity/HCMUS-paper1`.

The next controlled structural hypothesis should retain A41's improved B/C/D
representation and replace only the flat primary head with a hierarchical
A-vs-rest gate plus conditional B/C/D classifier. The combined four-class
distribution remains one differentiable, single-model inference path.
