# A39 completed two-fold screen: wide-gap ordinal primary head

A39 changes only the primary prediction parameterization relative to A30:
the flat four-class head is replaced by a monotonic ordinal head initialized
with threshold gap 2.0. DenseNet121, hierarchical relational fusion, losses,
sampling, optimizer, seed 42, cache and grouped split remain fixed. Each fold
ran the registered 50 epochs on the permitted RTX 5090 node. No ensemble and
no Vesta/worker2 were used.

Both read-only audits PASS. They validated the complete histories, selected
checkpoints, prediction files, frozen manifests, assignment SHA256
`43daa86936ee7b1bae1b200836fb1afdfe0c8294c7c865d8f5758bf989f12a9a`,
probability normalization and completed W&B records.

| Fold | Best epoch | Macro-F1 | Accuracy | QWK | F1 A/B/C/D |
|---|---:|---:|---:|---:|---:|
| 1 | 26 | 0.5427479530 | 0.8411910670 | 0.6398469573 | 0.000000 / 0.666667 / 0.900158 / 0.604167 |
| 3 | 19 | 0.7053704434 | 0.8341584158 | 0.6492146597 | 0.666667 / 0.682927 / 0.894569 / 0.577320 |

The two-fold mean is **0.6240591982**, sample SD **0.1149914658**, and
minimum **0.5427479530**. The registered expansion conditions (mean >=0.70
and minimum >=0.65) both fail, so folds 0/2/4 must not be launched. A39 is
rejected.

The wider gap fixed A38's invalid initial middle-class argmax geometry, as
shown by fold 3, but did not repair fold 1. Compared with the same A30 folds
(0.7584943371 and 0.6864294858), A39 lowers their mean from 0.7224619115 to
0.6240591982 and greatly increases dispersion. Fold 1 again has F1_A=0;
given only one A case in that DEV fold, this is not sufficient by itself to
explain the much broader instability.

W&B:

- fold 1: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/fzts4z74
- fold 3: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/1qqpu7sq

The next registered arm is A40, which returns to A30's flat head and changes
the backbone to ConvNeXt-Tiny. It may proceed only after its real 512-pixel
RTX 5090 forward/backward/update preflight passes.
