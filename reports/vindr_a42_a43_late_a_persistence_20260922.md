# Late-training rare-A persistence snapshot

Read directly from run histories on 2026-09-22. This is a diagnostic
snapshot, not a matched-horizon ranking or final A43 result.

| Arm | Fold | Completed epochs | Epochs with A F1 > 0 | A-positive epochs after30 / observed after30 |
|---|---:|---:|---:|---:|
| A42 | 0 | 50 | 7 | 0/20 |
| A42 | 1 | 50 | 1 | 0/20 |
| A42 | 2 | 50 | 2 | 0/20 |
| A42 | 3 | 50 | 4 | 0/20 |
| A42 | 4 | 47 | 8 | 2/17 |
| A43 | 0 | 39 | 31 | 3/9 |
| A43 | 1 | 40 | 1 | 0/10 |
| A43 | 2 | 50 | 12 | 0/20 |
| A43 | 3 | 50 | 9 | 4/20 |
| A43 | 4 | 39 | 12 | 5/9 |

A43 changes where A recovery occurs but does not demonstrate persistent
recovery across all folds. Every fold's latest observed A F1 is zero.
A42 folds0--3 never recover positive A F1 after epoch30. Only six A exams
exist across all DEV folds, so these counts describe sensitivity of those
cases, not population-level confidence or an independent test result.

Training focal losses are very small at the observed endpoints, while DEV
A fails; this is consistent with poor rare-class generalization but does
not establish its cause. Ordinal loss values dominate the remaining total
numerically, but loss magnitudes do not measure gradient dominance. Do not
infer causal loss interference without a controlled gradient/ablation check.
The next architecture decision remains pending full A43 CV5 audit.
