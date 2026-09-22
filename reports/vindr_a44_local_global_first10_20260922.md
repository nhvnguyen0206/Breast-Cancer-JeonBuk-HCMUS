# A44 fold1: matched first10 against A43

Job1050_1 verified RUNNING on master RTX5090. Histories for both arms contain
complete epochs1--10; select each arm's best DEV Macro-F1 within this same
horizon. Frozen split, seed42 and cache are unchanged.

| Arm | Selected epoch | Macro-F1 | Accuracy | QWK | B/C/D mean F1 | A-positive epochs |
|---|---:|---:|---:|---:|---:|---:|
| A43 | 4 | .5850244052 | .8114143921 | .6936709874 | .7133658737 | 1/10 |
| A44 | 4 | .5418260416 | .7965260546 | .6321601104 | .7224347221 | 0/10 |

A44 selected F1 A/B/C/D: [0,.7323943662,.8634812287,.5714285714].
Confusion matrix (true rows/predicted columns in A/B/C/D order):
[[0,1,0,0],[1,26,12,0],[0,5,253,54],[0,0,9,42]].
A43 selected F1 A/B/C/D: [.2,.5777777778,.8843537415,.6779661017].

A44 has a small B/C/D average gain, but lacks A recovery and loses accuracy
and QWK. Its selected Macro-F1 and QWK fail the registered screen gates;
no expansion is justified. At epoch10 A44 Macro-F1 is .5006176347, QWK
.5597278147, F1 [0,.6913580247,.9001536098,.4109589041]. Initial AMP skip
total9 (A43:8) does not by itself establish an AMP failure; losses remain
finite and the job is progressing.

Continue registered50 unchanged; report at20/40/final and audit before
acceptance/rejection. These selected DEV scores are not independent test
estimates. With one A exam in fold1, A behavior is case-level evidence.
W&B: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/2031sdoy
