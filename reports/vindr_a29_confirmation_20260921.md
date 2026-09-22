# A29 confirmation launch

Screen job976_0 COMPLETED exit0, 50 epochs; read-only screen audit PASS,
including saved predictions, selected checkpoint provenance, all frozen fold
manifests and live W&B finished status. Audit is not a fresh inference replay.
Selected DEV Macro-F1 .810309343483078 at epoch32 exceeds .75 gate.
Epoch50 Macro-F1 .7769489913842917; 12 epochs >=.75; 17 AMP skipped updates.
See vindr_a29_screen_audit_20260921.json for full evidence.

Submitted job977 with array1–4 only, same immutable snapshot/config:
/slurmshared/Ngoc/code/hcmus-density-auggeo-dropout30-brightness080-20260921-v1
configs/vindr_density_auggeo_dropout30_brightness080.yaml
Config SHA256 b4be21b0db70a9ca2797a9e54ecb826d9971ec7b9a73eca030b0119ca4230182
rechecked before submission. Queue empty before launch; no duplicate A29 jobs.
Launcher asserts RTX5090 and excludes worker2; no Vesta.

Preserve original976fold0 and combine only with977folds1–4 for final audit.
Seed42, frozen split and 50 epochs unchanged; fresh ImageNet initialization
per fold, no ensemble. All scores remain selected DEV, not independent test.
Final acceptance remains mean>=.70, sampleSD<=.05, min>=.65;
aspiration mean>=.75. Single-fold screen is not evidence of stability.

## Runtime verification

All four tasks verified RUNNING at elapsed44–45 seconds. Launch logs for
each explicitly report NVIDIA GeForce RTX5090. Folds1–2 on master,
folds3–4 on worker1, no Vesta. W&B run metadata:

- Fold1: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/9ccnqsma
- Fold2: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/lsc7p8qx
- Fold3: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/odv5s2u8
- Fold4: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/zxt9c2zp

No completed epoch histories at this initial check. Next score review at
10–20 completed epochs, not per epoch.
