# A17 sampling power 0.10 — completed fold-0 screen audit

The audit passes. Job907_0 completed all 50 epochs on
`slurm-b20a-master-0` (RTX5090) with ExitCode0:0, no restart or requeue.
All scalar training losses are finite, the best checkpoint exists, prediction
membership/labels/probabilities/argmax and recomputed metrics agree, all frozen
fold manifests validate, and W&B run `djz4e32c` is finished.

Selected DEV checkpoint epoch17: Macro-F1 0.7914694342156339, accuracy
0.8267326732673267, QWK 0.6559945504087192, class F1
`[1.0,0.6285714285714286,0.8856209150326797,0.651685393258427]`, no severe
errors. Confusion matrix:
`[[1,0,0,0],[0,33,7,0],[0,32,271,8],[0,0,23,29]]`.

Epoch50 Macro-F1 is 0.5301002143664046. Twelve of 50 checkpoints reach 0.75
or higher; total AMP-skipped updates are 18. The selected score exceeds A5
fold0 by 0.0018195780619777 and its B/C/D mean is also slightly higher, though
the fold contains only one A case.

A17 passes the preregistered 0.75 expansion gate. Retain this completed fold0
and launch fresh folds1--4 from the identical immutable snapshot. This remains
DEV-based model selection and is not an independent test result.

W&B: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/djz4e32c
