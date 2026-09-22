# A32 fold-0 first-20 review

Job `987_0` remained RUNNING on permitted RTX 5090 hardware. All first-20
training losses are finite. This is selected DEV, not a completed screen or
independent test.

The best checkpoint remains epoch 4: Macro-F1 **0.7771719287**, accuracy
**0.7871287129**, QWK **0.6339685642**, class F1 A/B/C/D
**1.000000 / 0.607143 / 0.851138 / 0.650407**, one severe error, and mean
B/C/D F1 0.702896. Epoch 20 itself has Macro-F1 0.5048624758.

A32 remains above the 0.70 expansion gate but found no improvement after
epoch 4. Its matched-horizon Macro-F1 exceeds A30 0.702595, while A6 reaches
0.782979 with higher accuracy and QWK. The numerical pass remains sensitive
to one class-A case. Continue unchanged through epoch 50; do not launch
folds 1–4 before completed audit. Next review at epoch 40.
