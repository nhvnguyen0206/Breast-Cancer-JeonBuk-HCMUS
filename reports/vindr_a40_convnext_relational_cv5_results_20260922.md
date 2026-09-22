# A40 completed CV5: ConvNeXt-Tiny with hierarchical relational fusion

A40 changes only A30's image backbone from DenseNet121 to ImageNet-pretrained
ConvNeXt-Tiny. The hierarchical relational fusion, flat/ordinal/binary heads,
losses, sampling, optimizer, augmentation, cache, grouped split and seed 42
remain fixed. Each fold uses one checkpoint and one inference path; there is
no ensemble.

All five runs completed 50 epochs on permitted RTX 5090 nodes. No task used
worker2/Vesta. All five read-only audits PASS, validating complete histories,
best checkpoints, prediction files, probability sums, frozen manifests,
assignment SHA256
`43daa86936ee7b1bae1b200836fb1afdfe0c8294c7c865d8f5758bf989f12a9a`
and finished W&B state/summary.

| Fold | Best epoch | Macro-F1 | Accuracy | QWK | F1 A/B/C/D |
|---|---:|---:|---:|---:|---:|
| 0 | 8 | 0.8212558177 | 0.8688118812 | 0.6972285068 | 1.000000 / 0.701299 / 0.917058 / 0.666667 |
| 1 | 4 | 0.8126870715 | 0.8560794045 | 0.6873629019 | 1.000000 / 0.655172 / 0.907051 / 0.688525 |
| 2 | 3 | 0.5439920998 | 0.8287841191 | 0.6332256150 | 0.000000 / 0.743590 / 0.890323 / 0.542056 |
| 3 | 34 | 0.6936746863 | 0.8316831683 | 0.6251807788 | 0.666667 / 0.647887 / 0.894488 / 0.565657 |
| 4 | 1 | 0.7268438333 | 0.8535980149 | 0.6760494298 | 0.666667 / 0.724638 / 0.908228 / 0.607843 |

Selected-DEV aggregate: mean Macro-F1 **0.7196907017**, sample SD
**0.1124297521**, minimum **0.5439920998**, mean accuracy **0.8477913176**,
and mean QWK **0.6638094465**. Mean class F1 A/B/C/D is
0.666667/0.694517/0.903430/0.614149. Mean epoch-50 Macro-F1 is only
0.5340460383.

The mean gate passes, but the SD and minimum-fold gates fail decisively, so
A40 is **rejected** as the stable solution. It nevertheless improves A30's
mean from 0.7099311809 to 0.7196907017 and its mean accuracy/QWK, showing that
backbone capacity is useful. The regression is concentrated in fold 2 and
the selected epochs span 1--34, indicating severe fold-dependent optimization
and checkpoint sensitivity. Only six class-A cases exist, so the high mean A
F1 is not robust evidence. These are selected DEV results, not an independent
test estimate.

W&B runs: sqcl5ezc, kgp5gj2y, o3ln0ceo, itp6g9co and qfsuypzh in project
`TN_Mammo_BreastDensity/HCMUS-paper1`.

The next architecture should not merely change another scalar hyperparameter.
It should preserve the strong ConvNeXt global relational path while adding a
residual spatial/view-aware fusion path, so learned regional interactions can
help without discarding the stable global representation at initialization.
