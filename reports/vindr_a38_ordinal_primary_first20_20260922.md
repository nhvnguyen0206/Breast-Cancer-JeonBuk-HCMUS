# A38 ordinal-primary common first-20 review

A38 remains severely collapsed after both folds reach epoch 20.

| Fold | Best epoch | Macro-F1 | Accuracy | F1 A/B/C/D | QWK | Learned gaps |
|---|---:|---:|---:|---|---:|---|
| 1 | 17 | 0.148633 | 0.166253 | 0.0625 / 0.2174 / 0.0615 / 0.2531 | 0.312556 | 1.309 / 1.370 |
| 3 | 20 | 0.172726 | 0.195545 | 0.0909 / 0.2083 / 0.1201 / 0.2715 | 0.344395 | 1.370 / 1.433 |

The two-fold mean is 0.160679, sample SD 0.017036 and minimum 0.148633.
Threshold gaps are expanding from 1.0, but only reach approximately 1.31–1.43
by the selected checkpoints. This is too slow and remains around the theoretical
`2*log(2) ~= 1.386` boundary where interior classes first gain an argmax region.
Confusion matrices still send most B/C cases to A/D.

A38 fails decisively and must not expand. Continue unchanged to epoch 50 for
audit. A39's preregistered spacing 2.0 directly fixes the demonstrated
initialization defect and already passes an explicit A/B/C/D argmax test.

