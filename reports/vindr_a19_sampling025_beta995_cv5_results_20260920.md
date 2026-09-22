# A19 final audited CV5 result

Audit status: **PASS**. All five folds use the fixed grouped split with
assignment SHA-256
`43daa86936ee7b1bae1b200836fb1afdfe0c8294c7c865d8f5758bf989f12a9a`,
seed 42, fresh ImageNet initialization, 50 epochs, and the same A19 learning
configuration. This is selected DEV cross-validation, not an independent test.

| Fold | Selected epoch | Macro-F1 | Accuracy | QWK | F1 A/B/C/D |
|---:|---:|---:|---:|---:|---|
| 0 | 11 | 0.762386 | 0.777228 | 0.601456 | 1.0000 / 0.6420 / 0.8464 / 0.5612 |
| 1 | 5 | 0.564052 | 0.856079 | 0.668773 | 0.0000 / 0.7324 / 0.9100 / 0.6139 |
| 2 | 25 | 0.681597 | 0.831266 | 0.605528 | 0.6667 / 0.6933 / 0.8958 / 0.4706 |
| 3 | 24 | 0.645849 | 0.811881 | 0.536563 | 0.6667 / 0.5152 / 0.8854 / 0.5161 |
| 4 | 20 | 0.558737 | 0.846154 | 0.670309 | 0.0000 / 0.7209 / 0.9018 / 0.6122 |

Final fold Macro-F1 vector:
`[0.762386, 0.564052, 0.681597, 0.645849, 0.558737]`.

- Macro-F1 mean: **0.642524**
- Macro-F1 sample SD: **0.085268**
- Minimum fold: **0.558737**
- Mean accuracy: **0.824522**
- Mean QWK: **0.616526**
- Mean class F1 A/B/C/D: **0.466667 / 0.660757 / 0.887878 / 0.554795**
- Mean B/C/D F1: **0.701143**
- Pooled descriptive Macro-F1: **0.677877** over 2,017 unique cases

## Decision

Reject A19 as the next baseline. It fails the agreed stability target (mean at
least 0.70, sample SD at most 0.05, minimum fold at least 0.65). It also trails
its direct A6 parent: A6 mean/SD/min were `0.676551 / 0.064446 / 0.619496`.
Changing class-balanced focal beta from `0.999` to `0.995` therefore did not
solve fold instability and materially reduced mean performance. A19 is only a
small improvement over rejected A17 in mean and dispersion, while its QWK and
class-D F1 are worse.

The six class-A cases make A-F1 highly discrete and unstable. The persistent
weakness is not an invalid split or incomplete run: it is mainly fold-dependent
B/D discrimination and the sensitivity of Macro-F1 to the extremely scarce A
class. Future changes should target calibration/selection or representation
robustness without stronger resampling/class-weight compensation.
