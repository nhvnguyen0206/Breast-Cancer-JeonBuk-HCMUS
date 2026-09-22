# A17 sampling-power .10 — completed CV5 audit

All five registered runs completed 50 epochs. Scheduler state is COMPLETED
with exit code 0 for array908 folds1--4; folds1/2 ran on master and folds3/4
on worker1. Worker2 and Vesta were not used. The read-only audit passed for
the common configuration, architecture, split hash, frozen manifests,
checkpoint selection, prediction membership and labels, probability sums,
recomputed metrics, 2017-case union and five finished W&B runs.

| Fold | Best epoch | Macro-F1 | Accuracy | QWK | F1 A/B/C/D | Epoch-50 Macro-F1 |
|---:|---:|---:|---:|---:|---|---:|
| 0 | 17 | 0.791469 | 0.826733 | 0.655995 | 1.0000 / 0.6286 / 0.8856 / 0.6517 | 0.530100 |
| 1 | 5 | 0.553133 | 0.851117 | 0.682527 | 0.0000 / 0.6897 / 0.9111 / 0.6118 | 0.505062 |
| 2 | 3 | 0.537696 | 0.801489 | 0.638662 | 0.1818 / 0.5075 / 0.8849 / 0.5766 | 0.477545 |
| 3 | 9 | 0.646880 | 0.804455 | 0.634895 | 0.5000 / 0.6118 / 0.8723 / 0.6034 | 0.508346 |
| 4 | 14 | 0.675912 | 0.776675 | 0.614935 | 0.6667 / 0.6000 / 0.8468 / 0.5902 | 0.521941 |

Audited selected-DEV aggregate:

- Macro-F1 mean: **0.641017889812455**
- Macro-F1 sample SD: **0.10281875126033155**
- Minimum fold: **0.5376961278531225**
- Accuracy mean: **0.8120937031668427**
- QWK mean: **0.6454029273260625**
- Mean F1 A/B/C/D: **0.469697 / 0.607491 / 0.880156 / 0.606728**
- Mean B/C/D F1: **0.6981248631842835**
- Fixed-epoch-50 Macro-F1 mean: **0.5085988060803085**
- Support A/B/C/D: **6 / 196 / 1556 / 259**
- Severe selected errors: **0**

A17 is rejected. Relative to A5, its mean Macro-F1 is lower by
0.0618103903, its sample SD is lower by only 0.0144700615, and every mean
class F1 is lower. It fails the mean, dispersion and minimum-fold criteria.
The passing fold0 screen did not generalize, and the result again shows why
the single fold0 A case cannot justify a campaign decision.

These scores are selected DEV results under seed42, not independent-test or
multi-seed evidence. A5 remains the best completed arm at mean 0.7028282801,
though it still fails the stability criteria.

W&B source runs: fold0 `djz4e32c`, fold1 `txm9bun2`, fold2 `7jtlt2gq`,
fold3 `7uqvm3ct`, fold4 `fpbres7g`.
