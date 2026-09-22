# A42 A-gate CV5 — common first 20 epochs

Expansion job `1043` remains RUNNING on RTX 5090. Combining preserved folds
1/3 with expansion folds 0/2/4 at the common first-20 horizon gives:

| Fold | Selected epoch <=20 | Macro-F1 | Accuracy | QWK | F1 A/B/C/D |
|---:|---:|---:|---:|---:|---|
| 0 | 4 | 0.824370 | 0.849010 | 0.712318 | 1.0000 / 0.7048 / 0.8988 / 0.6939 |
| 1 | 19 | 0.761529 | 0.851117 | 0.587921 | 1.0000 / 0.5862 / 0.9099 / 0.5500 |
| 2 | 8 | 0.606175 | 0.774194 | 0.606120 | 0.4000 / 0.6410 / 0.8503 / 0.5333 |
| 3 | 7 | 0.738565 | 0.851485 | 0.709429 | 0.6667 / 0.7579 / 0.9034 / 0.6263 |
| 4 | 6 | 0.794524 | 0.828784 | 0.661555 | 1.0000 / 0.7347 / 0.8867 / 0.5567 |

CV5 mean improves to `0.7450325`, but sample SD `0.0841712` and minimum
`0.6061748` still fail. Mean accuracy is `0.8309179`, QWK `0.6554684`, and
B/C/D F1 mean `0.7222656`.

Fold 1 now contributes its known epoch-19 improvement, while fold 2 has not
improved after epoch 8 and remains the bottleneck. The numerical pattern is
consistent with the A-gate helping some folds but failing to create a precise
fold-2 A boundary. Continue unchanged through full50/audit; do not tune or
draw a final conclusion early.
