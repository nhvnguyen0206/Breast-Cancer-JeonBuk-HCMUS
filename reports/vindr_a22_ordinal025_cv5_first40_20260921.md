# A22 CV5 confirmation — first 40 epochs

All confirmation tasks remain healthy on RTX 5090 nodes with no requeue or
restart. No fold selected a new best checkpoint during epochs 31--40, so the
best-through-40 results are unchanged from epoch 30:

| Fold | Best epoch | Macro-F1 |
|---:|---:|---:|
| 0 | 22 | 0.771853 |
| 1 | 10 | 0.566206 |
| 2 | 9 | 0.681848 |
| 3 | 15 | 0.593283 |
| 4 | 29 | 0.562611 |

Temporary mean Macro-F1 remains **0.635160**, sample SD **0.090328**, and
minimum **0.562611**. Mean accuracy is **0.817060**, mean QWK **0.634355**, and
mean class F1 A/B/C/D is `0.450000 / 0.621893 / 0.884186 / 0.584562`.
Continue through epoch 50, then audit every checkpoint/prediction artifact and
W&B run before drawing the final conclusion.
