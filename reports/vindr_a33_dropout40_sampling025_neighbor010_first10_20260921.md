# A33 fold-0 first-10 review

Job `992_0` remained RUNNING on permitted RTX 5090 hardware. The first ten
epochs have finite training losses. This is selected DEV, not a completed
screen or independent test, and no confirmation folds are authorized yet.

Best first-10 checkpoint is epoch 2: Macro-F1 **0.8159754728**, accuracy
**0.8341584158**, QWK **0.6912124389**, class F1 A/B/C/D
**1.000000 / 0.678899 / 0.887755 / 0.697248**, one severe error, and mean
B/C/D F1 **0.754634**. Epoch 10 itself remains above the gate at Macro-F1
0.7293753630 but with lower accuracy/QWK and D F1.

A33 provisionally exceeds the 0.70 screen gate and improves all substantive
fold-0 metrics versus A30 first10 and A25 first10; the gain is not confined
to the single A case. It is still one repeatedly used DEV fold, so continue
the unchanged run through all 50 epochs and audit before expanding folds
1–4. Next review at epoch 20.
