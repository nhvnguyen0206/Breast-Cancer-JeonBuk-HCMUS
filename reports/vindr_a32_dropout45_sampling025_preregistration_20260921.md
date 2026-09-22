# A32 preregistration: interpolated dropout on A30

Parent A30. Change only `model.dropout` from 0.40 to 0.45 and arm metadata.
Retain sampling power 0.25, augmentation, LR, weight decay, losses, AMP,
batch size, cache, preprocessing, DenseNet121/hierarchical fusion, seed 42,
and frozen grouped split. Inference remains one flat-head checkpoint; no
ensemble.

Rationale: A30 is the closest completed arm to joint acceptance (mean
0.709931, SD 0.051267, minimum 0.640275). A9 showed that dropout 0.50 with
natural sampling harmed CV5, so A32 is a bounded interpolation, not an
assumption that stronger regularization is monotonically beneficial. The
hypothesis is that a small additional dropout step may improve weak-fold
generalization while preserving A30's mean.

Before submission, clone immutable A30, add only the A32 config, verify the
semantic delta, source/script/split byte parity, assignment digest, and full
snapshot tests. Run fixed fold 0 for all 50 epochs on RTX 5090, excluding
worker2/Vesta. Expand folds 1–4 only after completed screen audit PASS and
selected DEV Macro-F1 >= 0.70, retaining the original fold 0. Final
acceptance remains mean >= 0.70, sample SD <= 0.05, and minimum >= 0.65.
Selected DEV is not independent-test evidence; only six class-A cases exist.

## Deployment preflight

Immutable A30 was cloned to
`/slurmshared/Ngoc/code/hcmus-density-auggeo-dropout45-sampling025-20260921-v1`.
The parsed config delta contains exactly arm metadata and dropout 0.40 ->
0.45. `src/` and `scripts/` are byte-identical to A30; assignment SHA256 is
unchanged; 16/16 snapshot tests passed. Config SHA256:
`b8ae926fdc235672455214518a40add2ae9cbef062b7391bbbfc5858e7070377`.

Submitted fold 0 only as job `987_0`. Startup verification: RUNNING on
`slurm-b20a-master-0`, `NVIDIA GeForce RTX 5090`, no requeue/restart, and
worker2/Vesta excluded. W&B:
https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/4fyhjmkw
