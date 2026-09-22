# A28: effective weight decay on A6

Parent immutable A6 sampling025, not A27. Only weight_decay .0001->.01
plus arm metadata. Preserve tempered sampling .25 (not uniform balanced
sampling), rotation5/translation.03, dropout.3, all losses/heads, DenseNet121,
hierarchical fusion, batch2, AMP, LR5e-5/cosine, seed42, input/cache/split.
No ensemble. No unrelated dirty local source changes may be deployed.

Rationale: A6 CV5 mean .6765513839/SD .0644461991/min .6194960833 is the
strongest observed stability tradeoff. A8 tested effective decay on A5,
not on A6; sampling/decay interaction remains untested. Hypothesis is reduced
overfitting of repeatedly sampled minority studies, not an established cause
or promised improvement. No DEV-driven resplitting or checkpoint rule change.

Preflight: clone A6, verify source/script/split byte parity; parsed config
delta exactly decay/arm; validate all five manifests; full regression and
real-cache augmented tensor finite. Verify nonzero float32 AdamW decay at
initial LR. Then run fixed fold0 full50 on RTX5090 only, exclude worker2/Vesta,
no requeue. Expand fresh folds1–4 only after completed audited selected DEV
Macro-F1>=.75, preserving screen0. Joint CV5 acceptance mean>=.70,
sampleSD<=.05,min>=.65; aspiration mean>=.75. Report classF1,accuracy,QWK;
six A studies limit certainty. Selected DEV is not independent test.
Review10–20 epochs; no job submitted at preregistration.

## Deployment

Snapshot /slurmshared/Ngoc/code/hcmus-density-auggeo-dropout30-sampling025-wd1e2-20260921-v1
cloned from immutable A6. Source/scripts/split byte parity PASS;
parsed config delta exactly decay/arm; all five manifests validated.
Regression16/16 PASS; real-cache four-view512 augmented tensor finite.
Float32 AdamW zero-gradient initial-LR check changes1->.9999995231628418,
confirming numerical decay at initial LR (not a guarantee at late cosine LR).
Config SHA256 d4506d47c8482be44aa4b7f2d301b113529a9d9e3001421309b9d22b0ee2ac75.
Submitted fixed fold0 only as job965; no confirmation folds submitted.
Verified RUNNING on master, Requeue0/Restarts0, worker2 excluded; startup
confirms RTX5090 and frozen assignment digest. W&B initializing run zzcsyjs3:
https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/zzcsyjs3.
First score review at10–20 epochs; no result claimed at launch.
