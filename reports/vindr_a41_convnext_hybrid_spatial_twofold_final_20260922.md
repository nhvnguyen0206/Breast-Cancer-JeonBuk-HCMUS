# A41 completed two-fold screen: ConvNeXt hybrid relational-spatial fusion

A41 preserves A40's ConvNeXt global hierarchical relational path and adds a
learned residual spatial/view-token Transformer. Backbone, heads, losses,
optimizer, sampling, augmentation, cache, grouped split and seed remain fixed.
There is one model/checkpoint per fold and no ensemble.

Both job-1031 runs completed 50 epochs on the permitted RTX 5090 node. Both
read-only audits PASS, including complete histories, selected checkpoints,
prediction files, probability normalization, all fold manifests, frozen
assignment SHA256
`43daa86936ee7b1bae1b200836fb1afdfe0c8294c7c865d8f5758bf989f12a9a`
and finished W&B state/summary.

| Fold | Best epoch | Macro-F1 | Accuracy | QWK | F1 A/B/C/D |
|---|---:|---:|---:|---:|---:|
| 1 | 16 | 0.8321319993 | 0.8808933002 | 0.7111887485 | 1.000000 / 0.783784 / 0.925697 / 0.619048 |
| 3 | 7 | 0.7170961423 | 0.8341584158 | 0.6654802511 | 0.666667 / 0.708861 / 0.892857 / 0.600000 |

The two-fold mean is **0.7746140708**, sample SD **0.0813426346**, and
minimum **0.7170961423**. Both registered expansion gates pass. Relative to
A40, A41 improves both screen folds and improves multiple B/C/D metrics, so
the gain is not only the three rare class-A cases.

Epoch-50 scores are 0.5174687346 and 0.5284593202, so checkpoint sensitivity
persists. Expansion is justified by the registered gate, but final stability
is unknown until folds 0/2/4 complete and all five audits are aggregated.

W&B:

- fold 1: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/o1khepub
- fold 3: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/jms2mbgl
