# A34 five-fold confirmation

The completed, audited fold 0 from job 997 is retained unchanged. After it
passed the registered Macro-F1 >=0.70 screen gate, only folds 1–4 were
submitted as array job 998 from the identical immutable A34 snapshot/config.

All four tasks started with `Requeue=0`, `Restarts=0` on permitted RTX 5090
nodes (`slurm-b20a-master-0` and `slurm-b40a-worker-1`). worker2/Vesta is
excluded by the immutable launcher. No fold was rerun or selected by outcome.

W&B runs:

- fold 0: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/6bhg258e
- fold 1: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/v9oaqxul
- fold 2: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/n12l50ul
- fold 3: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/g4a8wqyv
- fold 4: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/32h0eb36

Each confirmation fold must run all 50 epochs. Review common horizons every
10–20 epochs. Final acceptance requires audited mean Macro-F1 >=0.70, sample
SD <=0.05, and minimum fold >=0.65. Results are selected DEV, not an
independent test.
