# A30 completed screen: rejected for confirmation

Job981_0 COMPLETED ExitCode0:0, 50 epochs, runtime55:42, master node,
worker2 excluded. Immutable snapshot:
/slurmshared/Ngoc/code/hcmus-density-auggeo-dropout40-sampling025-20260921-v1.
Screen auditor PASS: saved predictions/checkpoint provenance/metrics and
all frozen fold manifests validated; W&B u5g2ni5n finished.
Assignment SHA256:
43daa86936ee7b1bae1b200836fb1afdfe0c8294c7c865d8f5758bf989f12a9a.

Selected DEV best epoch11 Macro-F1 .7025951908901428;
accuracy .8391089108910891; QWK .6494927923117992.
F1 A/B/C/D [.6666666666666666,.5783132530120482,.8987341772151899,.6666666666666666].
Epoch50 Macro-F1 .5172346846067319, accuracy .8267326732673267,
QWK .5925168564164915; F1 [0,.625,.8944881889763779,.5494505494505495].
Zero epochs >=.75; 17 AMP skipped updates total.
Maximum probability-sum error 1.311183268626337e-07.

Decision: fails fixed screen gate .75; do not submit folds1–4 or adopt
increased dropout. Not a five-fold success despite selected fold0 >.70.
Parent A6 selected fold0 .782979257528481; no evidence of improvement.
All scores selected tuning DEV, not independent test. The six total A
cases remain a major limitation. Retain all artifacts, no resplit/restart.

W&B: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/u5g2ni5n
