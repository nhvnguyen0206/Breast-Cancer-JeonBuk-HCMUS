# A41 ConvNeXt hybrid-spatial screen: common first 20 epochs

Both job-1031 tasks remain healthy on the permitted RTX 5090 node. At the
matched first-20 horizon, fold 1 improves its selected checkpoint while fold
3 retains epoch 7.

| Fold | Best epoch <=20 | Macro-F1 | Accuracy | QWK | F1 A/B/C/D |
|---|---:|---:|---:|---:|---:|
| 1 | 16 | 0.8321319993 | 0.8808933002 | 0.7111887485 | 1.000000 / 0.783784 / 0.925697 / 0.619048 |
| 3 | 7 | 0.7170961423 | 0.8341584158 | 0.6654802511 | 0.666667 / 0.708861 / 0.892857 / 0.600000 |

The common-first20 mean is **0.7746140708**, sample SD **0.0813426346**, and
minimum **0.7170961423**. Both registered screen gates remain met. Fold 1's
new checkpoint improves accuracy, QWK and B/C/D balance over its first10
selection, so the gain is not an artifact of only the single class-A case.

Epoch-20 scores themselves are 0.5082001100 and 0.5155016926, confirming that
checkpoint sensitivity persists. Continue unchanged to full50 and audit;
do not expand or tune from this intermediate result.
