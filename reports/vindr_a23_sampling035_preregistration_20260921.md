# A23 preregistration: sampling power 0.35

## Motivation

A5 has the strongest audited mean CV5 Macro-F1 (`0.702828`) but unstable
folds (sample SD `0.117289`, minimum `0.570186`). A6 changed only FIT sampling
power from 0 to 0.25 and produced the strongest stability result so far:
mean `0.676551`, sample SD `0.064446`, minimum `0.619496`. A17 power 0.10 was
too weak and A19's beta change on top of A6 degraded performance. A23 therefore
uses A6 as its direct parent and changes only sampling power from 0.25 to 0.35.

On fold0 FIT, the expected per-epoch class mass changes approximately from
`1.07% / 14.16% / 67.25% / 17.51%` to
`1.73% / 16.22% / 62.56% / 19.49%` for A/B/C/D. This is a moderate increase in
rare-class exposure, not full class balancing.

## Fixed protocol

- DenseNet121 shared backbone and hierarchical bilateral fusion unchanged.
- All loss coefficients, augmentation, optimizer, batch size, 50-epoch budget,
  cache, fixed grouped CV5 split, seed 42 and flat-head single-checkpoint
  inference unchanged from A6.
- Fixed fold0 runs first for all 50 epochs on RTX 5090; worker2/Vesta excluded.
- Launch folds 1--4 only after the completed fold0 audit has selected DEV
  Macro-F1 `>=0.75`.
- No resplitting, fold substitution, ensemble or independent-test claim.

## Acceptance

The final target remains CV5 mean Macro-F1 `>=0.70`, sample SD `<=0.05`, and
minimum fold `>=0.65`. Class-wise F1, accuracy, QWK and confusion matrices are
reported. With only six A cases, gains driven solely by class A are explicitly
treated as fragile selected-DEV evidence.
