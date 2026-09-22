# A36 view-token attention common first-20 review

Both fixed stress folds reached epoch 20 normally. Their selected values did
not improve after the common first-10 checkpoint.

| Fold | Best epoch | Macro-F1 | Accuracy | F1 A/B/C/D | QWK |
|---|---:|---:|---:|---|---:|
| 1 | 6 | 0.562825 | 0.841191 | 0.0000 / 0.7222 / 0.9020 / 0.6271 | 0.687210 |
| 3 | 8 | 0.726706 | 0.849010 | 0.6667 / 0.7089 / 0.9038 / 0.6275 | 0.683353 |

Two-fold mean remains 0.644766, sample SD 0.115881 and minimum 0.562825.
A36 remains below both expansion gates. Continue the immutable run to epoch
50 for the registered final audit, but do not expand it.

The controlled interpretation is that attention across four globally pooled
view vectors may help fold 3, but does not yet recover fold 1. If final A36
fails, the next architectural hypothesis should preserve spatial tokens from
each DenseNet feature map and perform cross-view attention over those tokens,
while keeping data, loss, optimizer and heads fixed.

