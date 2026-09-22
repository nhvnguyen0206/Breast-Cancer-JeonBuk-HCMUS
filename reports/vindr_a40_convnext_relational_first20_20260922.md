# A40 ConvNeXt-Tiny two-fold screen: common first 20 epochs

Both job-1022 tasks remain healthy on the permitted RTX 5090 node. Restricting
both histories to the same first-20 horizon leaves the selected checkpoints
unchanged from first10.

| Fold | Best epoch <=20 | Macro-F1 | Accuracy | QWK | F1 A/B/C/D |
|---|---:|---:|---:|---:|---:|
| 1 | 4 | 0.8126870715 | 0.8560794045 | 0.6873629019 | 1.000000 / 0.655172 / 0.907051 / 0.688525 |
| 3 | 2 | 0.6822455124 | 0.8440594059 | 0.6206403148 | 0.666667 / 0.740741 / 0.904908 / 0.416667 |

The common-first20 mean is **0.7474662919**, sample SD **0.0922361110**, and
minimum **0.6822455124**. The registered two-fold numerical gates remain met,
but neither fold improved after epoch 4. Epoch-20 Macro-F1 is only
0.5161323490/0.5306034483, confirming substantial selected-to-late-epoch
decay and making the final checkpoint/provenance audits especially important.

The evidence still supports ConvNeXt-Tiny over DenseNet121 at a matched early
horizon, mainly through fold 1. It does not yet prove lower five-fold
dispersion: two-fold sample SD is 0.0922 and rare-class A contributes only
three total DEV cases. Continue both immutable runs to 50 epochs and do not
expand until the completed audits pass. No tuning or new run is launched from
this intermediate result.
