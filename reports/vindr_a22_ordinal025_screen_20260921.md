# A22 fold0 screen — completed audit

Job `950_0` completed all 50 epochs on the master RTX 5090 with exit code
`0:0`, no requeue and no restart. The read-only audit passed checkpoint,
prediction, split-manifest, probability, provenance and W&B consistency checks.

- Selected epoch: **22**
- Macro-F1: **0.771853**
- Accuracy: **0.801980**
- QWK: **0.625822**
- F1 A/B/C/D: **1.000000 / 0.595745 / 0.866667 / 0.625000**
- Severe errors: **0**
- Epochs at or above 0.75: **1/50**
- Total AMP skipped updates: **17**

The preregistered fold0 gate passed. Confirmation job `951_[1-4]` was launched
for folds 1--4 only, with worker2/Vesta excluded and an in-job RTX 5090
assertion. This is selected DEV performance, not an independent test; class A
contains one fold0 DEV study.

[W&B fold0 run](https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/gdne1bkg)

Confirmation runs: [fold 1](https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/8jhy78kl),
[fold 2](https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/43295usj),
[fold 3](https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/p96msbjn), and
[fold 4](https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/dj5bsgwx).
