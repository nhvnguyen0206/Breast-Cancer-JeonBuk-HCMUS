# A32 fold-0 first-10 review

Job `987_0` remained RUNNING on permitted RTX 5090 hardware. The first ten
epochs have finite training losses. This is selected DEV, not a completed
screen or independent test, and no confirmation folds are authorized yet.

Best first-10 checkpoint is epoch 4: Macro-F1 **0.7771719287**, accuracy
**0.7871287129**, QWK **0.6339685642**, class F1 A/B/C/D
**1.000000 / 0.607143 / 0.851138 / 0.650407**, and one severe error. Mean
B/C/D F1 is 0.702896. Epoch 10 itself has Macro-F1 0.4696391043.

A32 exceeds the 0.70 numerical screen gate provisionally and is 0.187526
above A30 at the matched first-10 horizon, but the gain is sensitive to the
single fold-0 class-A case. A6 reached 0.782979 at the same horizon with
higher accuracy and QWK. Continue unchanged through all 50 epochs and audit
before deciding whether to expand folds 1–4. Next review at epoch 20.
