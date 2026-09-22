# A38 ordinal-primary common first-10 review

Both folds reached epoch 10 normally. The monotonic head is numerically stable
but performs catastrophically at this horizon.

| Fold | Best epoch | Macro-F1 | Accuracy | F1 A/B/C/D | QWK |
|---|---:|---:|---:|---|---:|
| 1 | 9 | 0.119022 | 0.148883 | 0.0606 / 0.1364 / 0.0315 / 0.2476 | 0.271153 |
| 3 | 9 | 0.112995 | 0.175743 | 0.0755 / 0.0000 / 0.1021 / 0.2744 | 0.355928 |

The two-fold mean is 0.116009, sample SD 0.004262 and minimum 0.112995.
Unlike the flat head, A38 predicts class A, but sends most B/C cases to the
extreme classes A/D.

This exposes a structural initialization defect. With initial threshold gaps
of 1, the maximum attainable probability of an interior class is only about
0.245, while an extreme class remains larger at the same score. Thus B/C have
no useful argmax region initially. At selected checkpoints the gaps have only
expanded to roughly 1.16–1.24, which is still insufficient.

Continue unchanged to common epoch 20 to test whether learned gaps expand
enough; do not expand A38. Prepare a corrected ordinal head whose initialization
is explicitly tested to give all four classes a nonempty argmax interval.

