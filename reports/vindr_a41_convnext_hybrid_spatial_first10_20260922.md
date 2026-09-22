# A41 ConvNeXt hybrid-spatial screen: common first 10 epochs

Both job-1031 tasks are healthy on the permitted RTX 5090 node. This is a
matched-horizon selected DEV milestone, not a final audit or independent test.

| Fold | Best epoch <=10 | Macro-F1 | Accuracy | QWK | F1 A/B/C/D |
|---|---:|---:|---:|---:|---:|
| 1 | 9 | 0.8213746277 | 0.8684863524 | 0.6901484050 | 1.000000 / 0.800000 / 0.917317 / 0.568182 |
| 3 | 7 | 0.7170961423 | 0.8341584158 | 0.6654802511 | 0.666667 / 0.708861 / 0.892857 / 0.600000 |

The common-first10 mean is **0.7692353850**, sample SD **0.0737360242**, and
minimum **0.7170961423**. Both registered numerical screen gates are met.

Against A40 at the same first10 horizon, A41 changes fold1 from 0.8126870715
to 0.8213746277 and fold3 from 0.6822455124 to 0.7170961423. The improvement
is not solely class A: fold1 B F1 rises to 0.80 and fold3 D F1 rises to 0.60.
This is early evidence that a residual regional path is better than either
global relational fusion alone or wholesale attention replacement.

Epoch-10 scores themselves are 0.5403411310 and 0.5554435014, so late-epoch
decay remains. Continue unchanged to common20 and full50/audit; do not expand
or tune from this intermediate result. Only three class-A DEV cases occur
across these folds, so A performance remains weak evidence by itself.
