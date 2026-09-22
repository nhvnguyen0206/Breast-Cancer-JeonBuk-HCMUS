# A32 completed fold-0 screen

A32 changes only dropout 0.40 -> 0.45 relative to A30. Job `987_0`
completed all 50 epochs on `slurm-b20a-master-0` with RTX 5090, exit code
0:0, no restart/requeue, and worker2/Vesta excluded.

The read-only screen audit passed; frozen assignment SHA256 remained
`43daa86936ee7b1bae1b200836fb1afdfe0c8294c7c865d8f5758bf989f12a9a`,
checkpoint/predictions/config agree, and W&B is `finished`.

Selected epoch 4: Macro-F1 **0.7771719287**, accuracy **0.7871287129**,
QWK **0.6339685642**, class F1 A/B/C/D
**1.000000 / 0.607143 / 0.851138 / 0.650407**, mean B/C/D F1 0.702896,
and one severe error. Epoch 50 Macro-F1 is 0.5180146711.

A32 passes the amended 0.70 numerical expansion gate. Preserve this exact
fold-0 result and launch folds 1–4 from the identical immutable snapshot and
config. Do not rerun fold 0. Full acceptance still requires CV5 mean >=0.70,
sample SD <=0.05, and minimum >=0.65. This is selected DEV, not independent
test evidence; the fold-0 score is sensitive to one class-A case.

W&B: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/4fyhjmkw

