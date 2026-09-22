# A21 preregistration: moderate primary focal scale

Parent: A5 (`auggeo_dropout30`), retained after A20 rejection.

## Single treatment

Add `loss.focal_scale: 2.0`, multiplying only the class-balanced focal term
used by the primary four-class head. The default is exactly 1.0. All auxiliary
loss terms and their coefficients remain unchanged. Architecture, natural FIT
sampling, augmentation, dropout, optimizer, batch size 2, cache, fixed split,
seed 42 and 50-epoch schedule remain A5-identical. Inference still uses one
flat-head checkpoint; no ensemble or head fusion.

## Rationale

Under natural FIT frequencies, the current class-mean weights give a small
average focal contribution relative to the auxiliary ordinal/binary/neighbor
terms. The earlier full FIT-expectation normalization multiplied focal by
about 17.49 and failed the B0 fold0 screen despite improving descriptive B/C/D
F1. A21 tests a deliberately modest interpolation (2x), not the failed full
normalization. No benefit is assumed.

## Protocol

- Verify default scale 1.0 is numerically identical and scale 2.0 changes only
  the focal contribution; require finite real-cache backward gradients.
- Run fixed fold0 only, fresh ImageNet initialization, full 50 epochs on RTX
  5090; exclude Vesta/worker2 and use no requeue.
- Audit the completed screen before expansion. Expand fresh folds1–4 only if
  fold0 selected DEV Macro-F1 is at least 0.75; retain fold0.
- Final acceptance requires mean Macro-F1 at least 0.70, sample SD at most
  0.05, and minimum fold at least 0.65 on the fixed seed-42 CV5 protocol.

Selected DEV is not an independent test; the six class-A studies remain a
major limitation and all class-wise metrics must be reported.
