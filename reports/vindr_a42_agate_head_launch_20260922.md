# A42 A-gate diagnostic control launch

A42 was launched as Slurm array job `1037` on the registered folds 1 and 3.
Both tasks are running on `slurm-b20a-master-0`, and both logs identify the
allocated device as `NVIDIA GeForce RTX 5090`. Vesta/worker2 is not used.

| Fold | W&B ID | W&B URL |
|---:|---|---|
| 1 | `5lsfvwi2` | https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/5lsfvwi2 |
| 3 | `jglym8l6` | https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/jglym8l6 |

The remote immutable snapshot is
`/slurmshared/Ngoc/code/hcmus-density-convnext-hybrid-agate-20260922-v1`.
The runs use the frozen assignment SHA256
`43daa86936ee7b1bae1b200836fb1afdfe0c8294c7c865d8f5758bf989f12a9a`,
seed 42, the registered 50 epochs and W&B project `HCMUS-paper1`.

This arm remains a diagnostic head ablation. It must finish and be audited;
its existence does not prevent preparation of the major architecture redesign
requested after launch. No expansion decision is allowed from early epochs.
