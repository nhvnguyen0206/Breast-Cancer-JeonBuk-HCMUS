# A15 warm-up5 — completed fold-0 screen audit

The audit passes. Job905_0 completed all 50 epochs on
`slurm-b20a-master-0` (RTX5090) with ExitCode0:0, no restart or requeue.
All scalar training losses are finite, the best checkpoint exists, prediction
membership/labels/probabilities/argmax and recomputed metrics agree, all frozen
fold manifests validate, and W&B run `cjdw2zo6` is finished. History separately
proves epochs1--5 frozen and epochs6--50 unfrozen exactly.

Selected DEV checkpoint epoch26: Macro-F1 0.7145881415028787, accuracy
0.8539603960396039, QWK 0.6663867428059568, class F1
[0.6666666666666666, 0.6301369863013698, 0.909375,
0.6521739130434783], no severe errors. Confusion matrix:
[[1,0,0,0],[1,23,16,0],[0,10,291,10],[0,0,22,30]].

Epoch50 Macro-F1 is 0.5404630542519797, accuracy 0.8465346534653465,
QWK 0.620432469935245, class F1
[0, 0.6753246753246753, 0.9051321928460342, 0.5813953488372093]. No epoch
reached 0.75 and total AMP-skipped updates are 15.

A15 fails the preregistered 0.75 expansion gate and is rejected. Do not submit
folds1--4. The score is selected on DEV, not an independent test result, and
class-A evidence is limited to one fold-0 case.

W&B: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/cjdw2zo6
