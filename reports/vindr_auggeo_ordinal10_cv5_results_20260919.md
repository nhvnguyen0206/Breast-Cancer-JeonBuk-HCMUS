# A4: geometric augmentation + ordinal coefficient 0.1

Selected DEV results, fixed density-grouped CV5 seed42 and training seed42.
Only ordinal coefficient differs from A1 (0.5 -> 0.1). Architecture and
single-checkpoint flat-head inference unchanged; no ensemble.

All folds completed 50 epochs. Audit PASS: checkpoint/history, frozen manifests,
prediction membership and labels, probability/argmax consistency, recomputed
metrics, finished W&B runs. Unique cases: 2017; A/B/C/D = 6/196/1556/259.
Confirmation tasks 766_1--4 verified COMPLETED exit 0, RTX5090 startup,
master/worker-1 allocation and worker-2 excluded. Fold0 completion evidence
is documented in the ledger; its Slurm record expired before final audit.

| Fold | Best epoch | DEV Macro-F1 |
|---|---:|---:|
| 0 | 32 | 0.795153 |
| 1 | 5 | 0.575086 |
| 2 | 15 | 0.697160 |
| 3 | 2 | 0.560221 |
| 4 | 32 | 0.635454 |

Mean Macro-F1: 0.6526148621; sample SD: 0.0963631584.
Mean accuracy: 0.8423347173; mean QWK: 0.6560994858.
Mean F1 A/B/C/D: 0.433333 / 0.685194 / 0.900582 / 0.591350.
B/C/D mean: 0.7257087050. Epoch-50 mean Macro-F1: 0.5156552271.

A4 is below A1 (0.6799754745) by 2.736 percentage points, although B/C/D
mean is higher than A1 (0.7021895215). The rare A class has only six cases;
neither improvement nor deterioration there alone establishes robust benefit.
Target not met; do not expand A4 to multiple seeds as a success candidate.
These are DEV-selected checkpoints, not an independent test estimate.
