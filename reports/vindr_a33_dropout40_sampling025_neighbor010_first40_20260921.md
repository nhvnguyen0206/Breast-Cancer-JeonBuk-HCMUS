# A33 fold-0 first-40 review

Job `992_0` remained RUNNING on permitted RTX 5090 hardware. All first-40
training losses are finite. This is selected DEV, not a completed screen or
independent test.

The best checkpoint remains epoch 2: Macro-F1 **0.8159754728**, accuracy
**0.8341584158**, QWK **0.6912124389**, class F1 A/B/C/D
**1.000000 / 0.678899 / 0.887755 / 0.697248**, one severe error, and mean
B/C/D F1 0.754634. Epoch 40 has Macro-F1 0.5303476721.

A33 remains well above the 0.70 numerical gate and stronger than A30/A25 at
the matched horizon, but no checkpoint after epoch 2 improves the selected
score and the selected-versus-epoch40 gap is large. Complete all 50 epochs
and audit before expanding folds 1–4; do not infer CV stability from fold 0.
