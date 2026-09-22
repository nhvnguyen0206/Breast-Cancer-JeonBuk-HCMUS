# A41 hybrid-spatial CV5: common first 30 epochs

At the matched first-30 horizon, fold 4 improves again and selects epoch 30;
the other fold selections remain unchanged.

| Fold | Best epoch <=30 | Macro-F1 | Accuracy | QWK | F1 A/B/C/D |
|---|---:|---:|---:|---:|---:|
| 0 | 4 | 0.8280128668 | 0.8465346535 | 0.7183085920 | 1.000000 / 0.720000 / 0.895623 / 0.696429 |
| 1 | 16 | 0.8321319993 | 0.8808933002 | 0.7111887485 | 1.000000 / 0.783784 / 0.925697 / 0.619048 |
| 2 | 3 | 0.5583275293 | 0.8486352357 | 0.6571265185 | 0.000000 / 0.732394 / 0.904762 / 0.596154 |
| 3 | 7 | 0.7170961423 | 0.8341584158 | 0.6654802511 | 0.666667 / 0.708861 / 0.892857 / 0.600000 |
| 4 | 30 | 0.8146311433 | 0.8535980149 | 0.6810810811 | 1.000000 / 0.790123 / 0.905901 / 0.562500 |

Mean Macro-F1 reaches **0.7500399362**, sample SD is **0.1170788722**, and
minimum remains **0.5583275293**. Mean now reaches the stretch target, but SD
and minimum still fail because fold 2 has not improved after epoch 3.

Fold 4's epoch-30 checkpoint materially improves B/C balance and QWK, showing
that later learning can still matter. Continue all runs unchanged to full50
and audit. Do not tune specifically on fold 2 or reinterpret the rare-A miss
as the only issue; its D F1 is also below the stronger folds.
