# A41 ConvNeXt hybrid-spatial screen: common first 30 epochs

At the matched first-30 horizon, the selected checkpoints remain unchanged
from first20.

| Fold | Best epoch <=30 | Macro-F1 | Accuracy | QWK | F1 A/B/C/D |
|---|---:|---:|---:|---:|---:|
| 1 | 16 | 0.8321319993 | 0.8808933002 | 0.7111887485 | 1.000000 / 0.783784 / 0.925697 / 0.619048 |
| 3 | 7 | 0.7170961423 | 0.8341584158 | 0.6654802511 | 0.666667 / 0.708861 / 0.892857 / 0.600000 |

Mean Macro-F1 remains **0.7746140708**, sample SD **0.0813426346**, and
minimum **0.7170961423**. Both screen gates still pass. The spatial residual
architecture therefore retains its advantage over A40 through 30 epochs,
although no later checkpoint improves the selected pair.

Epoch-30 scores are 0.5279787026 and 0.5553688474, so selected-to-late decay
persists. Continue unchanged to full50/audit; do not expand or tune early.
