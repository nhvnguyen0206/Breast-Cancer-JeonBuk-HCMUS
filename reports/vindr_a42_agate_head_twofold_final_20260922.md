# A42 A-gate diagnostic control — completed two-fold screen

Job `1037` completed all 50 epochs on folds 1 and 3. Both independent
read-only audits PASS, including frozen manifests and assignment SHA256,
complete histories, checkpoint selection, prediction reconstruction,
probability normalization and finished W&B summaries.

| Fold | Best epoch | Macro-F1 | Accuracy | QWK | F1 A/B/C/D | W&B |
|---:|---:|---:|---:|---:|---|---|
| 1 | 19 | 0.761529 | 0.851117 | 0.587921 | 1.0000 / 0.5862 / 0.9099 / 0.5500 | `5lsfvwi2` |
| 3 | 7 | 0.738565 | 0.851485 | 0.709429 | 0.6667 / 0.7579 / 0.9034 / 0.6263 | `jglym8l6` |

Two-fold mean is `0.7500472`, sample SD `0.0162380`, minimum `0.7385653`,
mean accuracy `0.8513009`, mean QWK `0.6486748`, and B/C/D F1 mean
`0.7222852`. Both registered expansion gates pass.

The result remains scientifically qualified: fold 1 trades lower B/D and QWK
for perfect F1 on its single A exam, and positive-A behavior is transient.
Nevertheless, the preregistered rule requires expansion once both audits and
both numerical gates pass. Preserve folds 1/3 and train only folds 0/2/4 from
the exact immutable snapshot. This is selected DEV evidence, not an
independent test estimate.

Audit artifacts:
`/slurmshared/Ngoc/audits/vindr-a42-twofold-final-20260922`.
