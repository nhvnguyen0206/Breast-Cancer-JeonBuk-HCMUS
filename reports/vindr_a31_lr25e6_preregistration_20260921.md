# A31 preregistration

Parent immutable A6. Only learning change: global LR5e-5 ->2.5e-5.
Rationale and negative prior evidence: vindr_post_a30_next_step_20260921.md.
Retain architecture, sampling.25, dropout.3, augmentation, losses, seed42,
cache and frozen grouped split. No ensemble. Hypothesis only, no promise.

Deploy by cloning immutable A6, adding only new config; verify parsed delta,
source/script/split byte parity and run snapshot tests before submission.
Fixed fold0 full50 on RTX5090 only, exclude worker2, never Vesta.
Report scores at10–20 epoch intervals, not each epoch.
Expand folds1–4 only after completed audit and selected DEV>=.70, preserving
original fold0. Joint final mean>=.70, sampleSD<=.05, minimum>=.65;
aspiration mean>=.75. DEV is not independent-test evidence; six A cases
limit conclusions. No job submitted at preregistration.

The screen gate was amended from .75 to .70 before A31 submission, following
the user's documented goal-threshold revision. The treatment, frozen split,
and final stability criteria are unchanged.

## Submission

Preflight repeated before submission: semantic config delta contained only
the arm name and learning rate 5e-5 -> 2.5e-5; `src/` and `scripts/` were
byte-identical to immutable A6; assignment SHA256 remained
`43daa86936ee7b1bae1b200836fb1afdfe0c8294c7c865d8f5758bf989f12a9a`;
16/16 snapshot tests passed. Config SHA256 is
`1248909bb75aa8ab3d6f691f8d14c9750a5a47244f18c1a09c0cc9d985f350da`.

Submitted fold 0 only as job `986_0`. Startup verification: RUNNING on
`slurm-b20a-master-0`, allocated GPU `NVIDIA GeForce RTX 5090`, worker2/Vesta
excluded, no requeue or restart. W&B run:
https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/9v7h7cr0
