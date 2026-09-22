# A40 ConvNeXt-Tiny CV5 expansion launch

After both fixed screen audits passed and the registered two-fold gates were
met, A40 expanded to the remaining folds 0, 2 and 4 as Slurm array job 1024.
The original completed job-1022 folds 1 and 3 are preserved and will be used
unchanged in the final CV5 aggregate.

Folds 0 and 2 run on `slurm-b20a-master-0`; fold 4 was initially pending for
resources on that two-GPU node and was reassigned before training began to
`slurm-b40a-worker-1`. Direct GPU checks and each training log report
`NVIDIA GeForce RTX 5090`. No task uses worker2/Vesta.

All three tasks use the same immutable A40 snapshot, config, seed 42, cache,
frozen split and assignment digest as folds 1/3. Each is registered for 50
epochs with no requeue. W&B:

- fold 0: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/sqcl5ezc
- fold 2: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/o3ln0ceo
- fold 4: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/qfsuypzh

Final acceptance requires all five audits to PASS and the complete CV5 mean
Macro-F1 >=0.70, sample SD <=0.05 and minimum fold >=0.65. These are selected
DEV results, not an independent test.
