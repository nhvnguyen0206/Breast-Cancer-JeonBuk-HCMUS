# A40 completed two-fold screen: ConvNeXt-Tiny relational model

A40 replaces only A30's DenseNet121 image backbone with ImageNet-pretrained
ConvNeXt-Tiny. Hierarchical relational fusion, flat primary head, auxiliary
heads, losses, optimizer, sampling, augmentation, cache, grouped split and
seed 42 remain fixed. There is one model/checkpoint per fold and no ensemble.

Both job-1022 runs completed 50 epochs on the permitted RTX 5090 node. Both
read-only audits PASS, including complete histories, selected checkpoints,
prediction files, probability normalization, all frozen fold manifests,
assignment SHA256
`43daa86936ee7b1bae1b200836fb1afdfe0c8294c7c865d8f5758bf989f12a9a`
and W&B state/summary.

| Fold | Best epoch | Macro-F1 | Accuracy | QWK | F1 A/B/C/D |
|---|---:|---:|---:|---:|---:|
| 1 | 4 | 0.8126870715 | 0.8560794045 | 0.6873629019 | 1.000000 / 0.655172 / 0.907051 / 0.688525 |
| 3 | 34 | 0.6936746863 | 0.8316831683 | 0.6251807788 | 0.666667 / 0.647887 / 0.894488 / 0.565657 |

The two-fold mean is **0.7531808789**, sample SD **0.0841544646**, and
minimum **0.6936746863**. Both registered expansion gates pass: mean >=0.70
and minimum >=0.65. Fold 3 improved after the first30 milestone, so the full
registered horizon materially changed its selected checkpoint.

Epoch-50 scores are only 0.5464473229 and 0.4963791084. Thus A40 still has
large selected-to-final decay, and the two-fold SD is above the final CV5
stability target. Expansion is justified by the preregistered gate, but final
acceptance remains unknown until folds 0/2/4 complete and all five audits are
aggregated. Rare-class A has only three cases across these DEV folds and is
not robust evidence by itself.

W&B:

- fold 1: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/kgp5gj2y
- fold 3: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/itp6g9co
