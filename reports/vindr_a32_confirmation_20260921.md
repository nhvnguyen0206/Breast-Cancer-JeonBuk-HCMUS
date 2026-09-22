# A32 five-fold confirmation

Completed and audited fold 0 from job 987 is retained unchanged. After its
0.7771719287 selected-DEV Macro-F1 passed the amended 0.70 gate, folds 1–4
were submitted as array job 988 from the identical immutable A32 snapshot
and config. Fold 0 was not rerun.

Startup verification: tasks 1–4 are RUNNING, tasks 1/2 on master and tasks
3/4 on worker1; every launch log explicitly reports `NVIDIA GeForce RTX
5090`. Worker2/Vesta is excluded, with no restart or requeue.

W&B source runs:

- fold 0: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/4fyhjmkw
- fold 1: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/ohc9o4zi
- fold 2: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/vnbvhiuc
- fold 3: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/3a1trh2a
- fold 4: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/ltf1g5qs

Run all confirmation tasks for 50 epochs. Interim summaries use common
10–20 epoch horizons; no acceptance claim before all tasks complete and the
full audit passes. Final criteria: mean >=0.70, sample SD <=0.05, minimum
>=0.65. Results are selected DEV, not independent test; six A cases limit
interpretation.
