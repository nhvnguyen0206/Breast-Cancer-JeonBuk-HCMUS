# A26 completed screen — rejected

Verified on 2026-09-21 using Slurm job963_0 and audit_density_screen.py
from immutable backbonelr01 snapshot. Job COMPLETED, ExitCode0:0,
runtime55:28, no restart/requeue; master RTX5090 deployment, worker2 excluded.
Run: /slurmshared/Ngoc/runs/hcmus-density-cv5-v1-963-fold0.
W&B: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/hpzf3sq6
(API state finished).

Audit PASS: 50 epochs, selected checkpoint/saved predictions consistent,
all fold manifests valid; assignment SHA256
43daa86936ee7b1bae1b200836fb1afdfe0c8294c7c865d8f5758bf989f12a9a.
Maximum probability sum error 1.2759096534864511e-7.

Selected DEV epoch23,404 studies:
- Macro-F1 .7467283693843594; accuracy .7797029702970297.
- QWK .5878118121790169.
- F1 A/B/C/D: [1,.56,.8519134775374376,.575].
- Confusion (rows true A/B/C/D): [[1,0,0,0],[0,35,5,0],[0,50,256,5],[0,0,29,23]].
- Severe errors0. BCD-only descriptive mean .6623044925124792.

Epoch50 Macro-F1 .5070203258567435, accuracy .8094059405940595,
QWK .5847837693539776; F1 [0,.5842696629213483,.8785942492012779,.5652173913043478].
17 AMP skipped updates; zero epochs reached .75.

Decision: no folds1–4. Strict screening gate is not met; rounding to75%
would be incorrect. Compared with A5 screen .7896498561536562, this
normalization treatment does not improve the selected four-class metric.
Perfect A F1 reflects only one DEV study, not robust minority performance.
50 C->B and29 D->C errors indicate remaining B/C/D confusion; these counts
alone do not establish a causal mechanism. Selected DEV is not independent
test evidence. No CV5 stability inference is possible from this screen.
Keep default binary normalization unchanged; no next arm submitted.
