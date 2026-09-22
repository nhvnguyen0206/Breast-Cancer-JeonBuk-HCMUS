# A19 CV5 confirmation — common epoch 10

Job937 folds 1–4 all reached epoch 10 on RTX 5090 without task failure.
Fold0 is retained from completed audited job936; it was not rerun.

| Fold | Best epoch so far | Best Macro-F1 | Epoch-10 Macro-F1 | Best class F1 A/B/C/D |
|---:|---:|---:|---:|---|
| 0 | 11 (completed) | 0.762386 | — | 1.0000 / 0.6420 / 0.8464 / 0.5612 |
| 1 | 5 | 0.564052 | 0.493735 | 0.0000 / 0.7324 / 0.9100 / 0.6139 |
| 2 | 9 | 0.604389 | 0.474965 | 0.4000 / 0.6087 / 0.8542 / 0.5546 |
| 3 | 7 | 0.597245 | 0.502603 | 0.4000 / 0.6316 / 0.8339 / 0.5235 |
| 4 | 4 | 0.530128 | 0.503829 | 0.0000 / 0.6542 / 0.8702 / 0.5962 |

The provisional best-so-far vector is `[0.762386, 0.564052, 0.604389,
0.597245, 0.530128]`: mean `0.611640`, sample SD `0.089293`, minimum
`0.530128`. These are incomplete checkpoints for folds 1–4, so they are not
the final CV5 estimate and must not be used to accept or reject A19 early.

All four tasks remain running unchanged to epoch 50. The next scheduled review
is the common epoch-20 milestone unless a task fails first.
