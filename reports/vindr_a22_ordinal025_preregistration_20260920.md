# A22 preregistration: ordinal coefficient 0.25

Parent: A5 (`auggeo_dropout30`), retained after A21 failed its screen.

## Single treatment

Change only `loss.ordinal` from `0.5` to `0.25`. Preserve the shared
DenseNet121 backbone, hierarchical bilateral fusion, all prediction heads,
focal/binary/neighbor terms, natural sampling, augmentation, dropout, batch
size, optimizer, cache, fixed split, seed 42 and 50-epoch schedule. Inference
continues to use one flat-head checkpoint; no ensemble or head fusion.

## Rationale

The CORAL diagnostic found a substantial nonzero ordinal-loss floor from the
learned threshold spacing. Its weighted contribution remains the largest late
training term. Raising ordinal weight to 1.0 previously reduced completed CV5
performance, while A21's 2x focal term failed the fold0 screen. A22 therefore
tests whether reducing only the potentially competing ordinal gradient helps
the primary flat head without removing the auxiliary task. This is an
unverified hypothesis.

## Protocol

- Verify the config differs from A5 only in arm metadata and ordinal `0.5 →
  0.25`; validate finite real-cache loss and backward gradients.
- Run fixed fold0 only with fresh ImageNet initialization for all 50 epochs on
  RTX 5090, excluding Vesta/worker2 with no requeue.
- Audit the completed screen before expansion. Run fresh folds1–4 only if
  fold0 selected DEV Macro-F1 is at least 0.75; retain the screened fold0.
- Final acceptance requires mean Macro-F1 at least 0.70, sample SD at most
  0.05, and minimum fold at least 0.65 on fixed seed-42 CV5.

Selected DEV is not an independent test. Report A/B/C/D F1, accuracy, QWK,
severe errors and fold dispersion because only six class-A studies exist.
