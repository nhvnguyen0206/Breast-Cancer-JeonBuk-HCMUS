# A40 ConvNeXt-Tiny two-fold screen: common first 10 epochs

Both job-1022 tasks are healthy on the permitted RTX 5090 node. This is a
matched common-horizon DEV checkpoint, not the final audit and not an
independent test result.

| Fold | Best epoch <=10 | Macro-F1 | Accuracy | QWK | F1 A/B/C/D |
|---|---:|---:|---:|---:|---:|
| 1 | 4 | 0.8126870715 | 0.8560794045 | 0.6873629019 | 1.000000 / 0.655172 / 0.907051 / 0.688525 |
| 3 | 2 | 0.6822455124 | 0.8440594059 | 0.6206403148 | 0.666667 / 0.740741 / 0.904908 / 0.416667 |

The common-first10 mean is **0.7474662919**, sample SD **0.0922361110**, and
minimum **0.6822455124**. The two numerical expansion gates are provisionally
met at this early horizon, but expansion is forbidden until both full
50-epoch runs and read-only audits complete.

At the matched first10 horizon, A30 scored 0.5477628992 on fold 1 and
0.6864294858 on fold 3 (two-fold mean 0.6170961925). A40's improvement comes
almost entirely from fold 1; fold 3 is essentially unchanged. Fold 1 contains
only one class-A case and fold 3 only two, so the high A F1 values cannot be
treated as robust evidence. B/C/D and final cross-fold stability remain the
important checks.

Epoch-10 scores themselves have already fallen to 0.5536474887 and
0.4914785246, showing the same checkpoint-selection sensitivity observed in
earlier arms. Continue unchanged to the preregistered 50 epochs and reassess
at common epoch 20; do not tune or expand now.
