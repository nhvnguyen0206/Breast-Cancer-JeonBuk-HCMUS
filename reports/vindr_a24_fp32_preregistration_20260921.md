# A24: A5 FP32 training

Registered after A23 completed50 and failed its audited .75 screen gate.
Direct parent A5; only training.amp true->false and arm metadata change.
The existing engine disables CUDA autocast and GradScaler when amp=false.
Architecture, losses, augmentation, optimizer, batch2, seed42, frozen split,
cache, checkpoint selection and single-model inference remain as in A5.

Hypothesis: changing training precision may improve numerical behavior and
optimization. Sparse skipped AMP updates do not establish a cause of poor
F1. A18's FP16 failure involved a different BN policy and is not evidence
that A5 has the same forward failure. No improvement is assumed.

Real batch2/512 FP32 forward/backward/update preflight passed on RTX5090,
peak allocation5.1951GiB; see vindr_precision_candidate_20260921.md.

Run fresh ImageNet fixed fold0 full50 first. Expand to folds1--4 only if
completed audited selected DEV Macro-F1>=.75. Preserve the screen fold0.
RTX5090 only; exclude worker2/Vesta. No requeue. W&B HCMUS-paper1.
Final acceptance mean>=.70, sample SD<=.05, min>=.65; aspirational mean .75.
Report class F1, accuracy, QWK and numerical failures. Selected DEV is not
an independent test. Six A studies limit evidence on rare-class stability.
