# A40 ConvNeXt-Tiny two-fold launch

A40 launched as Slurm array job 1022 on only the preregistered weakest folds
1 and 3. Both tasks are running on `slurm-b20a-master-0`, and both logs verify
`NVIDIA GeForce RTX 5090`. Vesta/worker2 is excluded. The immutable snapshot
is `/slurmshared/Ngoc/code/hcmus-density-convnext-relational-20260922-v1`.

The frozen assignment SHA256 is
`43daa86936ee7b1bae1b200836fb1afdfe0c8294c7c865d8f5758bf989f12a9a`.
Each run uses seed 42, the fixed cache, four views at 512 pixels, ConvNeXt-Tiny
with ImageNet initialization, A30 relational fusion/flat head/loss/training,
and the registered 50 epochs. The only model change from A30 is the backbone.

W&B:

- fold 1: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/kgp5gj2y
- fold 3: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/itp6g9co

Do not launch folds 0/2/4 unless both completed audits PASS, the selected-DEV
two-fold mean Macro-F1 is >=0.70, and neither fold is below 0.65.
