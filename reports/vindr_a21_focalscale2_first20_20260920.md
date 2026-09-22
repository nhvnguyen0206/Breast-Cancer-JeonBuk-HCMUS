# A21 focal-scale 2 — first 20 epochs

The selected checkpoint remains epoch 6 at Macro-F1 `0.550700`; no improvement
occurred in epochs 11–20 and epoch 20 is `0.513724`. There are no checkpoints
at or above `0.75`.

A5 reaches `0.765442` at the matched horizon. A21 therefore provides no
evidence that doubling the focal contribution improves the primary result.
Continue the preregistered fold0 run unchanged to 50 epochs; do not launch
confirmation folds. Next review at epoch 30.
