# A27: rotation-range ablation on immutable A5

Only training augmentation rotation range changes5->10 degrees. Translation
remains .03, brightness .9–1.1. Preserve all architecture, losses, pretrained
initialization, batch2, AMP, dropout.3, optimizer/schedule, seed42, cache and
frozen split. Do not import A26 normalization or unrelated local edits.

Rationale: all A5 folds exhibit falling BCD DEV window means while training
loss declines. Rotation diversity may improve generalization, not proven.
Joint rotation10/translation.05 was rejected for excess mask clipping.

Before deployment, broaden paired mask-retention check from32 to128 FIT
studies (no DEV scores). Practical engineering gate: mean retained mask
mass>=.97, observed minimum>=.90, and<5% sampled transforms below .95.
These are campaign choices informed by the preliminary FIT diagnostic, not
clinical safety thresholds or guarantees of retained diagnostic information.
Abort this candidate if the broader check fails. Check source parity,
all manifests, config delta, regression tests and real-cache augmentation.

Fixed fold0 only, full50 epochs on RTX5090, exclude worker2 and Vesta,
no requeue. Only completed audited selected DEV Macro-F1>=.75 permits
fresh folds1–4, preserving screen0. CV5 acceptance mean>=.70, sampleSD<=.05,
min>=.65; aspiration mean>=.75. No ensemble or altered selection. Report
per-class F1/accuracy/QWK and rare-A limitation. Repeatedly tuned DEV is not
independent test. Review every10–20 epochs. Not submitted at registration.

## Preflight and launch

Broader128-study/512-view/16-draw FIT audit: rotation-only mean retention
.9773875427,min .9225813150,p05 .9524901330,fraction below95% .0213623047;
passes the recorded engineering gate. Parent mean .9848635228 and fraction
below95% .00048828125. Joint increase still rejected (.1403808594 below95%).

Immutable snapshot:
/slurmshared/Ngoc/code/hcmus-density-auggeo-dropout30-rotation10-20260921-v1.
Copied from A5; source/scripts/split byte parity PASS. Parsed config differs
only in arm metadata and rotation5->10. All five manifests validated;
real-cache four-view512 augmentation finite and within[0,1]. Full regression
16/16 PASS. Config SHA256
318550f0b028d22d3e5e65d44638802aabfdb8bd8949c97491b999725476ec03.
Submitted fixed fold0 as Slurm job964; no confirmation folds submitted.
Verified RUNNING on master, Requeue0/Restarts0,worker2 excluded; startup
confirms NVIDIA GeForce RTX5090 and unchanged assignment digest.
W&B initializing: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/wjz7dz8t.
Next planned result review10–20 epochs; no score claimed at launch.
