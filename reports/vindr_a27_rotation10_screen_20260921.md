# A27 completed screen — rejected

Slurm964_0 COMPLETED ExitCode0:0, runtime56:06, no restart/requeue.
Registered master RTX5090 run; worker2 excluded. Completed50 history entries.
audit_density_screen.py from immutable backbonelr01 snapshot exited0/PASS:
checkpoint/saved predictions/history consistent, all frozen fold manifests
validated, assignment SHA256
43daa86936ee7b1bae1b200836fb1afdfe0c8294c7c865d8f5758bf989f12a9a.
Maximum probability-sum error1.3338285498321056e-7.
W&B API state finished:
https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/wjz7dz8t.

Selected epoch16,404 DEV studies:
- Macro-F1 .6751496226906062; accuracy .7995049504950495.
- QWK .6115753489697084.
- F1 A/B/C/D [.6666666666666666,.6095238095238096,.8688524590163934,.5555555555555556].
- Confusion rows A/B/C/D [[1,0,0,0],[1,32,7,0],[0,33,265,13],[0,0,27,25]].
- Severe errors0.

Epoch50 Macro-F1 .5332049653816215, accuracy .8366336633663366,
QWK .6343390016456392; F1 [0,.6428571428571429,.8990536277602523,.5909090909090909].
Confusion [[0,1,0,0],[1,27,12,0],[0,16,285,10],[0,0,26,26]],severe0.
17 cumulative AMP skipped updates;zero/50 epochs reached .75.

Decision: reject rotation10 treatment; no folds1–4. A5 selected fold0
.7896498561536562 is higher. Do not deploy this candidate as a model
improvement. Mask-retention preflight passing was not evidence of accuracy
benefit. Only one A DEV study; no cross-fold stability inference from this
screen. Repeatedly selected DEV is not independent test. No next job launched.
