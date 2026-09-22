# A39 corrected ordinal-primary common first-20 review

A39 removes A38's collapse but does not solve the hardest fold by epoch 20.

| Fold | Best epoch | Macro-F1 | Accuracy | F1 A/B/C/D | QWK |
|---|---:|---:|---:|---|---:|
| 1 | 5 | 0.541072 | 0.828784 | 0.0000 / 0.6250 / 0.8936 / 0.6457 | 0.663031 |
| 3 | 19 | 0.705370 | 0.834158 | 0.6667 / 0.6829 / 0.8946 / 0.5773 | 0.649215 |

The two-fold mean is 0.623221, sample SD 0.116177 and minimum 0.541072.
Fold 3 now exceeds 0.70, confirming the corrected head can learn a useful
ordinal classifier. Fold 1 remains below A30/A36 and still has F1_A=0, so A39
fails both expansion gates.

Continue unchanged to epoch 50 for audit; do not expand. If final A39 fails,
the controlled roadmap has now tested handcrafted fusion, view-token fusion,
spatial-token fusion and ordinal-primary output. The next major isolated
hypothesis should replace the image backbone while returning to A30's
relational fusion and flat head.

