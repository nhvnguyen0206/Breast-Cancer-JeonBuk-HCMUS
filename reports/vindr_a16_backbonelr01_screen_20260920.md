# A16 backbone-LR 0.1 — completed fold-0 screen audit

The audit passes. Job906_0 completed all 50 epochs on
`slurm-b20a-master-0` (RTX5090) with ExitCode0:0, no restart or requeue.
All scalar training losses are finite, the best checkpoint exists, prediction
membership/labels/probabilities/argmax and recomputed metrics agree, all frozen
fold manifests validate, and W&B run `en6zi94h` is finished. The DenseNet
backbone remained trainable throughout and used 0.1 times the fusion/head LR.

Selected DEV checkpoint epoch20: Macro-F1 0.6647013473177328, accuracy
0.8292079207920792, QWK 0.6636583011583012, class F1
[0.5, 0.6206896551724138, 0.8910569105691057, 0.6470588235294118], no
severe errors. Confusion matrix:
[[1,0,0,0],[2,27,11,0],[0,20,274,17],[0,0,19,33]].

Epoch50 Macro-F1 is 0.5668188358910276, accuracy 0.8143564356435643,
QWK 0.649435394298408, class F1
[0.2222222222222222, 0.5952380952380952, 0.8906752411575563,
0.5591397849462365]. No epoch reached 0.75 and total AMP-skipped updates are
20.

A16 fails the preregistered 0.75 expansion gate and is rejected. Do not submit
folds1--4. The score is selected on DEV, not an independent test result, and
class-A evidence is limited to one fold-0 case.

W&B: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/en6zi94h
