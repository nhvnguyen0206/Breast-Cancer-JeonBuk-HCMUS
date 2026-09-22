# A41 hybrid-spatial CV5: common first 10 epochs

This preliminary aggregate restricts every fold to the same first-10 horizon.
Job1031 supplies preserved folds 1/3 and job1033 supplies folds 0/2/4. All
tasks use the same immutable A41 snapshot/config/split/seed on permitted RTX
5090 nodes. These are selected DEV results, not final audits.

| Fold | Best epoch <=10 | Macro-F1 | Accuracy | QWK | F1 A/B/C/D |
|---|---:|---:|---:|---:|---:|
| 0 | 4 | 0.8280128668 | 0.8465346535 | 0.7183085920 | 1.000000 / 0.720000 / 0.895623 / 0.696429 |
| 1 | 9 | 0.8213746277 | 0.8684863524 | 0.6901484050 | 1.000000 / 0.800000 / 0.917317 / 0.568182 |
| 2 | 3 | 0.5583275293 | 0.8486352357 | 0.6571265185 | 0.000000 / 0.732394 / 0.904762 / 0.596154 |
| 3 | 7 | 0.7170961423 | 0.8341584158 | 0.6654802511 | 0.666667 / 0.708861 / 0.892857 / 0.600000 |
| 4 | 6 | 0.7598495569 | 0.7692307692 | 0.6149800191 | 1.000000 / 0.614035 / 0.837128 / 0.588235 |

Mean Macro-F1 is **0.7369321446**, sample SD **0.1098231696**, and minimum
**0.5583275293**. Only the mean gate passes. Fold 2 remains the bottleneck and
again misses its single class-A case, although it improves slightly over A40's
matched first10 fold-2 score 0.5439920998 and improves D F1.

The result does not justify early rejection: A40 fold3 improved only at epoch
34, and A41's spatial residual may learn later. Continue all expansion runs
unchanged to common20 and full50/audit. Do not tune on fold 2 or replace the
frozen split.
