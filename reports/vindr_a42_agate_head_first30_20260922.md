# A42 A-gate diagnostic control — common first 30 epochs

Both job-1037 tasks remain RUNNING on master RTX 5090 and completed epoch 30.
The reproducible horizon summary is unchanged from first20.

| Fold | Selected epoch <=30 | Macro-F1 | Accuracy | QWK | F1 A/B/C/D |
|---:|---:|---:|---:|---:|---|
| 1 | 19 | 0.761529 | 0.851117 | 0.587921 | 1.0000 / 0.5862 / 0.9099 / 0.5500 |
| 3 | 7 | 0.738565 | 0.851485 | 0.709429 | 0.6667 / 0.7579 / 0.9034 / 0.6263 |

Aggregate mean is `0.7500472`, sample SD `0.0162380`, minimum `0.7385653`,
accuracy `0.8513009`, QWK `0.6486748`, and B/C/D F1 mean `0.7222852`. Both
numerical screen gates remain provisionally met, but no checkpoint improved
between epochs 21 and 30.

Epoch 30 itself has fold-1/fold-3 Macro-F1 `0.5581752/0.5452214`; both have A
F1 `0`. This large gap from the selected checkpoints confirms unstable rare-A
decision dynamics. Continue unchanged to full50/audit and do not expand early.
