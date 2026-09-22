# VinDR L2 ordinal coefficient 0.1 CV5 result

Date: 2026-09-19. Controlled change versus B0: ordinal loss coefficient
0.5 to 0.1 only. DenseNet121 hierarchical fusion, split seed 42, training
seed 42, cache, natural sampling, resize and remaining optimization settings
are retained. All five runs completed 50 epochs on RTX 5090, excluding Vesta.

## Selected DEV results

| Fold | Best epoch | Macro-F1 | Accuracy | QWK | F1 A / B / C / D | Epoch-50 F1 |
|---:|---:|---:|---:|---:|---|---:|
| 0 | 22 | 0.775419 | 0.819307 | 0.621276 | 1.000000 / 0.650602 / 0.882448 / 0.568627 | 0.536475 |
| 1 | 3 | 0.560827 | 0.833747 | 0.674534 | 0.000000 / 0.714286 / 0.890365 / 0.638655 | 0.489292 |
| 2 | 5 | 0.634974 | 0.843672 | 0.647830 | 0.400000 / 0.705882 / 0.906542 / 0.527473 | 0.488051 |
| 3 | 17 | 0.606002 | 0.821782 | 0.645588 | 0.333333 / 0.600000 / 0.890675 / 0.600000 | 0.531165 |
| 4 | 20 | 0.675618 | 0.808933 | 0.603574 | 0.666667 / 0.578947 / 0.877419 / 0.579439 | 0.492464 |

Primary mean Macro-F1: **0.650568**, sample SD **0.081391**.
Mean accuracy: 0.825488; mean QWK: 0.638560.
Mean class F1 A/B/C/D: [0.480000,0.649944,0.889490,0.582839].
Mean B/C/D F1: 0.707424 versus baseline 0.693730.
Epoch-50 mean Macro-F1: 0.507489, sample SD 0.024163.

Pooled descriptive Macro-F1 is 0.649281 on 2,017 unique cases, with support
[6,196,1556,259]. Pooled confusion matrix:
[[4,2,0,0],[7,124,65,0],[0,59,1382,115],[0,0,104,155]].
The pooled metric does not replace the per-fold mean.

## Verification and decision

All Slurm tasks completed with exit 0. The final fold (746_4) completed in
1h13m57s on worker-3 with Vesta excluded. The reproducible audit verified
exact epochs 1--50, common learning configuration and protocol metadata,
assignment digest, registered FIT/DEV manifests, checkpoint selection,
prediction membership and labels, normalized finite probabilities, argmax,
recomputed metrics, non-overlapping CV coverage and finished W&B states.

The target is not met. L2 improves selected mean Macro-F1 over B0 by 0.049318
but remains below A1's 0.679975. Fold dispersion is higher than B0's 0.056188.
B/C/D improvement is modest; the rare A class remains unstable. Do not expand
L2 alone to multiple seeds. A large ordinal loss value is not evidence of
harmful gradients by itself; see ordinal_loss_diagnostic_20260919.md.

These results use DEV for checkpoint/model selection and are not independent
test estimates. Machine-readable results are in the companion JSON file.

## W&B runs

- Fold 0: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/7aoquqms
- Fold 1: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/6jy6a7lh
- Fold 2: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/4vgdqbob
- Fold 3: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/ofu6s261
- Fold 4: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/53akuiz4
