# A30 confirmation under revised user threshold

See goal_threshold_revision_20260921.md: user revised aim to .70 after
completed screen, so original .75 gate is explicitly superseded. Screen
job981 fold0 audited PASS at .7025951908901428, W&B finished.
Preserve original fold0; no rerun or favorable-fold replacement.

Before submission: user queue empty; immutable config SHA256 unchanged:
a9a96fd9e28dbfa8a34d187376e416d191bb6605bb5d5f9bb0ab7cb2806c112d.
Reviewed launcher: excludes worker2, asserts RTX5090 at runtime, online
HCMUS-paper1, no requeue, original immutable source and split.
Submitted array982 tasks1–4 only, full50 each, same snapshot/config as981.
No Vesta. A31 remains unsubmitted.

Final evaluation combines981-fold0 with982-fold1–4; mean>=.70,
sampleSD<=.05 and minimum>=.65 on seed42. Selected DEV, not independent
test. Report A/B/C/D and BCD diagnostics; six A cases limit inference.
Do not claim acceptance before all jobs finish and complete audit passes.

## Startup verification

All982 tasks1–4 RUNNING; launch logs explicitly NVIDIA GeForce RTX5090.
Tasks1/2 on master, tasks3/4 on worker1. At elapsed7:29 all had5 completed
epochs with finite recorded training losses. W&B run URLs from launch logs:

- fold1: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/hr7gemp9
- fold2: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/hcmxmcdw
- fold3: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/xm3smofb
- fold4: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/8c5663vr

These URLs identify logging runs, not proof of completed remote sync/audit.
