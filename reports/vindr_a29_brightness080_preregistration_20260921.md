# A29 preregistration: wider darkening augmentation on A5

Only learning change: brightness_min .9->.8; upper bound remains1.1,
rotation5/translation.03 unchanged. Parent immutable A5, not failed A28.
Architecture, losses, natural FIT sampling, dropout.3, optimizer/LR/AMP,
seed42, frozen grouped split, cache and50epochs remain unchanged.

Hypothesis: stronger photometric variability may reduce reliance on absolute
brightness. This is not established causality or a promised improvement.
FIT focal saturation at A5 selected checkpoint motivates a controlled
regularization test; gradient probes do not justify cutting auxiliary losses.
Inspected configs use .9–1.1 brightness; this lower-bound change is untested.
The distribution becomes asymmetric (mean factor .95 rather than1), so any
effect cannot be attributed to variance alone. Keeping upper bound avoids
increasing maximum bright-pixel saturation; geometry/cropping is unchanged.

Before launch: clone immutable A5 without deploying unrelated local edits;
verify parsed delta exactly lower brightness bound and arm metadata; verify
source and frozen manifest parity, run tests and real FIT-cache finite/range
preflight at both endpoints. Stop if data contract checks fail.
Run fixed fold0 full50 on RTX5090 only, never Vesta; exclude worker2.
Expand fresh folds1–4 only after completed auditPASS and selected DEV>=.75,
retain original fold0. Joint final acceptance mean>=.70/sampleSD<=.05/
min>=.65; mean>=.75 aspiration. No ensemble or changed checkpoint selection.
Selected DEV is not independent test; six A cases limit conclusions.
Review10–20epoch intervals. No training job submitted at registration.

## Deployment

Cloned immutable A5 to
/slurmshared/Ngoc/code/hcmus-density-auggeo-dropout30-brightness080-20260921-v1.
Parsed config delta and byte parity for source/scripts/frozen split PASS.
Real FIT cache four-study endpoint checks at.8/1.1 finite,shape/range PASS.
Snapshot unittest discovery exit0. Config SHA256
b4be21b0db70a9ca2797a9e54ecb826d9971ec7b9a73eca030b0119ca4230182.
Submitted fixed fold0 only as job976, no confirmation folds submitted.
