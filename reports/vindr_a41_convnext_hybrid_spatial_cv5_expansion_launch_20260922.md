# A41 hybrid-spatial CV5 expansion launch

After both fixed screen audits passed and the registered two-fold gates were
met, A41 expanded to folds 0, 2 and 4 as Slurm array job 1033. The completed
job-1031 folds 1 and 3 are preserved unchanged for final aggregation.

Folds 0/2 run on `slurm-b20a-master-0`; fold 4 runs on
`slurm-b40a-worker-1`. All logs verify `NVIDIA GeForce RTX 5090`. No task uses
worker2/Vesta. All runs use the same immutable A41 snapshot, config, seed 42,
cache, frozen grouped split and assignment digest, for 50 epochs.

W&B:

- fold 0: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/twd1bi2e
- fold 2: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/f12x7ilg
- fold 4: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/ysfrdx6l

Final acceptance requires all five audits PASS, mean Macro-F1 >=0.70, sample
SD <=0.05 and minimum fold >=0.65. These remain selected DEV results.
