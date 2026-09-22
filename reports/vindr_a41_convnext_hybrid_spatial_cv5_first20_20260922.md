# A41 hybrid-spatial CV5: common first 20 epochs

At the matched first-20 horizon, fold 4 improves its selection to epoch 19;
the other folds remain unchanged.

| Fold | Best epoch <=20 | Macro-F1 | Accuracy | QWK | F1 A/B/C/D |
|---|---:|---:|---:|---:|---:|
| 0 | 4 | 0.8280128668 | 0.8465346535 | 0.7183085920 | 1.000000 / 0.720000 / 0.895623 / 0.696429 |
| 1 | 16 | 0.8321319993 | 0.8808933002 | 0.7111887485 | 1.000000 / 0.783784 / 0.925697 / 0.619048 |
| 2 | 3 | 0.5583275293 | 0.8486352357 | 0.6571265185 | 0.000000 / 0.732394 / 0.904762 / 0.596154 |
| 3 | 7 | 0.7170961423 | 0.8341584158 | 0.6654802511 | 0.666667 / 0.708861 / 0.892857 / 0.600000 |
| 4 | 19 | 0.7897866700 | 0.8138957816 | 0.6355667555 | 1.000000 / 0.740741 / 0.876033 / 0.542373 |

Mean Macro-F1 rises to **0.7450710415**, sample SD is **0.1141426504**, and
minimum remains **0.5583275293**. Mean passes; SD and minimum fail because
fold 2 still has not improved after epoch 3. Fold 4's later improvement shows
that continuing the complete registered horizon remains necessary.

Continue all runs unchanged to full50/audit. Do not tune specifically on fold
2 or select a different split. Rare class A remains insufficient evidence by
itself; fold-2 B/C/D mean is approximately 0.7444 despite its zero A F1.
