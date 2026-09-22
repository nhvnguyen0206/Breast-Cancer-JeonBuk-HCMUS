# A7 completed CV5: configured weight decay is a no-op

A7 was intended to change only AdamW weight decay from 1e-4 to 5e-4
relative to A5. Shared DenseNet121, hierarchical fusion, augmentation,
dropout 0.3, losses, LR 5e-5, natural sampling, seed42 and the frozen split
were unchanged. Inference uses one flat-head checkpoint; no ensemble.

Fold0 job780 and confirmation array781 folds1--4 all completed 50 epochs.
Scheduler records report COMPLETED with ExitCode 0:0; folds1/2 ran on master,
folds3/4 on worker1, and worker2 was excluded. RTX 5090 startup was verified.

The full read-only audit PASS: common architecture/config, checkpoint/history,
all frozen manifests and assignment hash, exact DEV prediction membership and
labels, normalized probabilities/argmax, independently recomputed metrics,
2017-case union, and all five source W&B runs finished50.

| Fold | Best epoch | DEV Macro-F1 |
|---|---:|---:|
| 0 | 30 | 0.7896498562 |
| 1 | 8 | 0.5792311841 |
| 2 | 5 | 0.7991001000 |
| 3 | 3 | 0.5701863354 |
| 4 | 27 | 0.7759739248 |

Mean Macro-F1 **0.7028282801**, sample SD **0.1172888127**. Accuracy
0.8373756234 ± 0.0258578896; QWK 0.6707563558 ± 0.0326389085. Mean class
F1 A/B/C/D = 0.6000000000 / 0.6818263058 / 0.8937691979 / 0.6357176166;
BCD mean 0.7371043734. Epoch50 mean Macro-F1 0.5598344538 ± 0.1078510234.
Support remains 6/196/1556/259.

Every completed history metric, logged train scalar and selected checkpoint
state tensor is identical to A5. Runtime arithmetic confirms both configured
decay factors round to 1.0 in float32 at LR 5e-5. A7 is therefore a no-op
replication, not evidence against effective weight decay. The target 0.75 is
not met; these are selected DEV results, not an independent test, and no
multi-seed success is claimed. A5 remains the best substantive completed arm.

The next controlled fixed-fold0 screen should use a materially effective
weight decay such as 1e-2 while keeping every other A5 factor fixed.
