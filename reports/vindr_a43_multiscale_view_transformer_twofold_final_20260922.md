# A43 multi-scale four-view Transformer — completed weak-fold screen

Job `1041` completed all 50 epochs on the current weak folds 2 and 3. Both
read-only audits PASS, validating frozen manifests and assignment SHA256,
complete histories, selected checkpoints, reconstructed predictions,
probability normalization and finished W&B summaries.

| Fold | Best epoch | Macro-F1 | Accuracy | QWK | F1 A/B/C/D | W&B |
|---:|---:|---:|---:|---:|---|---|
| 2 | 7 | 0.799443 | 0.836228 | 0.668040 | 1.0000 / 0.7158 / 0.8925 / 0.5895 | `hw6b2q8i` |
| 3 | 35 | 0.719963 | 0.844059 | 0.668921 | 0.6667 / 0.7027 / 0.9010 / 0.6095 | `0cojka4k` |

Two-fold mean is `0.7597029`, sample SD `0.0562008`, minimum `0.7199629`,
mean accuracy `0.8401438`, mean QWK `0.6684805`, and B/C/D F1 mean
`0.7351594`. Both registered expansion gates pass. B/C/D is within `0.0040`
of A41 on the same folds, while A43 uniquely repairs the ConvNeXt fold-2 A
collapse. This supports a substantive representation gain rather than an
A-only checkpoint artifact.

The selected checkpoints still differ widely in epoch and epoch-50 scores
decay, so CV5 stability remains unproven. Preserve folds 2/3 and train only
folds 0/1/4 from the exact immutable snapshot. This remains selected DEV
evidence, not an independent test estimate.

Audit artifacts:
`/slurmshared/Ngoc/audits/vindr-a43-twofold-final-20260922`.
