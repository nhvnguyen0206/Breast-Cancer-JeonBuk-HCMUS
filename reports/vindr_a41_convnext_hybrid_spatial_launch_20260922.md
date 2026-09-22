# A41 ConvNeXt hybrid-spatial two-fold launch

A41 launched as Slurm array job 1031 on only the fixed historically weak
folds 1 and 3. Both tasks run on `slurm-b20a-master-0`; logs verify
`NVIDIA GeForce RTX 5090`. Worker2/Vesta is not used.

The immutable snapshot is
`/slurmshared/Ngoc/code/hcmus-density-convnext-hybrid-spatial-20260922-v1`.
Both tasks use the corrected frozen manifests with assignment SHA256
`43daa86936ee7b1bae1b200836fb1afdfe0c8294c7c865d8f5758bf989f12a9a`,
seed 42 and the registered 50 epochs.

W&B:

- fold 1: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/o1khepub
- fold 3: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/jms2mbgl

Do not expand to folds 0/2/4 unless both completed audits PASS, two-fold mean
Macro-F1 >=0.70 and minimum >=0.65.
