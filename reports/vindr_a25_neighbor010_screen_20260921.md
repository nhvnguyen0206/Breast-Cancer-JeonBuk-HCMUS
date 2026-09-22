# A25 completed screen: reject expansion

Job962_0 COMPLETED50, ExitCode0:0, runtime55:46, Requeue0/Restarts0,
master RTX5090; worker2/Vesta excluded. W&B vjgvwnx6 verified finished.
Read-only screen audit PASS: all five manifests, checkpoint/history selection,
saved prediction membership/argmax/recomputed metrics and live W&B agree.
Audit does not rerun inference. Assignment SHA256 remains
43daa86936ee7b1bae1b200836fb1afdfe0c8294c7c865d8f5758bf989f12a9a.

Selected epoch4 Macro-F1 .706347382145964, accuracy .801980198019802,
QWK .6636976608673937; F1 A/B/C/D
[.6666666666666666,.6016260162601627,.8640275387263339,.693069306930693].
Confusion [[1,0,0,0],[1,37,2,0],[0,46,251,14],[0,0,17,35]], severe0.
Epoch50 Macro .49749756816421153, accuracy .8168316831683168,
QWK .5592640641585093; F1 [0,.5866666666666667,.8864696734059098,
.5168539325842697]. Confusion [[0,1,0,0],[0,22,18,0],[0,12,285,14],
[0,0,29,23]], severe0. AMP skips16; zero/50 checkpoints>=.75.
Maximum saved probability-sum error1.2364762369543314e-7.

Reject A25 without folds1–4: below .75 screen gate and A5 screen .7896498562.
This rules out this candidate under the registered screening procedure, not
every possible benefit of changing neighbor loss. Retain A5/A6 references;
no successful stable CV5 claim. Selected DEV is not independent test.

W&B: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/vjgvwnx6
