# VinDR A1 shared-geometry augmentation CV5 result

Date: 2026-09-19

Protocol: fixed grouped density CV5 seed 42, assignment SHA
`43daa86936ee7b1bae1b200836fb1afdfe0c8294c7c865d8f5758bf989f12a9a`.
All runs used the same DenseNet121 hierarchical-fusion model, fresh ImageNet
initialization, stretch resize, natural sampling and baseline optimization.
Relative to B0, A1 adds only shared four-view affine augmentation (rotation up
to 5 degrees and translation up to 3%) while retaining shared brightness.
Each fold ran exactly 50 epochs on RTX 5090; Vesta was excluded.

## Selected DEV results

| Fold | Best epoch | Macro-F1 | Accuracy | QWK | F1 A | F1 B | F1 C | F1 D | Epoch-50 F1 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 38 | 0.804868 | 0.849010 | 0.668941 | 1.000000 | 0.675676 | 0.903021 | 0.640777 | 0.781052 |
| 1 | 5 | 0.560361 | 0.843672 | 0.682840 | 0.000000 | 0.691589 | 0.898693 | 0.651163 | 0.494223 |
| 2 | 21 | 0.649828 | 0.796526 | 0.572718 | 0.666667 | 0.612245 | 0.870400 | 0.450000 | 0.515132 |
| 3 | 9 | 0.634811 | 0.853960 | 0.658255 | 0.400000 | 0.603175 | 0.913846 | 0.622222 | 0.557184 |
| 4 | 38 | 0.750009 | 0.799007 | 0.580785 | 1.000000 | 0.620690 | 0.869144 | 0.510204 | 0.510712 |

Primary aggregate (unweighted mean of five fold metrics):

- Macro-F1 **0.679975**, sample SD **0.097159**.
- Accuracy **0.828435**, sample SD 0.028245.
- QWK **0.632708**, sample SD 0.051898.
- Mean per-class F1 A/B/C/D:
  **0.613333 / 0.640675 / 0.891021 / 0.574873**.
- Mean B/C/D F1: **0.702190**.
- Epoch-50 Macro-F1: **0.571661**, sample SD 0.119333.

For comparison, B0 mean Macro-F1 was 0.601250 (sample SD 0.056188), mean
accuracy 0.818550, mean QWK 0.620394 and mean B/C/D F1 0.693730. A1 therefore
improves mean selected Macro-F1 by 0.078726 and B/C/D by only 0.008460, while
substantially increasing fold dispersion.

Decomposing the Macro-F1 gain by class gives A/B/C/D contributions of
0.072381 / 0.004854 / 0.001763 / -0.000272. Thus 91.94% of the net gain
comes from A, supported by only six cases. B/C/D mean changes by fold are
+0.051656 / -0.002889 / -0.032539 / -0.016964 / +0.043035: it declines in
three of five folds. These are arithmetic contributions at selected DEV
checkpoints, not causal estimates of augmentation effects.

## Pooled descriptive check

The union contains exactly 2,017 unique DEV cases, with support A/B/C/D
[6,196,1556,259]. Pooled (descriptive, not a replacement for the fold mean):

- Macro-F1 0.681912, accuracy 0.828458, QWK 0.632102.
- Per-class F1 [0.615385,0.643357,0.891228,0.577681].
- Confusion matrix:
  `[[4,2,0,0],[3,138,55,0],[0,93,1397,66],[0,0,127,132]]`.

## Audit and interpretation

All five jobs completed with exit code 0. The audit verified exact epochs
1--50, selected checkpoint/history agreement, fixed fold/assignment metadata,
all DEV IDs and labels, finite normalized probabilities, argmax predictions,
independently recomputed metrics, 2,017-case non-overlapping CV coverage, and
W&B state `finished` with 50 completed epochs.

W&B runs by fold:

- fold 0: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/rm5cgljr
- fold 1: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/obhrh9bo
- fold 2: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/ffuqaxqv
- fold 3: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/snvrmwj8
- fold 4: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/fnfddqkp

A1 fails the target: mean CV5 Macro-F1 is below 0.75 and variance is high.
Fold 0 and fold 4 cross 0.75 partly because their single A case is correct;
fold 1 misses its A entirely. A1 should not proceed to multi-seed stability
testing or be described as a successful solution. These are selected DEV
results, not an independent-test estimate.
