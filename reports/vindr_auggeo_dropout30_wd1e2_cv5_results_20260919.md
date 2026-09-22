# A8 completed CV5: effective AdamW weight decay

A8 changed only AdamW weight decay from 1e-4 to 1e-2 relative to A5.
Shared DenseNet121, hierarchical fusion, augmentation, dropout 0.3, losses,
LR 5e-5, natural sampling, seed42 and the frozen split were unchanged.
Inference uses one flat-head checkpoint; no ensemble.

Fold0 job785 and confirmation array786 folds1--4 all completed 50 epochs.
Scheduler records report COMPLETED with ExitCode 0:0; folds0--2 ran on master,
folds3--4 on worker1, worker2 was excluded, and RTX 5090 startup was verified.
No task restarted or requeued.

The full read-only audit PASS: common architecture/config, checkpoint/history,
all frozen manifests and assignment hash, exact DEV prediction membership and
labels, normalized probabilities/argmax, independently recomputed metrics,
2017-case union, and all five source W&B runs finished50.

| Fold | Best epoch | DEV Macro-F1 |
|---|---:|---:|
| 0 | 29 | 0.8050193050 |
| 1 | 15 | 0.5685669490 |
| 2 | 42 | 0.7817985393 |
| 3 | 18 | 0.7093373275 |
| 4 | 32 | 0.6253638411 |

Mean Macro-F1 **0.6980171924**, sample SD **0.1007878795**. Accuracy
0.8413409331 +/- 0.0206055967; QWK 0.6449785726 +/- 0.0347083833. Mean class
F1 A/B/C/D = 0.6333333333 / 0.6620012689 / 0.9001940430 / 0.5965401243;
BCD mean 0.7195784787. Epoch50 mean Macro-F1 0.5251450156 +/- 0.0233859501.
Support remains 6/196/1556/259, and all selected predictions have zero
severe errors.

A8 is 0.4801 percentage points below substantive best A5 (0.7028282801),
despite improving fixed fold0 by 1.5369 points and fold2 reaching 0.7818.
The stronger decay reduced cross-fold SD but weakened B/D mean F1 and did not
generalize the fold0 gain. The 0.75 CV5 target is not met. These are selected
DEV results, not independent-test evidence, and no multi-seed success is
claimed. A5 remains the best substantive completed arm.

The pooled confusion matrix is `[[4,2,0,0],[2,121,73,0],
[0,46,1426,84],[0,0,113,146]]`. The remaining error is overwhelmingly
adjacent B<->C and C<->D confusion; class A has only six cases and must not
drive the next decision. A controlled next screen should target the B/D
boundaries without changing the architecture or split.
