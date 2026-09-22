# A33 fold-0 first-20 review

Job `992_0` remained RUNNING on permitted RTX 5090 hardware. All first-20
training losses are finite. This is selected DEV, not a completed screen or
independent test.

The best checkpoint remains epoch 2: Macro-F1 **0.8159754728**, accuracy
**0.8341584158**, QWK **0.6912124389**, class F1 A/B/C/D
**1.000000 / 0.678899 / 0.887755 / 0.697248**, one severe error, and mean
B/C/D F1 0.754634. Epoch 20 itself also exceeds the 0.70 gate at Macro-F1
**0.7511291598**, although D F1 falls to 0.519481.

A33 still exceeds A30 and A25 at the matched first-20 horizon. More than one
checkpoint clears the gate, but this remains one repeatedly used DEV fold.
Continue unchanged through all 50 epochs and audit before expanding folds
1–4. Next review at epoch 40.
