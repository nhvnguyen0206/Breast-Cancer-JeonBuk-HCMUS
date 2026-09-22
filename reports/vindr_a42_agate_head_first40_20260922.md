# A42 A-gate diagnostic control — common first 40 epochs

Both job-1037 tasks remain RUNNING on master RTX 5090 and completed epoch 40.
The selected result is unchanged from first20 and first30.

| Fold | Selected epoch <=40 | Macro-F1 | Accuracy | QWK | F1 A/B/C/D |
|---:|---:|---:|---:|---:|---|
| 1 | 19 | 0.761529 | 0.851117 | 0.587921 | 1.0000 / 0.5862 / 0.9099 / 0.5500 |
| 3 | 7 | 0.738565 | 0.851485 | 0.709429 | 0.6667 / 0.7579 / 0.9034 / 0.6263 |

Aggregate mean is `0.7500472`, sample SD `0.0162380`, minimum `0.7385653`,
accuracy `0.8513009`, QWK `0.6486748`, and B/C/D F1 mean `0.7222852`. Both
numerical gates remain met, but neither fold has improved for at least 21
epochs.

Epoch-40 Macro-F1 is `0.5402210/0.5000093`, with A F1 zero on both folds.
Finish the remaining ten epochs and audit; do not expand before then.
