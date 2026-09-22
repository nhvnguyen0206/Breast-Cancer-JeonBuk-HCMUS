# A20 preregistration: physical batch size 4

Parent: A5 (`auggeo_dropout30`), the strongest completed mean CV5 arm.
A19 is rejected before this arm is registered.

## Single treatment

Change only `training.batch_size` from 2 cases (8 mammography views) to 4
cases (16 views). Keep the DenseNet121 shared backbone, hierarchical bilateral
fusion, all three heads, loss weights, class weighting, natural FIT sampling,
augmentation, stretch-512 preprocessing, optimizer hyperparameters, seed 42,
fixed grouped split, cache and 50-epoch contract unchanged. Inference uses one
selected checkpoint; no ensemble.

The larger physical batch changes BatchNorm statistics and necessarily halves
optimizer steps per epoch. Those are inseparable effects of this treatment and
will be reported together; no learning-rate scaling or second treatment is
allowed in A20.

## Rationale

The DenseNet backbone contains 121 BatchNorm modules while the current case
batch is only two. A18 showed that forcing their running statistics to remain
fixed is numerically incompatible with the current AMP run, so A20 tests a
less invasive way to improve their estimates. This is a hypothesis, not an
expected gain.

## Protocol and decision rule

- First verify a real forward/backward/update at batch 4 on an RTX 5090.
- Run only fixed fold0, fresh ImageNet initialization, full 50 epochs.
- Exclude Vesta and `slurm-b40a-worker-2`; require the runtime GPU name to
  contain `5090` and use no requeue.
- Complete the read-only screen audit before any expansion.
- Expand fresh folds1–4 only if completed fold0 selected DEV Macro-F1 is at
  least 0.75. Retain fold0; do not rerun or select a favorable fold.
- Final success remains mean Macro-F1 at least 0.70, sample SD at most 0.05,
  and minimum fold at least 0.65 on the fixed seed-42 CV5 protocol.

Selected DEV is not an independent test. With only six class-A studies, A-F1
and four-class Macro-F1 remain highly discrete; B/C/D F1, QWK, severe errors
and fold dispersion must accompany the primary score.
