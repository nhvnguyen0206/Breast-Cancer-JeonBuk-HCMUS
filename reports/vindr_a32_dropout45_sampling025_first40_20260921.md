# A32 fold-0 first-40 review

Job `987_0` remained RUNNING on permitted RTX 5090 hardware. All first-40
training losses are finite. This is selected DEV, not a completed screen or
independent test.

The best checkpoint remains epoch 4: Macro-F1 **0.7771719287**, accuracy
**0.7871287129**, QWK **0.6339685642**, class F1 A/B/C/D
**1.000000 / 0.607143 / 0.851138 / 0.650407**, one severe error, and mean
B/C/D F1 0.702896. Epoch 40 itself has Macro-F1 0.5048510886.

A32 remains above the 0.70 numerical expansion gate but has not improved
since epoch 4. A6 is still slightly higher at the matched horizon
(0.782979) with better accuracy and QWK. The large selected-versus-epoch40
gap and single-A sensitivity prevent an early stability claim. Continue
unchanged through epoch 50 and audit before submitting folds 1–4.
