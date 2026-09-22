# A9 completed CV5: dropout 0.5

A9 changed only model dropout from 0.3 to 0.5 relative to substantive best A5.
Shared DenseNet121, hierarchical fusion, augmentation, LR 5e-5, AdamW weight
decay 1e-4, losses, natural sampling, seed42 and the frozen split were
unchanged. Inference uses one flat-head checkpoint; no ensemble.

Fold0 job790 and confirmation array791 folds1--4 all completed 50 epochs.
Scheduler records report COMPLETED with ExitCode 0:0; folds0--2 ran on master,
folds3--4 on worker1, worker2 was excluded, and RTX 5090 startup was verified.
No confirmation task restarted or requeued.

The full read-only audit PASS: common architecture/config, checkpoint/history,
all frozen manifests and assignment hash, exact DEV prediction membership and
labels, normalized probabilities/argmax, independently recomputed metrics,
2017-case union, and all five source W&B runs finished50.

| Fold | Best epoch | DEV Macro-F1 |
|---|---:|---:|
| 0 | 18 | 0.7983834791 |
| 1 | 28 | 0.5569145775 |
| 2 | 19 | 0.7578714628 |
| 3 | 34 | 0.6431991883 |
| 4 | 25 | 0.6046581573 |

Mean Macro-F1 **0.6722053730**, sample SD **0.1024152650**. Accuracy
0.8225032553 +/- 0.0109967438; QWK 0.6314935199 +/- 0.0304188602. Mean class
F1 A/B/C/D = 0.6163636364 / 0.6115190727 / 0.8901661405 / 0.5707726425;
BCD mean 0.6908192852. Epoch50 mean Macro-F1 0.5354832714 +/- 0.0444662842.
Support remains 6/196/1556/259. All selected checkpoints have zero severe
errors; the pooled selected confusion matrix is
`[[5,1,0,0],[13,124,59,0],[0,83,1395,78],[0,0,124,135]]`.

A9 is 3.0623 percentage points below A5 (0.7028282801). Stronger dropout
improved fixed fold0 by 0.8734 points but reduced B and D discrimination and
did not generalize across folds. The 0.75 CV5 target is not met. These are
selected DEV results, not independent-test evidence, and no multi-seed
success is claimed. A5 remains the best substantive completed arm.

The result rejects dropout 0.5 as the next base. The next controlled screen
should return to A5 and target adjacent B/C and C/D boundary errors with one
factor only, without changing the split or architecture. Class A has only six
cases and must not drive that decision.
