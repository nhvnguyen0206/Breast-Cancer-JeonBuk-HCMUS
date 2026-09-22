# Persistence of the rare-A decision region

This audit uses every completed epoch inside the latest common horizons, not
only the selected DEV checkpoint. A positive A epoch means class-A F1 > 0 as
reconstructed from that epoch's confusion matrix.

| Arm/fold | Horizon | Positive-A epochs | Longest consecutive run | Positive epochs |
|---|---:|---:|---:|---|
| A42 fold 1 | 30 | 1/30 | 1 | 19 |
| A42 fold 3 | 30 | 4/30 | 3 | 1, 2, 3, 7 |
| A43 fold 2 | 20 | 10/20 | 3 | 1, 3, 4, 6, 7, 12, 13, 14, 17, 19 |
| A43 fold 3 | 20 | 4/20 | 1 | 3, 7, 12, 18 |

A42's apparent fold-1 recovery is a single isolated epoch, confirming that its
selected two-fold stability is fragile. A43 is materially different on fold
2: it recovers the single A exam in half of the first 20 epochs, compared with
zero positive-A epochs across all 50 epochs for A40 and A41 fold 2. Thus A43
has established an A decision region rather than producing only one lucky
checkpoint on that fold.

This does not make A43 successful. Its maximum positive-A streak is only three
epochs, fold 3 remains sporadic, and its selected B/C/D mean and QWK trail A41.
The correct interpretation is therefore: multi-scale token fusion repairs the
specific ConvNeXt fold-2 A collapse, but has not yet preserved the substantive
B/C/D representation or demonstrated stable convergence.
