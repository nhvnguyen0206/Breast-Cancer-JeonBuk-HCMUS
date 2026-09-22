# A36 completed two-fold stress screen

A36 replaced the complete handcrafted relational fusion with attention over
four globally pooled view vectors. Both preregistered folds completed 50
epochs on the permitted master RTX 5090, and both final read-only audits PASS.

| Fold | Best epoch | Macro-F1 | F1 A/B/C/D | QWK | W&B |
|---|---:|---:|---|---:|---|
| 1 | 21 | 0.563194 | 0.0000 / 0.6377 / 0.9151 / 0.7000 | 0.680339 | `v4vdj0ig` |
| 3 | 35 | 0.739842 | 0.6667 / 0.7368 / 0.9185 / 0.6374 | 0.703911 | `7be8i6ku` |

The two-fold mean is 0.651518, sample SD 0.124909 and minimum 0.563194.
A36 fails the registered mean >=0.70 and minimum >=0.65 expansion gates, so
folds 0/2/4 must not run. Neither screen fold reached 0.75 at any epoch.

The audits verified the frozen split hash, all 50 history entries, checkpoint
and prediction consistency, valid manifests, normalized probabilities, and
finished W&B states. These remain selected DEV results, not independent-test
performance.

Conclusion: view-level attention materially improves fold 3 but does not
solve fold 1. Reject A36 and proceed to the preregistered A37 spatial-token
attention preflight, which directly tests whether global pooling discarded
useful regional density information.

