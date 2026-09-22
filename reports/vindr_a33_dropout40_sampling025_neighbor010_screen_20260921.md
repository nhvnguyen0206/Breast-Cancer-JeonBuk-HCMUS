# A33 completed fold-0 screen

A33 changes only neighbor loss 0.20 -> 0.10 relative to A30. Job `992_0`
completed all 50 epochs on `slurm-b20a-master-0` with RTX 5090, exit code
0:0, no restart/requeue, and worker2/Vesta excluded.

The read-only screen audit passed; assignment SHA256 remained
`43daa86936ee7b1bae1b200836fb1afdfe0c8294c7c865d8f5758bf989f12a9a`,
checkpoint/predictions/config agree, and W&B is `finished`.

Selected epoch 2: Macro-F1 **0.8159754728**, accuracy **0.8341584158**,
QWK **0.6912124389**, class F1 A/B/C/D
**1.000000 / 0.678899 / 0.887755 / 0.697248**, mean B/C/D F1 0.754634,
and one severe error. Epoch 50 Macro-F1 is 0.5294743044.

A33 passes the 0.70 expansion gate with substantive B/C/D performance.
Preserve this exact fold-0 result and launch folds 1–4 from the identical
immutable snapshot/config. Do not rerun fold 0. Full acceptance still
requires CV5 mean >=0.70, sample SD <=0.05, and minimum >=0.65. This remains
selected DEV, not independent test evidence; only six class-A cases exist.

W&B: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/x6422mve

