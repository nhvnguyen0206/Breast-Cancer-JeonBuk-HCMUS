# A33 completed CV5: lower neighbor loss on A30

A33 changes only neighbor-loss weight 0.20 -> 0.10 relative to A30. Fold 0
comes from job 992 and folds 1–4 from job 993. Every fold completed 50 epochs
with exit code 0 on permitted RTX 5090 nodes; worker2/Vesta was not used.

The read-only audit passed for the frozen split, all 2,017 unique studies,
configuration and architecture provenance, saved best checkpoints,
predictions, probability sums, recomputed metrics, and five finished W&B
runs. The assignment SHA256 remains
`43daa86936ee7b1bae1b200836fb1afdfe0c8294c7c865d8f5758bf989f12a9a`.

| Fold | Best epoch | Macro-F1 | Accuracy | QWK | F1 A/B/C/D |
|---|---:|---:|---:|---:|---:|
| 0 | 2 | 0.815975 | 0.834158 | 0.691212 | 1.000000 / 0.678899 / 0.887755 / 0.697248 |
| 1 | 2 | 0.545568 | 0.784119 | 0.657378 | 0.142857 / 0.509091 / 0.870748 / 0.659574 |
| 2 | 22 | 0.619445 | 0.806452 | 0.586667 | 0.500000 / 0.626506 / 0.879365 / 0.471910 |
| 3 | 33 | 0.670448 | 0.829208 | 0.586164 | 0.666667 / 0.597015 / 0.895385 / 0.522727 |
| 4 | 22 | 0.650992 | 0.799007 | 0.550316 | 0.666667 / 0.588235 / 0.873817 / 0.475248 |

Selected-fold mean Macro-F1 is **0.6604856963**, sample SD
**0.0990667973**, and minimum **0.5455677048**. Mean accuracy is
0.8105889001, mean QWK is 0.6143473649, and mean class F1 A/B/C/D is
0.595238/0.599949/0.881414/0.565341. Mean epoch-50 Macro-F1 is 0.5204241921.

A33 fails all registered gates: mean >=0.70, sample SD <=0.05, and minimum
fold >=0.65. It is rejected. Lowering neighbor loss worsened both mean and
dispersion relative to A30 and did not generalize the favorable fold-0
screen. These are repeatedly selected DEV estimates, not independent-test
results; class A has only six cases.

Audited W&B summary:
https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/hrrvh977
