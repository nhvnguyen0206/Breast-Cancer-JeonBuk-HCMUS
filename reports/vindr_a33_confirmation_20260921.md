# A33 five-fold confirmation

Completed and audited fold 0 from job 992 is retained unchanged. After its
0.8159754728 selected-DEV Macro-F1 passed the 0.70 gate, folds 1–4 were
submitted as array job 993 from the identical immutable A33 snapshot/config.
Fold 0 was not rerun.

Startup verification: all four tasks are RUNNING; tasks 1/2 use master and
tasks 3/4 use worker1. Every log explicitly reports `NVIDIA GeForce RTX
5090`; worker2/Vesta is excluded, with no restart or requeue.

W&B source runs:

- fold 0: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/x6422mve
- fold 1: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/1ifsqlfk
- fold 2: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/qdysa2as
- fold 3: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/apgkweq6
- fold 4: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/do5sli1k

Run all confirmation tasks for 50 epochs. Interim summaries use common
10–20 epoch horizons; no acceptance claim before all tasks complete and the
full audit passes. Final gates: mean >=0.70, sample SD <=0.05, minimum
>=0.65. Selected DEV is not independent test; six A cases limit inference.
