# A24 completed screen and confirmation decision

Job957_0 COMPLETED exit0:0, runtime56:16, no restart/requeue.
Screen auditor PASS including all frozen manifests, saved predictions,
checkpoint selection, 50-epoch history and live W&B finished state.
This audit recomputes stored predictions, not fresh inference.

Selected epoch43 DEV Macro-F1 .801688234419158, accuracy .8613861386138614,
QWK .6632531555132174. F1 A/B/C/D
[1,.6666666666666666,.9135802469135802,.6265060240963856].
Confusion matrix [[1,0,0,0],[0,25,15,0],[0,10,296,5],[0,0,26,26]].
Epoch50 Macro-F1 .5474088489488576; only5/50 epochs>=.75.
Zero skipped updates. Rare-A sensitivity and D recall26/52 remain concerns.

Gate >=.75 passes. Proceed with folds1--4 full50, same immutable snapshot,
seed42/config/cache/split/checkpoint rule. Preserve original fold0 run957.
No ensemble, no Vesta, exclude worker2, require RTX5090. No claim of
five-fold stability or independent test performance before confirmation.
Acceptance remains mean>=.70, sample SD<=.05, minimum>=.65.

Snapshot /slurmshared/Ngoc/code/hcmus-density-auggeo-dropout30-fp32-20260921-v1
Config SHA256 a2948d41e6c7235eb53098ac2701e19bec855bd40b1027ca7bac0ffdc5483fc6
Split SHA256 43daa86936ee7b1bae1b200836fb1afdfe0c8294c7c865d8f5758bf989f12a9a
W&B https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/ikzls2eb

## Confirmation launch verified

Slurm array958 tasks1--4, no fold0 rerun. All four verified RUNNING at
runtime1:20, each log confirms NVIDIA GeForce RTX5090. Folds1/2 on master,
folds3/4 on worker1, no Vesta/worker2. W&B runs:

- fold1: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/nls020ul
- fold2: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/usyx425t
- fold3: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/lb2y56pt
- fold4: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/n8ejk3n7

No traceback/error found in launch logs. Next metric review after10 epochs.
