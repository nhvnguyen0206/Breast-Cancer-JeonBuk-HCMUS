# A20 batch4 final audited CV5 result

Audit status: **PASS**. All five folds use the fixed grouped split, seed 42,
fresh ImageNet initialization, the same batch4 configuration and 50 epochs.
All source W&B runs are finished and agree with recomputed predictions. This
is selected DEV cross-validation, not an independent test.

| Fold | Selected epoch | Macro-F1 | Accuracy | QWK | F1 A/B/C/D |
|---:|---:|---:|---:|---:|---|
| 0 | 13 | 0.773328 | 0.816832 | 0.612385 | 1.0000 / 0.6486 / 0.8810 / 0.5636 |
| 1 | 3 | 0.558851 | 0.846154 | 0.674365 | 0.0000 / 0.6813 / 0.9015 / 0.6526 |
| 2 | 3 | 0.772299 | 0.808933 | 0.627367 | 1.0000 / 0.6226 / 0.8731 / 0.5934 |
| 3 | 12 | 0.577816 | 0.829208 | 0.673262 | 0.2000 / 0.6575 / 0.9027 / 0.5510 |
| 4 | 24 | 0.768573 | 0.816377 | 0.605581 | 1.0000 / 0.6582 / 0.8814 / 0.5347 |

- Macro-F1 mean: **0.690174**
- Macro-F1 sample SD: **0.111440**
- Minimum fold: **0.558851**
- Mean accuracy: **0.823501**
- Mean QWK: **0.638592**
- Mean class F1 A/B/C/D: **0.640000 / 0.653674 / 0.887950 / 0.579070**
- Mean B/C/D F1: **0.706898**

## Decision

Reject A20 as the next baseline. It fails all agreed targets: mean at least
`0.70`, sample SD at most `0.05`, and minimum fold at least `0.65`.

Relative to A5, batch4 lowers mean Macro-F1 by `0.012655`, minimum fold by
`0.011335`, accuracy by `0.013875`, QWK by `0.032164`, and B/C/D mean by
`0.030206`. Its SD improves by only `0.005849`. Mean A-F1 rises by `0.04`, but
with six A studies this does not compensate for weaker B and especially D.
Larger physical batches therefore do not resolve the fold instability; keep
A5 as the strongest completed mean-CV5 reference.
