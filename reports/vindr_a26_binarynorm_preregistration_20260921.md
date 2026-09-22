# A26 preregistration: FIT-expectation binary normalization

Parent: immutable A5. Single treatment: binary weighted CE changes from
batch-weight mean to mean(weighted per-case CE)/E_FIT[binary_weight].
Keep coefficient .3, focal/ordinal/neighbor losses, natural sampling, batch2,
AMP, augmentation, dropout, optimizer, seed42, cache and frozen split.
No architectural or inference change; all heads retained, no ensemble.
Rationale: vindr_binary_batch_normalization_diagnostic_20260921.md.
Hypothesis is unproven; changing objective normalization may hurt results.

Implementation is opt-in binary_normalization=train_expectation; default
batch_weight_mean preserves historical behavior. Engine already forwards
loss config kwargs. Local loss implementation and three focused tests copied
to isolated remote /slurmshared/Ngoc/runs/binary-normalization-tests-z5gnNc:
3/3 PASS for default equivalence, explicit weighted-CE formula, unchanged
other loss terms, finite backward gradients, sample-weighted partition
invariance including homogeneous pairs/singleton, and invalid-mode rejection.
This is not a real-cache GPU preflight or a full pipeline regression pass.

Before launch: clone immutable A5; port only binary-normalization change,
verify unrelated source parity and config delta; validate all manifests,
run regression plus focused tests and finite real-cache forward/backward.
Do not deploy unrelated dirty local source changes.

Run fixed fold0 full50 on RTX5090 only, worker2/Vesta excluded, no requeue.
Only completed audited selected DEV Macro-F1>=.75 permits fresh folds1–4;
preserve screen fold0. CV5 acceptance mean>=.70/sampleSD<=.05/min>=.65,
aspirational mean>=.75. Report class F1/accuracy/QWK and severe errors.
Only six A studies; selected DEV is not independent test. Review every10–20
epochs. No training job submitted yet.

## Preflight completed

Created `/slurmshared/Ngoc/code/hcmus-density-auggeo-dropout30-binarynorm-20260921-v1`
from immutable A5, porting only the normalization change into its older loss
implementation (not replacing it with dirty local loss code). Other source,
launcher and frozen split files are byte-identical. Parsed config differs
only in arm metadata and binary_normalization; all five manifests validated.
Config SHA256 a401f859f6fde827f905d27802056f5d1f943ae5d86ce56b150c98f5a7234eaa.
Loss SHA256 a3f04f75cb360874475263ff56da6beb2a7c25bbd0a93dc5b498cb85be14514c.
Full remote unittest discovery exited0 (A5 suite plus3 focused tests).
Real-cache batch2/512 CPU FP32 forward/backward: finite loss1.1900737286,
all populated parameter gradients finite. This preflight used random model
weights; actual registered training uses fresh ImageNet weights and GPU AMP.

Submitted fixed fold0 only as job963_0, verified RUNNING on master and log
confirms NVIDIA GeForce RTX5090. W&B initializing run hpzf3sq6.
No confirmation folds submitted. First result review at10–20 epochs.
