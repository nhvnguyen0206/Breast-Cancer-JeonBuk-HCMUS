# A42 A-gate CV5 — common first 10 epochs

Expansion job `1043` remains RUNNING on permitted RTX 5090 nodes. Combining
its folds 0/2/4 with the preserved job-1037 folds 1/3, the reproducible common
first-10 selection is:

| Fold | Selected epoch <=10 | Macro-F1 | Accuracy | QWK | F1 A/B/C/D |
|---:|---:|---:|---:|---:|---|
| 0 | 4 | 0.824370 | 0.849010 | 0.712318 | 1.0000 / 0.7048 / 0.8988 / 0.6939 |
| 1 | 5 | 0.580333 | 0.873449 | 0.696890 | 0.0000 / 0.7536 / 0.9219 / 0.6458 |
| 2 | 8 | 0.606175 | 0.774194 | 0.606120 | 0.4000 / 0.6410 / 0.8503 / 0.5333 |
| 3 | 7 | 0.738565 | 0.851485 | 0.709429 | 0.6667 / 0.7579 / 0.9034 / 0.6263 |
| 4 | 6 | 0.794524 | 0.828784 | 0.661555 | 1.0000 / 0.7347 / 0.8867 / 0.5567 |

CV5 mean is `0.7087932`, sample SD `0.1102572`, minimum `0.5803329`, mean
accuracy `0.8353844`, mean QWK `0.6772623`, and B/C/D F1 mean `0.7406132`.
Only the mean gate passes. SD and minimum fail.

Fold 2 improves over A41's `0.5583275` and now has positive A F1 `0.4`, but
its single true A is accompanied by three A false positives and B/C/D regress.
Fold 1 is still limited by the first-10 horizon; it later improved at epoch 19
in the completed screen. Continue all expansion folds unchanged to common20
and full50/audit. Do not draw a final conclusion from this early horizon.
