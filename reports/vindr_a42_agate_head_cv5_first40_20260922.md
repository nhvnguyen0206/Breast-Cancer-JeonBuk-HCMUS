# A42 hierarchical A-gate CV5 — common first 40 epochs

Expansion job `1043` remains RUNNING on master/worker1 RTX 5090. Selection is
the independently best DEV Macro-F1 in the common epoch-1--40 horizon for all
folds, without ensembling or fold-specific thresholds.

| Fold | Selected epoch <=40 | Macro-F1 | Accuracy | QWK | F1 A/B/C/D |
|---:|---:|---:|---:|---:|---|
| 0 | 4 | 0.824370 | 0.849010 | 0.712318 | 1.0000 / 0.7048 / 0.8988 / 0.6939 |
| 1 | 19 | 0.761529 | 0.851117 | 0.587921 | 1.0000 / 0.5862 / 0.9099 / 0.5500 |
| 2 | 25 | 0.677315 | 0.823821 | 0.605038 | 0.6667 / 0.6585 / 0.8899 / 0.4941 |
| 3 | 7 | 0.738565 | 0.851485 | 0.709429 | 0.6667 / 0.7579 / 0.9034 / 0.6263 |
| 4 | 6 | 0.794524 | 0.828784 | 0.661555 | 1.0000 / 0.7347 / 0.8867 / 0.5567 |

The result is unchanged from the common first-30 horizon: CV5 mean
`0.7592604`, sample SD `0.0561945`, minimum `0.6773145`, mean accuracy
`0.8408434`, mean QWK `0.6552521`, and B/C/D F1 mean `0.7234584`. Mean and
minimum pass, while SD remains `0.0061945` above the final `0.05` gate. The
arm must finish epoch50 and pass all fold audits before any final claim.
