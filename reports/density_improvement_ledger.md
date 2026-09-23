# Active density improvement goal

Target: mean four-class Macro-F1 >= 0.75 across the fixed density CV5 protocol,
with stability checked across fixed folds using training seed 42 only. The target has **not been met**.
Do not declare success from a single favorable fold, a pooled metric alone,
or predictions on the six class-A studies alone.

## A25 screen launched (2026-09-21)

After completed A24 failed stability acceptance, return to immutable A5 and
change only neighbor loss coefficient .2 -> .1. No architecture/selection
change. Preregistration: vindr_a25_neighbor010_preregistration_20260921.md.
Source/split parity and semantic config delta verified;16 regression tests
PASS. Fixed fold0 job962_0 is RUNNING on master, worker2 excluded, no requeue.
W&B vjgvwnx6. Run50 epochs; expand folds1–4 only after completed audited
screen Macro-F1>=.75. No result yet. Next review10–20 epochs.

A25 first10: selected epoch4 Macro .7063473821, accuracy .8019801980,
QWK .6636976609. Gain over matched A5 is concentrated in A; BCD mean
.719574 versus .726998. Epoch10 drops to .510332 with excess A predictions.
Below .75 gate; continue unchanged50, no confirmation. Report:
vindr_a25_neighbor010_first10_20260921.md. Next review20.

A25 first20: no new best since epoch4 (.7063473821), below matched A5
.7654421855 and .75 gate. Epoch20 .5377401184; finite losses,9 AMP skips.
Continue full50, no confirmation, next review30. Exact report:
vindr_a25_neighbor010_first20_20260921.md.

A25 first30: selected remains epoch4 .7063473821, below matched A5
.7896498562. Epoch30 .4968663673, finite losses,12 AMP skips. Continue
full50 unchanged, no confirmation. Next40; report
vindr_a25_neighbor010_first30_20260921.md.

A25 first40: selected remains epoch4 .7063473821, below .75 gate;
epoch40 .5083610974, finite losses,14 AMP skips. Continue unchanged50 then
audit; no confirmation. Report: vindr_a25_neighbor010_first40_20260921.md.

A25 completed50 screen audit PASS, job962_0 COMPLETED ExitCode0:0,
W&B vjgvwnx6 finished. Selected epoch4 Macro .7063473821, accuracy
.8019801980, QWK .6636976609; epoch50 .4974975682,16 AMP skips,
zero/50 checkpoints>=.75. Reject without folds1–4. Exact report:
vindr_a25_neighbor010_screen_20260921.md. No subsequent job submitted yet.

Post-A25 FIT-only diagnostic: weighted binary CE normalizes by batch weights;
~82% homogeneous batch2 pairs cancel class weights. Expected AB coefficient
mass ~.1605 vs .3634 with fixed FIT normalization (not measured gradients).
Candidate A26: opt-in binary FIT normalization on immutable A5; not yet
implemented/submitted. Evidence and test requirements:
vindr_binary_batch_normalization_diagnostic_20260921.md.

A26 launched after immutable-A5 source parity, config-only normalization
delta, frozen-manifest validation, full regression exit0 and real-cache CPU
finite forward/backward. Fixed fold0 job963_0 RUNNING on master RTX5090;
W&B hpzf3sq6 initializing. No confirmation until completed audited>=.75.
Preregistration: vindr_a26_binarynorm_preregistration_20260921.md.

A26 first10: selected epoch7 Macro .6867574622, accuracy .7970297030,
QWK .6292416510; apparent gain over matched A5 driven by A, BCD lower.
Epoch10 .6250497810; finite losses,7 AMP skips, below .75 gate. Continue
full50 unchanged; next20. Report: vindr_a26_binarynorm_first10_20260921.md.

A26 first20: best remains epoch7 .6867574622, below matched A5 .7654421855
and .75 gate. Epoch20 .5151554315; finite losses,9 AMP skips. Continue50
unchanged, no confirmation, next30. Report: vindr_a26_binarynorm_first20_20260921.md.

A26 first30: selected epoch23 .7467283694, still strictly below .75 gate;
accuracy .7797029703, QWK .5878118122, F1 [1,.56,.8519134775,.575].
Epoch30 .5086044924; finite losses,12 AMP skips. Continue50 unchanged,
no confirmation, next40. Report: vindr_a26_binarynorm_first30_20260921.md.

A26 first40: best remains epoch23 .7467283694, strictly below .75 gate;
epoch40 .5156740957, finite losses,15 AMP skips. Continue50 unchanged then
audit; no confirmation. Report: vindr_a26_binarynorm_first40_20260921.md.

## Frozen comparison protocol

A28 first30: selected remains epoch11 Macro .7645251627; below parent
A6 .7829792575. Epoch30 .5412416090, finite losses,13 AMP skips. Continue
unchanged50 then audit before confirmation, next40. Report:
vindr_a28_sampling025_wd1e2_first30_20260921.md.

A28 first20: selectedepoch11 Macro .7645251627, accuracy .8292079208,
QWK .6047078843, still below parent A6 .7829792575. Epoch20 .6860569986,
finite losses,11 AMP skips. Continue unchanged full50 and audit before
confirmation; next30. Report vindr_a28_sampling025_wd1e2_first20_20260921.md.

A28 first10: selectedepoch7 Macro .7579900045, accuracy .8168316832,
QWK .5947294220; provisionally>=.75 but below A6 .7829792575, with lower
B/D F1. Epoch10 .6149738923, finite losses,7 AMP skips. Continue unchanged
full50 then audit before confirmation; no folds1–4 submitted. Next20.
Report vindr_a28_sampling025_wd1e2_first10_20260921.md.

A28 submitted job965 fold0: immutable A6 plus weight_decay .0001->.01
only. Source/config/split parity, all manifests,16 tests and real-cache
augmentation PASS; float32 decay initial-LR effect verified. Full50,
RTX5090 launcher, worker2 excluded, no requeue; expand only after completed
audited>=.75. No result yet. Details:
vindr_a28_sampling025_wd1e2_preregistration_20260921.md.

Post-A27 review recomputed20 unique completed audited-schema CV5 arms:
none meets joint acceptance. A6 remains strongest stability tradeoff;
BCD SD .0209 versus four-class .0644. Prior ordinal-floor diagnosis and
failed A13 already address the scalar-loss question; do not repeat.
Next candidate: effective decay.01 on A6 (not A5), pending preregistration
and deployment checks. No job submitted. Evidence:
vindr_post_a27_campaign_review_20260921.md.

A27 completed50 screen audit PASS; job964_0 COMPLETED ExitCode0:0,
W&B wjz7dz8t finished. Selected epoch16 Macro .6751496227, accuracy
.7995049505,QWK .6115753490;epoch50 .5332049654,17 AMP skips,
zero/50 epochs>=.75. Reject rotation10; no confirmation folds or next job.
Exact report vindr_a27_rotation10_screen_20260921.md.

A27 first40: selected remains epoch16 Macro .6751496227, below .75 gate
and matched A5 .7896498562. Epoch40 .5306800395, finite losses,15 AMP
skips. Continue unchanged50 then audit; no confirmation. Report:
vindr_a27_rotation10_first40_20260921.md.

A27 first30: selected remains epoch16 Macro .6751496227, below matched
A5 .7896498562 and .75 gate. Epoch30 .5363996246, finite losses,14 AMP
skips. Continue unchanged50, no confirmation, next40. Exact report:
vindr_a27_rotation10_first30_20260921.md.

A27 first20: selectedepoch16 Macro .6751496227, accuracy .7995049505,
QWK .6115753490; below matched A5 .7654421855 and .75 gate. Epoch20
.5745552561; finite losses,10 AMP skips. Continue unchanged50, no
confirmation. Next30; report vindr_a27_rotation10_first20_20260921.md.

A27 first10: job964 RUNNING, bestepoch10 Macro .5906979830, accuracy
.8366336634,QWK .6769409712, classes [.25,.5,.9044585987,.7083333333].
Four-class gain over matched A5 is A-driven; BCD mean .704264 below .726998.
Finite losses,7 AMP skips. Continue unchanged50, no confirmation; next20.
Report vindr_a27_rotation10_first10_20260921.md.

A27 registered and submitted as job964 fold0 after broader128-study FIT
retention gate, source/config parity, manifest validation,16/16 tests and
real-cache augmentation preflight. Only rotation5->10 on immutable A5;
translation remains .03. Full50, RTX5090 launcher, worker2 excluded,
no requeue; no confirmation until completed audited>=.75. Details:
vindr_a27_rotation10_preregistration_20260921.md. No result yet.

FIT-only geometry audit (32 studies/128 masks,16 paired draws,seed42):
parent5deg/.03 mean retention .98478; proposed10deg/.05 .97025 with14.45%
of transforms retaining<95%, versus parent .146%. Do not launch joint
increase. Rotation-only10deg/.03 mean .97722,2.39% below95%; not yet approved
for training. Reproducible script and limitations in
vindr_augmentation_retention_20260921.md. No next job submitted.

Post-A26 read-only A5 history diagnostic: every fold shows lower training
loss but lower BCD DEV mean in epochs41–50 versus1–10 (decline1.11–3.20pp).
This is consistent with a generalization problem beyond scarce A support,
not causal proof. Candidate: stronger geometric augmentation on immutable
A5, pending transform/mask-retention checks; no launch. Evidence:
vindr_a5_temporal_generalization_20260921.md.

A26 completed50: screen audit PASS; job963_0 COMPLETED ExitCode0:0,
no restarts, W&B hpzf3sq6 finished. Selected epoch23 Macro-F1
.7467283693843594 is strictly below .75; zero eligible epochs. Reject
without folds1–4. Accuracy .7797029703, QWK .5878118122,
class F1 [1,.56,.8519134775,.575]; BCD mean .6623044925.
Epoch50 Macro-F1 .5070203259;17 AMP skipped updates. Frozen manifests
validated, assignment SHA unchanged. Full report:
vindr_a26_binarynorm_screen_20260921.md. No next arm submitted.

- Population: the same 2,017 four-view studies; six A studies total.
- Split: `vindr_density_cv5_seed42_v1`, split seed 42 unchanged.
- Canonical case/label/component/fold SHA256:
  `e9b851771108792d83b12246f8aa97aba0e9e1ae5ac3f926351e5985778806df`.
- Cluster assignment-file SHA256:
  `43daa86936ee7b1bae1b200836fb1afdfe0c8294c7c865d8f5758bf989f12a9a`.
- Updated user protocol: screen each arm on fixed fold 0, 50 epochs, training
  seed 42. Only after four-class DEV Macro-F1 reaches 0.75 run five-fold
  confirmation. Never switch screening folds to obtain a favorable score.
  A screening pass is not goal completion; inspect class-A sensitivity too.
- Primary comparison: mean per-fold four-class DEV Macro-F1 at selected epochs.
  Also report fixed-epoch-50 metrics, paired fold deltas, sample SD, per-class
  F1/support, B/C/D-only descriptive F1, accuracy, QWK, and pooled confusion.
- Selection uses DEV, so results are development estimates, not independent
  final-test results. Prior development exposure must remain disclosed.
- W&B project: `TN_Mammo_BreastDensity/HCMUS-paper1`.
- RTX 5090 only; Vesta / `slurm-b40a-worker-2` explicitly excluded.

## B0: completed baseline

Direct stretch resize to 512 square, natural-frequency sampling, current
class-balanced focal + ordinal/binary/neighbor objective. Original DenseNet121
and relational fusion unchanged.

Mean best DEV Macro-F1 0.6012498 (sample SD 0.0561879), accuracy 0.8185502,
QWK 0.6203942. Fixed-epoch-50 mean Macro-F1 0.5185930.
Full results: [baseline](vindr_density_cv5_results_20260918.md).
Selected run IDs: phfsagbm, ecgddcce, m7d1pybx, z2c15901, ps6qqkst.

## L1: letterbox-only ablation — CV5 completed, target not met

- Slurm array **720**, tasks `720_0` through `720_4`.
- Output roots: `/slurmshared/Ngoc/runs/hcmus-density-cv5-v1-720-fold{i}`.
- Logs: `/slurmshared/Ngoc/logs/hcmus-density-cv5-720_{i}.log`.
- W&B group: `vindr-densityCV5-v1-letterbox-seed42-full50`.
- Following the user's protocol update, tasks 720_1 through 720_4 were
  explicitly cancelled; their partial outputs are retained, not final results.
  Task 720_0 continues on slurm-b20a-master-0 (RTX 5090).
- Fold-0 W&B: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/4lbfmjyc
- Interrupted fold 1–4 run IDs: p4t7ydzv, j7sv4zzv, 4enzjcdg, j6fglfc5.
- Initial check: all five reached epoch 3 with cloud logging before the
  cancellation. Fold-0 epoch-3 Macro-F1 was 0.545595; this is provisional.

- Config: `configs/vindr_density_letterbox.yaml`.
- Change: preserve aspect ratio with area interpolation and centered zero
  padding before brightness augmentation and ImageNet normalization.
- Unchanged: seed, input size, cache, split, architecture, loss, batch size,
  sampling, brightness augmentation, optimizer and 50-epoch schedule.
- Default old-config behavior remains stretch; inference obtains resize mode
  from the checkpoint. DICOM mode rejects unsupported letterbox use explicitly.
- Independent code deployment:
  `/slurmshared/Ngoc/code/hcmus-density-letterbox-20260918-v1`.
- Data and dependency symlinks point to the immutable prior deployment; the
  original source deployment and cache were not altered.
- All eleven tests passed, including backward-compatible stretch pixels,
  letterbox geometry, cache training and checkpoint/inference parity.
- Remote preflight verifies all five manifest payloads/hashes and reads a
  real FIT tensor with shape `[4,3,512,512]`.

Risk: aspect preservation removes distortion but padding makes breast content
occupy less of the square; better F1 is a hypothesis, not an assumption.

## F1: FIT-expectation focal normalization — retry completed, screening not passed

- Config: `configs/vindr_density_focalnorm.yaml`; Slurm task **725_0**.
- Deployment: `/slurmshared/Ngoc/code/hcmus-density-focalnorm-20260918-v1`.
- Output: `/slurmshared/Ngoc/runs/hcmus-density-cv5-v1-725-fold0`.
- W&B group: `vindr-densityCV5-v1-focalnorm-seed42-full50`.
- W&B run: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/78xotjy2
- Isolated comparison against B0, not L1: retain original stretch resize,
  architecture, natural sampling, class-weight ratios, all auxiliary terms,
  seed 42, optimizer and full 50 epochs. Only normalize focal scale by its
  fixed expected class weight under FIT class frequencies.
- FIT counts verified remotely: A=5, B=156, C=1245, D=207.
  Expected weight is 0.0571813248, giving a fixed focal multiplier of ~17.49.
  No DEV labels/frequencies are used in this denominator. No per-batch
  normalization (batch size is two). Default old loss behavior is unchanged.
- Rationale: class-mean normalization leaves natural-frequency mean weight
  far below one. L1 epoch 3 focal=0.0798 versus weighted ordinal=0.5501;
  loss values alone do not prove gradient dominance or causality. This arm
  tests the relative scale hypothesis, not a guaranteed fix.
- Risks: rare-A memorization and larger/less stable gradients. Monitor skipped
  AMP updates and per-class errors; inspect B/C/D changes, not A alone.
- All 12 tests passed; test checks exact scaling, unchanged auxiliary terms,
  finite backward gradients, and default compatibility. Baseline config
  parity and frozen assignment hash verified before submission.
- Initial allocation confirmed slurm-b20a-master-0, excluding Vesta.
  L1 and F1 are separate simultaneous single-fold experiments, not CV5 runs.
- Latest L1 observation when F1 started: 7 epochs, best Macro-F1 0.580687
  at epoch 7. Per-class F1 [0.4000, 0.4348, 0.8903, 0.5977]. Provisional,
  below the fold-0 B0 best of 0.682793 and below the screening gate.

## Next actions after screening completes

### Prepared, not launched: tempered FIT sampling

Local engine supports `training.sampling_power`: default 0 preserves natural
shuffle without replacement; 0.5 uses inverse-square-root frequency weights;
1 gives equal expected class mass. Nonzero power samples with replacement,
exactly FIT-size draws per epoch, using a dedicated seed-controlled generator.
All weights come from FIT only. DEV remains unchanged and is never resampled.
Realized class draws are logged in history and W&B for future runs.

Fold-0 expected draws at power 0.5: [56.01, 312.84, 883.78, 360.37]
versus natural [5, 156, 1245, 207]. This increases exposure, not independent
support; rare-A memorization remains a concern. Existing class-balanced focal
weights also favor rare classes, so any sampling arm must disclose their
combined effect rather than silently normalizing loss a second time.
No sampling job/config has been launched and neither live deployment changed.
Choose its parent configuration after L1/F1 evidence is available.

### Interim health check (not final results)

Both 720_0 and 725_0 were re-polled live on slurm-b20a-master-0.
At L1 epoch 9 / F1 epoch 1, L1 best remains 0.580687; F1 epoch-1
Macro-F1 is 0.525880, accuracy 0.824257, QWK 0.625261, per-class F1
[0, 0.555556, 0.887097, 0.660870]. F1 loss is finite; 8 initial AMP updates
were skipped and require tracking over subsequent epochs, not a restart.
Neither arm has passed the 0.75 gate. Keep both existing handles running;
do not add CV folds or modify their deployed configurations mid-run.

Later verified wait: L1 reached 14/50 epochs, F1 6/50; both still RUNNING
on the same allowed node. Best scores remain L1 0.580687 (epoch 7), F1
0.566861 (epoch 3). F1 per-class F1 is [0, 0.686869, 0.900164, 0.680412],
accuracy 0.846535, QWK 0.691071. Descriptive mean of B/C/D F1 at this
checkpoint is 0.755815, versus B0's selected checkpoint 0.688169. This is
not the four-class target, not an independently selected B/C/D comparison,
and not proof that the completed experiment improves overall performance.
Continue the full runs before selecting the next parent configuration.

### F1 infrastructure failure and retry

Task 725_0 was subsequently confirmed FAILED by Slurm (ExitCode 1:0), after
six complete epochs, during validation in epoch 7. Error: DataLoader worker
could not unlink `/torch_...` shared memory file (ENOENT). No nonfinite loss
was reported. The shared-memory filesystem was only 1% used when inspected;
the cause of the missing object is not established. Do not call it OOM.

Mitigation: set `training.valid_num_workers: 0` for F1 only, eliminating
validation worker IPC. Keep training workers=4 and sampling_power default=0.
New deployment `/slurmshared/Ngoc/code/hcmus-density-focalnorm-20260918-v2`.
All 14 tests pass, including identical validation predictions and equal
post-validation torch RNG state for workers=0 versus workers=2 on synthetic
cache. Actual cluster trajectory will also be compared where available.
This prevents the observed validation path; FIT worker IPC remains and must
still be monitored. Existing L1 code/deployment is untouched.

Retry is fresh ImageNet initialization, seed 42, all 50 epochs on fold 0;
not a resume from best.pt (no optimizer/resume state was saved). Preserve
725 outputs and W&B 78xotjy2 as an incomplete failed attempt, exclude it
from completed-arm comparisons. Local sampling support is present in v2
but disabled, so no imbalance sampling treatment is added to this retry.

Retry task **726_0** confirmed RUNNING on slurm-b20a-master-0; GPU startup
check confirms RTX 5090. W&B run:
https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/h7csqjkr
Output `/slurmshared/Ngoc/runs/hcmus-density-cv5-v1-726-fold0`;
log `/slurmshared/Ngoc/logs/hcmus-density-cv5-726_0.log`.
Active handles are now 720_0 (L1) and 726_0 (F1 retry), NOT 725_0.

### L1 fold-0 gate passed; confirmation authorized by threshold

At epoch 16, L1 fold 0 reached Macro-F1 **0.7571777706**, accuracy
0.777227723, QWK 0.604920028; per-class F1
[1.0, 0.594059406, 0.846416382, 0.588235294]. The checkpoint, prediction
CSV, DEV membership/labels, probabilities and recomputed metrics were checked
and agree. This passes the user's single-fold screening gate, NOT the goal.

Class-A caveat: the only DEV A case is correct with no false-A predictions.
Mean B/C/D F1 is ~0.676237, below B0's selected ~0.688169. The total
Macro-F1 gain over B0 fold 0 is driven by A, so evidence is weak until
cross-fold and multi-seed confirmation. Do not present this as a robust gain.

Submitted **727_1 through 727_4**, 50 epochs each, to complete L1 CV5.
Fold 0 continues as **720_0**, without restart or duplicate. Previously
cancelled 720_1–4 remain excluded. All confirmation manifests verified.
Use the identical original L1 deployment/config (including validation workers
4) for direct comparability; monitor for worker IPC failures. No F1 or sampling
changes are included. Slurm explicitly excludes Vesta.
Outputs: `/slurmshared/Ngoc/runs/hcmus-density-cv5-v1-727-fold{i}` for i=1..4.
W&B group stays `vindr-densityCV5-v1-letterbox-seed42-full50`.
All four confirmation tasks verified RUNNING on slurm-b40a-worker-1, each
logging `Allocated GPU: NVIDIA GeForce RTX 5090`, no startup traceback.
W&B IDs (fold 1..4): **pcruvhxl, wqxdgc1u, 3epkvxx9, rx2441bh**.
Together with fold 0 **4lbfmjyc**, these are the five active L1 run handles.

F1 retry parity: epoch-1 training component values and validation metrics
exactly match failed attempt 725, after the validation-worker mitigation.
Subsequent checks verified exact training-component and validation-metric
parity across all six overlapping epochs (725 vs 726). Retry 726 completed
epoch 7, passing the original failure point, with finite loss and zero skipped
AMP updates that epoch; it remains RUNNING. This confirms the observed path
was avoided, not that all future IPC failures are impossible.
All four L1 confirmation tasks also matched training/validation values for
the first three overlapping epochs of their cancelled 720 attempts.

### L1 fold 0 completed (not CV5 completion)

720_0 is COMPLETED, ExitCode 0:0, runtime 50m37s. History contains all 50
epochs; W&B 4lbfmjyc is finished, completed_epochs=50, stopped_early=False.
Checkpoint epoch/metrics equal the history maximum and W&B summary.
Best is epoch 16: Macro-F1 0.7571777706, accuracy 0.777227723,
QWK 0.604920028, per-class F1 [1, 0.594059406, 0.846416382, 0.588235294].
At epoch 50: Macro-F1 **0.4909769677**, accuracy 0.794554455,
QWK 0.556032200, per-class F1 [0, 0.564705882, 0.868589744, 0.530612245].
Thus passing the screening gate was not sustained through the final epoch.
The selected peak and tiny class-A support require caution; no goal success
or multi-seed confirmation is established. 727_1–4 and 726_0 remain RUNNING.
Do not restart 720_0 or replace its completed output.

## S1: tempered sampling — completed, screening not passed

After L1 fold-0 completion demonstrated a fragile A-driven peak and poor
final-epoch performance, screen the independent imbalance hypothesis against
the completed B0 reference; do not adopt L1 or unfinished F1 as the parent.

- Config `configs/vindr_density_sampling.yaml`, arm `sqrt_sampling`.
- Task **731_0**, fold 0 only, fresh seed-42 ImageNet, 50 epochs.
- Deployment `/slurmshared/Ngoc/code/hcmus-density-sampling-20260918-v1`.
- Output `/slurmshared/Ngoc/runs/hcmus-density-cv5-v1-731-fold0`.
- W&B group `vindr-densityCV5-v1-sqrt_sampling-seed42-full50`.
- W&B run https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/h32uqkzx
- Startup verified RUNNING on slurm-b20a-master-0 with RTX 5090.
- Only learning treatment vs B0: sampling_power=0.5, replacement FIT draws
  with inverse-square-root frequency weights; 1,613 draws each epoch.
- Baseline stretch resize, model, class-balanced loss, all auxiliary losses,
  optimizer, augmentation and schedule unchanged. No focal normalization.
- Runtime mitigation valid_num_workers=0 retained; previous six-epoch F1
  parity established this preserves the training trajectory. FIT workers=4.
- All 14 tests pass; baseline configuration parity, remote manifest hash and
  exact expected draw counts verified. Slurm excludes Vesta.
- Risks: repeated rare examples may overfit; existing class weights and
  sampling both favor rare classes. Record actual class draws and B/C/D
  metrics rather than treating an A-only improvement as sufficient evidence.
- Do not expand S1 to other folds unless its four-class Macro-F1 reaches .75.
  Existing L1 confirmation and F1 retry are unmodified.

Initial S1 observation: epoch 1 Macro-F1 0.708668115, accuracy 0.831683168,
QWK 0.661341223, per-class F1 [0.666667, 0.595745, 0.891410, 0.680851].
Actual sampled counts epoch 1 [47,306,883,377], epoch 2 [61,329,866,357],
both exactly 1,613 draws, consistent with the intended stochastic sampler.
Epoch 2 had zero skipped AMP updates. This early result is below the .75
screening gate and is not a completed-run or cross-fold success claim.

## F1 completed outcome (2026-09-19)

Retry 726_0 / W&B h7csqjkr completed all 50 epochs; cloud state finished,
completed_epochs=50, stopped_early=False. Checkpoint matches history maximum.
Best epoch 3: Macro-F1 **0.5668611810**, accuracy 0.8465346535,
QWK 0.6910705476; per-class F1 [0, 0.686868687, 0.900163666, 0.680412371].
Epoch 50: Macro-F1 **0.5565711270**, accuracy 0.8589108911,
QWK 0.6632151632; per-class F1 [0, 0.708860759, 0.912772586, 0.604651163].
Against B0 fold-0 best 0.6827931034, four-class Macro-F1 regressed despite
better descriptive B/C/D mean at selected checkpoints. It did not pass the
screening gate, so do NOT launch F1 folds 1–4. Keep this negative result;
do not adopt full-strength focal expectation normalization as an improvement.
L1 confirmation 727_1–4 and S1 screening 731_0 remain in progress.

## O1: lower learning rate — screening passed; CV5 confirmation launched

- Config `configs/vindr_density_lr1e5.yaml`; task **732_0**, fold 0, seed 42,
  50 epochs, natural sampling and baseline stretch resize.
- Only learning treatment vs B0: initial AdamW LR 1e-5 instead of 5e-5;
  same 50-epoch cosine schedule. All architecture/loss/augmentation/weight
  decay settings remain baseline. Do not mix in F1 normalization or S1 sampling.
- Rationale: B0/L1 peaks deteriorate later; test whether smaller updates
  retain useful pretrained features and reduce fluctuations. This is a
  hypothesis, not proof of the cause; reduced LR may instead underfit.
- Runtime mitigation validation workers=0 retained, FIT workers=4. Existing
  validated code unchanged; only new config. Automated configuration parity
  check and cluster fold manifest/hash validation passed before submission.
- Deployment `/slurmshared/Ngoc/code/hcmus-density-lr1e5-20260919-v1`.
- Output `/slurmshared/Ngoc/runs/hcmus-density-cv5-v1-732-fold0`.
- W&B group `vindr-densityCV5-v1-lr1e5-seed42-full50`.
- W&B run https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/a7d4bt0w
- Startup verified RUNNING on slurm-b20a-master-0, GPU RTX 5090.
- RTX 5090 required by launcher, Vesta excluded. Do not expand beyond fold 0
  unless four-class Macro-F1 reaches .75. Prior runs remain unmodified.

### O1 screening gate passed at epoch 13

Fold 0 best Macro-F1 **0.7968110413**, accuracy 0.8366336634,
QWK 0.6606597434; class F1 [1, 0.725274725, 0.893548387, 0.568421053].
Checkpoint/prediction metrics, finite normalized probabilities/argmax,
DEV membership/labels and all confirmation manifests verified.
Descriptive B/C/D mean ~0.729081, versus B0 selected ~0.688169;
unlike L1 fold 0, not solely an A improvement. However A still has only one
DEV case, and D F1 declines versus B0. This remains a screening result.

Submitted **733_1–4**, fresh seed 42, 50 epochs each, identical O1 code/config.
Fold 0 continues as **732_0**, no duplicate. Vesta excluded. Outputs
`/slurmshared/Ngoc/runs/hcmus-density-cv5-v1-733-fold{i}` for i=1..4;
W&B group `vindr-densityCV5-v1-lr1e5-seed42-full50` unchanged.
S1 731_0 continues independently; no sampling change is included in O1.
Goal not met until full CV5 and multi-seed stability are established.
All four tasks verified RUNNING on slurm-b40a-worker-1 with RTX 5090 startup
checks and no startup traceback. W&B IDs fold 1..4:
**77eq4ie2, tjwdppss, vsh65hkq, 8rvtdj1d**; fold 0 remains **a7d4bt0w**.

## S1 completed outcome (2026-09-19)

731_0 COMPLETED, exit 0:0, runtime 57m44s; W&B h32uqkzx finished, all 50
epochs, no early stop. Verified checkpoint/history/prediction metric agreement,
exact frozen DEV membership/labels and finite normalized argmax probabilities.
Every epoch had 1,613 FIT draws; mean realized A/B/C/D counts were
[56.96,312.80,881.22,362.02], matching intended sampling in expectation.

Best epoch **1**: Macro-F1 **0.7086681150**, accuracy 0.8316831683,
QWK 0.6613412229; per-class F1 [0.666667,0.595745,0.891410,0.680851].
Epoch 50: Macro-F1 **0.5443640240**, accuracy 0.8514851485,
QWK 0.6426465385; per-class F1 [0,0.64,0.908243,0.629213].
Best exceeds B0 fold 0 by ~2.59 pp with the same A F1, but is below the
0.75 gate and not sustained. Do NOT launch additional S1 folds. Retain
sampling as a possible component for future controlled arms, not as a proven
CV5 improvement. Class A is again missed at epoch 50 despite more exposure.

Active handles: O1 fold 0 732_0 plus 733_1–4. No S1/L1/F1 job remains live.

1. Verify each live Slurm/W&B handle before any retry; do not duplicate jobs.
2. Compare screening fold 0 against B0 fold 0, including class-A sensitivity and
   metrics excluding A descriptively. If screening reaches Macro-F1 0.75,
   confirm all five folds against B0; retain the four-class target metric.
3. Isolate imbalance experiments (sampling and/or loss scaling) as their own
   arms, followed by optimizer/freeze/augmentation ablations as evidence warrants.
   Do not combine unrelated changes or silently alter the fold roster.
4. Validate any promising candidate on additional training seeds (e.g. 43/44)
   with the same split seed and all five folds. Record unsuccessful arms too.

No changes to clinical claims, dataset membership, labels, or held-out roles
are authorized by merely pursuing the numerical target.

## Completed L1 CV5 decision (2026-09-19)

All five runs finished 50 epochs, verified with W&B, histories, checkpoints
and prediction CSVs. Mean selected Macro-F1 **0.619073373 ± 0.080752855**
(sample SD), versus B0 0.601249756 ± 0.056187877. Mean accuracy 0.811123259,
QWK 0.612618612; fixed-epoch-50 mean Macro-F1 0.499134444. Target not met.
Descriptive B/C/D F1 declines in four of five paired folds; pooled Macro-F1
also declines (0.608766489 vs B0 0.615557360). Do not interpret the A-driven
screening peak as a robust gain or launch extra seeds for L1 alone now.
Full audit: [L1 results](vindr_letterbox_cv5_results_20260919.md).
At that earlier snapshot S1 731_0 and O1 732_0 were active; S1 has since
completed as audited above, and O1 expanded to 733_1–4.

## R1 backbone warm-up screening launched (2026-09-19)

Controlled B0 comparison: freeze DenseNet features (weights AND BatchNorm
statistics) for epochs 1–5; train fusion/heads normally, unfreeze all features
from epoch 6. Same baseline LR 5e-5, loss, natural sampling, stretch resize,
architecture, frozen fold 0 membership and training seed 42. Cosine schedule
runs continuously over 50 epochs, with no reset at unfreeze. Validation uses
zero workers as in the previously parity-verified runtime mitigation.
Not combined with O1 lower LR or S1 sampling.

Config: `configs/vindr_density_warmup.yaml`, arm `warmup5`.
All 15 local tests passed (20.879 s), including an actual optimizer-step test
proving frozen weights/BN unchanged while heads update, and backbone weights/
BN update after unfreezing. Remote configure validated the frozen manifest
hash and baseline config parity apart from the documented treatment/runtime.

Submitted screening job **737_0** only, full 50 epochs, RTX 5090 required and
Vesta excluded. Deployment:
`/slurmshared/Ngoc/code/hcmus-density-warmup-20260919-v1`.
Output: `/slurmshared/Ngoc/runs/hcmus-density-cv5-v1-737-fold0`.
W&B group: `vindr-densityCV5-v1-warmup5-seed42-full50`.
Startup confirmed RUNNING on slurm-b20a-master-0 with NVIDIA RTX 5090;
Slurm explicitly excludes slurm-b40a-worker-2. W&B run:
https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/iilc5qpu
First epoch completed with `backbone_frozen=true`, natural FIT counts
[5,156,1245,207], finite loss, Macro-F1 0.36922757; four AMP skipped updates
recorded (not hidden). This initial warm-up result is not a final comparison.
Runtime transition verified: epochs 1–5 recorded `backbone_frozen=true`;
epoch 6 recorded `backbone_frozen=false`, zero AMP-skipped updates and finite
loss. Its DEV Macro-F1 was 0.559847495 (best so far), versus 0.505122296 at
epoch 5. This proves the deployed run crossed the intended unfreeze boundary;
it does not yet establish an accuracy gain.
Do not expand unless fixed fold 0 reaches four-class Macro-F1 0.75; inspect
per-class changes and rare-A sensitivity before interpreting any gain.

O1 jobs **732_0, 733_1–4** remain live and their deployed code is unchanged.
Latest verified O1 histories: fold 0 epoch 34, other folds epoch 15; full CV5
outcome is not yet available. Goal remains unproven.

### O1 fold 0 completed and audited (2026-09-19)

Job **732_0** COMPLETED exit 0:0 after 57m34s. W&B `a7d4bt0w` is `finished`,
reports 50 completed epochs and no early stop. Verified an exact 1..50 history,
checkpoint epoch/metrics equal to the history maximum, 404 unique prediction
rows exactly matching frozen fold-0 DEV IDs and labels, finite normalized
probabilities, probability argmax equality, and recomputed metrics equality.
The checkpoint retains arm `lr1e5`, LR 1e-5 and the registered assignment hash.

Selected epoch 13 remains Macro-F1 **0.7968110413**, accuracy 0.8366336634,
QWK 0.6606597434, per-class F1 [1,0.725275,0.893548,0.568421]. Epoch 50 was
Macro-F1 **0.5299639193**, accuracy 0.8292079208, QWK 0.6246768634 and class
F1 [0,0.630435,0.891720,0.597701]. The large selected-to-final gap and the
single A case make this a volatile DEV result. Folds 1–4 (733) continue; do
not claim a CV5 result until all are complete and audited.

Provisional A-probability diagnostic on each fold's currently selected O1
checkpoint (not a new inference rule): fold 0 true A had p(A)=0.514 and ranked
above every non-A case; fold 2 true A had p(A)=0.620 but one non-A case ranked
higher and became a false A. Missed true-A cases were not consistently just
below argmax: fold 1 p(A)=0.138 (rank 3 among non-A), fold 3 p(A)=0.068/0.027
(ranks 7/12), fold 4 p(A)=0.096 (rank 3). Therefore a simple fixed A threshold
would introduce false positives and cannot be claimed as a reliable fix. Repeat
this diagnostic after folds 1–4 finish because their selected checkpoints may
still change.

## A1 mild geometric augmentation screening launched (2026-09-19)

Controlled B0 comparison: retain the existing shared brightness multiplier and
add one exam-consistent affine transform to all four views: rotation uniformly
within +/-5 degrees and horizontal/vertical translation within 3% of the image
dimensions, bilinear interpolation and zero fill. No flip, crop or intensity
change beyond B0 brightness. Same stretch resize, natural sampling, loss,
LR 5e-5, model, fold 0 roster and seed 42. Validation is unaugmented.

Config: `configs/vindr_density_auggeo.yaml`, arm `auggeo`. All 16 local tests
passed (21.510 s), including shared-transform/range validation. Baseline config
parity and the fixed remote assignment hash were checked before submission.

Submitted screening job **738_0** only, full 50 epochs. Startup confirmed on
slurm-b40a-worker-3 with NVIDIA RTX 5090; Vesta is excluded. Deployment:
`/slurmshared/Ngoc/code/hcmus-density-auggeo-20260919-v1`.
Output: `/slurmshared/Ngoc/runs/hcmus-density-cv5-v1-738-fold0`.
W&B group: `vindr-densityCV5-v1-auggeo-seed42-full50`.
W&B run: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/rm5cgljr
Epoch 1 completed without data/augmentation error: natural FIT counts
[5,156,1245,207], finite losses, four AMP-skipped updates, Macro-F1
0.566119475, accuracy 0.863861386 and QWK 0.682897591. Class F1 was
[0,0.674699,0.915361,0.674419]; this is an initial observation, not the gate.
Do not expand unless fixed fold 0 reaches four-class Macro-F1 0.75; interpret
the tiny class-A support separately and require the complete 50-epoch audit.

## D1 stronger dropout screening launched (2026-09-19)

Controlled B0 comparison motivated by the large early-peak/epoch-50 gap in B0
and O1: increase fusion/head dropout from 0.1 to 0.3. Architecture dimensions,
pretrained backbone, stretch resize, original brightness-only augmentation,
natural sampling, loss, LR 5e-5, weight decay, fold 0 and seed 42 are unchanged.

Config `configs/vindr_density_dropout30.yaml`, arm `dropout30`. Local and remote
parity checks confirmed only dropout plus experiment metadata/zero validation
workers differ from B0. Submitted screening job **739_0** only, full 50 epochs.
Startup confirmed on slurm-b20a-master-0 with NVIDIA RTX 5090; Vesta excluded.
Deployment: `/slurmshared/Ngoc/code/hcmus-density-dropout30-20260919-v1`.
Output: `/slurmshared/Ngoc/runs/hcmus-density-cv5-v1-739-fold0`.
W&B: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/6t9qscfl
Epoch 1 completed with finite losses, natural FIT counts [5,156,1245,207],
four AMP-skipped updates, Macro-F1 0.501695889, accuracy 0.826732673 and QWK
0.585823081. Class F1 [0,0.447761,0.892356,0.666667]; initial observation only.
Do not expand unless fixed fold-0 four-class Macro-F1 reaches 0.75 and the
per-class/confusion evidence is not merely a rare-A fluctuation.

## L2 reduced ordinal coefficient screening launched (2026-09-19)

At O1 fold 0's selected epoch, the weighted ordinal term contributed about
0.470 of roughly 0.515 total loss (~91%); at epoch 50 it was nearly the entire
loss, although the primary multiclass head supplies inference. Controlled B0
comparison L2 reduces only the auxiliary ordinal coefficient from 0.5 to 0.1.
The ordinal task remains active; architecture, all other loss terms, stretch
resize, brightness augmentation, natural sampling, LR 5e-5, model, fixed fold
0 and seed 42 are unchanged.

Config `configs/vindr_density_ordinal10.yaml`, arm `ordinal10`. Local and remote
parity checks plus assignment hash validation passed. Submitted **740_0** only,
full 50 epochs. Startup confirmed on slurm-b40a-worker-3, NVIDIA RTX 5090,
with Vesta excluded. Deployment:
`/slurmshared/Ngoc/code/hcmus-density-ordinal10-20260919-v1`.
Output: `/slurmshared/Ngoc/runs/hcmus-density-cv5-v1-740-fold0`.
W&B: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/7aoquqms
Epoch 1 completed with finite losses and natural FIT counts. Raw components
were focal 0.1510, ordinal 1.1869, binary 0.3735, neighbor 0.5744; after their
coefficients their contributions were approximately 0.151/0.119/0.112/0.115,
confirming that no auxiliary component dominated the initial objective. Four
normal AMP-skipped updates were recorded. DEV Macro-F1 0.503515392, accuracy
0.811881188, QWK 0.589430894, class F1 [0,0.473684,0.88,0.660377]. Initial
observation only; no gate decision.
Do not expand unless the complete fold-0 run reaches the 0.75 gate with sound
per-class evidence.

### L2 numeric gate crossed; CV5 confirmation submitted (2026-09-19)

Fold 0 epoch 22 reached Macro-F1 **0.7754193814**, accuracy 0.8193069307,
QWK 0.6212759400, per-class F1 [1,0.650602,0.882448,0.568627], with no severe
errors. Checkpoint/history/prediction/probability/frozen-membership verification
passed. B/C/D mean 0.700559 is +1.24 pp versus B0 fold 0, so the gain remains
mostly driven by its single A case and is not yet robust evidence.

Submitted confirmation **746_1–4**, same immutable L2 deployment/config, fresh
seed 42 and full 50 epochs; 740_0 continues without duplication. At startup,
746_1 was RUNNING on slurm-b20a-master-0 and 746_2 on slurm-b40a-worker-3;
746_3–4 were legitimately PENDING for resources. The launcher excludes Vesta
and requires RTX 5090. Do not restart pending tasks; verify allocation/startup
when resources become available.
Fold 1 W&B `6jy6a7lh` and fold 2 `4vgdqbob`; both confirmed RTX 5090 and
completed a finite first epoch with Macro-F1 0.518061172 / 0.486240988 and no
severe errors. Pending task 746_3 explicitly records
`ExcNodeList=slurm-b40a-worker-2` (Vesta).

L2 fold 0 subsequently completed all 50 epochs: job **740_0 COMPLETED exit 0**
after 1h13m33s on slurm-b40a-worker-3 (RTX 5090), with Vesta explicitly
excluded. The selected checkpoint remains epoch 22: Macro-F1
**0.7754193814**, accuracy 0.8193069307, QWK 0.6212759400, class F1
[1,0.650602,0.882448,0.568627], no severe errors. Epoch-50 Macro-F1 was
0.5364750459. The final audit verified exact epochs 1--50, checkpoint/history
agreement, all 404 fixed-fold DEV IDs and labels, finite normalized
probabilities, argmax predictions, and independently recomputed confusion and
metrics. W&B `7aoquqms` reports `finished`, 50 completed epochs and the same
best epoch/score. Confirmation folds 1--4 remain in progress; the one-fold
gate result is not a CV5 conclusion and is still strongly affected by the
single fold-0 class-A case.

L2 fold 1 subsequently completed: task **746_1 COMPLETED exit 0** after
58m41s on slurm-b20a-master-0 (RTX 5090), with Vesta excluded. Its selected
epoch 3 reached Macro-F1 **0.5608266562**, accuracy 0.8337468983, QWK
0.6745338171 and class F1 [0,0.714286,0.890365,0.638655], no severe errors;
epoch-50 Macro-F1 was 0.4892918283. The final audit passed exact epochs 1--50,
checkpoint/history agreement, all 403 fixed DEV IDs/labels, finite normalized
argmax probabilities and independently recomputed metrics. W&B `6jy6a7lh`
reports `finished` with 50 completed epochs. The failure to recognize fold
1's A case demonstrates that fold 0's 0.7754 gate result does not transfer
stably; folds 2--4 remain in progress.

L2 folds 2 and 3 subsequently completed exit 0 after 1h18m29s and 58m27s,
respectively, on RTX 5090 with Vesta excluded. Fold 2 selected epoch 5:
Macro-F1 **0.6349742341**, accuracy 0.8436724566, QWK 0.6478298864, class F1
[0.4,0.705882,0.906542,0.527473]; epoch-50 F1 0.4880509162. Fold 3 selected
epoch 17: Macro-F1 **0.6060021436**, accuracy 0.8217821782, QWK 0.6455881278,
class F1 [0.333333,0.6,0.890675,0.6]; epoch-50 F1 0.5311648279. Both final
audits passed exact 50-epoch history, checkpoint, fixed DEV membership/labels,
probabilities, independently recomputed metrics and W&B states `finished`
(`4vgdqbob`, `ofu6s261`). Fold 4 remains in progress; the current evidence
already confirms the fold-0 L2 peak is not stable across folds.

## R1 warm-up screening completed (2026-09-19)

Job 737_0 COMPLETED exit 0 after 57m02s, all 50 epochs. Artifact audit verified
the intended frozen state for epochs 1–5, unfreeze at epoch 6, checkpoint/history
maximum, exact 404-case DEV membership/labels, finite normalized argmax
probabilities, and recomputed metrics. Best epoch 23: Macro-F1
**0.6959794461**, accuracy 0.8217821782, QWK 0.6201484304, class F1
[0.666667,0.629213,0.883871,0.604167]. Epoch 50 Macro-F1 0.5469394388.
It fails the 0.75 gate; do not launch additional folds or seeds for R1 alone.
W&B `iilc5qpu` independently reports `finished`, 50 completed epochs, no early
stop and the same best epoch/metric.

## D1 dropout-0.3 screening completed (2026-09-19)

Job 739_0 COMPLETED exit 0 after 58m15s. All 50 epochs and the selected
checkpoint/prediction/probability/frozen-membership audit passed. W&B
`6t9qscfl` reports `finished`, 50 completed epochs, no early stop and matching
best epoch/metric. Best epoch 32: Macro-F1 **0.7291174276**, accuracy
0.8514851485, QWK 0.6935679612, class F1
[0.666667,0.658537,0.904992,0.686275], no severe errors. Epoch 50 Macro-F1
0.6988806011. This is a balanced-looking improvement over B0 fold 0 but fails
the fixed 0.75 gate; do not launch additional folds or seeds for D1 alone.

D1 completion freed a GPU and L2 confirmation task **746_3** started on
slurm-b20a-master-0 with RTX 5090; W&B `ofu6s261`. Task 746_4 remains pending
for resources and must not be restarted.

## O1 lower-LR CV5 completed decision (2026-09-19)

All five folds completed 50 epochs with Slurm exit 0 and W&B `finished`; full
history/checkpoint/prediction/probability/frozen-membership and pooled-coverage
audit passed. Selected Macro-F1 mean **0.6351955762**, sample SD
**0.1022552801**, mean accuracy **0.8443198290**, mean QWK **0.6633020463**.
Epoch-50 mean Macro-F1 **0.5025014529** (SD 0.0178046055). Pooled descriptive
Macro-F1 **0.6634577419**, accuracy 0.8443232524, QWK 0.6629621154.

Best epochs/fold F1: [13,4,15,7,5] and
[0.7968110413,0.5680718555,0.6776928320,0.5644199577,0.5689821947].
Mean improvement over B0 is +3.39 pp, but dispersion nearly doubled and the
75% mean target failed. O1 B/C/D mean **0.7358163239** versus B0
**0.6937298330**, improving in all five folds; folds 1/3/4 still missed every
A case. No multi-seed confirmation for O1 alone. Full report:
[O1 results](vindr_lr1e5_cv5_results_20260919.md).

## A1 augmentation screening gate crossed (2026-09-19)

Fold 0 epoch 30 reached Macro-F1 **0.7718085026**, accuracy 0.8366336634,
QWK 0.6122164049, class F1 [1,0.631579,0.897516,0.558140], no severe errors.
Checkpoint/history/prediction/probability/frozen-membership checks passed.
The numeric gate is crossed, but B/C/D mean is only 0.695745 (just +0.76 pp
versus B0 fold 0), so most apparent improvement comes from the single A case.

Per the fixed gate, submitted confirmation **741_1–4**, fresh seed 42, same A1
snapshot/config and 50 epochs; fold 0 continues as 738_0 with no duplicate.
All four confirmed RUNNING on RTX 5090 (three on slurm-b40a-worker-1, one on
slurm-b40a-worker-3), Vesta excluded. Outputs use job 741 for folds 1–4.
W&B IDs by fold 1–4: `obhrh9bo`, `ffuqaxqv`, `snvrmwj8`, `fnfddqkp`.
Each produced three finite epochs with no traceback at the first follow-up;
best early Macro-F1 was 0.5082/0.4960/0.5411/0.5251. These are startup
observations only.
This is a robustness test, not evidence that the target has been achieved.

A1 fold 0 later completed: job 738_0 COMPLETED exit 0 after 1h09m52s; W&B
`rm5cgljr` reports `finished`, 50 epochs and no early stop. Full artifact audit
passed. Final selected epoch 38 reached Macro-F1 **0.8048682606**, accuracy
0.8490099010, QWK 0.6689414293, class F1
[1,0.675676,0.903021,0.640777], no severe errors; B/C/D mean 0.739824.
Epoch-50 Macro-F1 remained 0.7810521445. This is the strongest completed
fold-0 A1 evidence, but CV5 confirmation remains required.

A1 fold-0 completion freed a GPU; L2 task **746_4** started on
slurm-b40a-worker-3 with RTX 5090, W&B `53akuiz4`. All L2 folds are now
running; no L2 task remains pending.

Provisional A1 A-probability diagnostic (selected checkpoints can still change):
folds 0/2/4 correctly classify their A case; fold 3 classifies one of two A
cases; fold 1 misses its A with p(A)=0.161 and rank 10 among non-A p(A).
Fold 2 has one false A, fold 3 two, fold 4 two; fold 4 includes a non-A case
with p(A)=0.975 above the true A p(A)=0.869. Thus geometry augmentation does
produce A signal beyond fold 0, unlike O1, but it is not precise or consistent
enough to support threshold calibration. Re-run only after final checkpoints.

A1 fold 4 later improved at epoch 38 to Macro-F1
**0.7500093793**, accuracy 0.7990074442, QWK 0.5807851850 and class F1
[1,0.620690,0.869144,0.510204], no severe errors. The fold's B/C/D mean is
only 0.666679, so crossing 0.75 is again substantially driven by its single A
case. Task **741_4 COMPLETED exit 0** after 1h18m40s on RTX 5090 worker-3,
with Vesta excluded. Final audit passed exact epochs 1--50,
checkpoint/history agreement, all 403 fixed DEV IDs/labels, finite normalized
argmax probabilities, independently recomputed metrics and W&B `fnfddqkp`
state `finished`; epoch-50 Macro-F1 was 0.5107118009. With current selected
checkpoints the provisional A1 five-fold mean is about 0.680; folds 1--3 must
still complete before the final aggregate audit.

### A1 CV5 completed — target not met (2026-09-19)

Tasks 741_1--3 subsequently completed exit 0; all five A1 folds are now
terminal with exactly 50 epochs. Full checkpoint/prediction/membership/W&B
audit passed for every fold and for the non-overlapping union of 2,017 cases.
Selected fold Macro-F1 values are
[0.8048682606, 0.5603610966, 0.6498278912, 0.6348107448, 0.7500093793],
giving mean **0.6799754745** and sample SD **0.0971587423**. Mean accuracy is
0.8284352505 and mean QWK 0.6327079214. Mean per-class F1 A/B/C/D is
[0.613333,0.640675,0.891021,0.574873]; B/C/D mean is 0.702190. Epoch-50 mean
Macro-F1 is 0.5716605657. The pooled descriptive Macro-F1 is 0.6819124635 on
support [6,196,1556,259]. A1 improves over B0 but fails the 0.75 target and
has much higher fold dispersion; it must not proceed to multi-seed testing.
Detailed report: `reports/vindr_auggeo_cv5_results_20260919.md`.

## O2 low LR plus mild sampling screening launched (2026-09-19)

O1 improved B/C/D in every fold but missed A in three folds. S1 sampling power
0.5 overexposed the five fold-0 FIT A cases (~56 expected draws/epoch) and
failed its gate. O2 therefore retains completed O1 unchanged and adds only
sampling power 0.25: expected FIT draws/epoch approximately
[17.31,228.46,1084.78,282.45] for A/B/C/D versus natural
[5,156,1245,207]. This is mild exposure (~3.5x A), not full balancing.

Config `configs/vindr_density_lr1e5_sampling025.yaml`, arm
`lr1e5_sampling025`. Config parity against O1 and the frozen assignment hash
were verified. Submitted screening **745_0** only, full 50 epochs. Startup
confirmed on slurm-b40a-worker-1 with NVIDIA RTX 5090; Vesta excluded.
Deployment:
`/slurmshared/Ngoc/code/hcmus-density-lr1e5-sampling025-20260919-v1`.
Output: `/slurmshared/Ngoc/runs/hcmus-density-cv5-v1-745-fold0`.
W&B: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/imixg793
Epoch 1 completed with realized A/B/C/D draws [12,246,1077,278] (total 1,613),
consistent with stochastic mild sampling and far below S1's A exposure. Finite
losses, four AMP-skipped updates, Macro-F1 0.531409905, accuracy 0.844059406,
QWK 0.635274562, class F1 [0,0.694737,0.903125,0.527778]. Initial observation
only; class A is not yet recognized.
Do not expand unless fold 0 crosses 0.75 with B/C/D retained and confusion
evidence not explained only by its single A case.

### O2 numeric gate crossed; CV5 confirmation queued (2026-09-19)

Fold 0 epoch 4 reached Macro-F1 **0.7929794609**, accuracy 0.8193069307,
QWK 0.6567185027, class F1 [1,0.673913,0.878536,0.619469], no severe errors.
B/C/D mean 0.723973 is +3.58 pp versus B0 fold 0 and close to O1 fold 0,
so common-class behavior is retained even though the single A case still
materially raises Macro-F1. Checkpoint/history/prediction/probability/frozen
membership and all realized sampler-count sums were verified.

Submitted confirmation **749_1–4**, same immutable O2 deployment/config, fresh
seed 42 and full 50 epochs; 745_0 continues without duplication. All four were
initially PENDING for priority behind older work; this is normal and they must
not be restarted. `ExcNodeList=slurm-b40a-worker-2` confirms Vesta exclusion;
the launcher will also reject any non-RTX-5090 allocation.

O2 fold 0 subsequently improved at epoch 6 to Macro-F1 **0.8196671789**,
accuracy 0.8539603960, QWK 0.6967430025, class F1
[1,0.707317,0.904685,0.666667], no severe errors. B/C/D mean **0.759556** is
also strong (+7.14 pp versus B0 fold 0), so this peak is not explained only by
the single A case. Realized sampling counts [15,239,1079,280] remained mild.
This strengthens the rationale for the already queued CV5 confirmation but is
still selected DEV evidence from one fold.

O2 fold 0 subsequently completed all 50 epochs: job **745_0 COMPLETED exit
0** after 1h21m21s on RTX 5090 worker-1, with Vesta excluded. Its selected
epoch remains 6 with the metrics above; epoch-50 Macro-F1 was 0.5062474503.
Final audit passed exact epochs 1--50, checkpoint/history agreement, all 404
fixed DEV IDs/labels, finite normalized argmax probabilities, independently
recomputed metrics and W&B `imixg793` state `finished`. Mean realized
sampling counts across 50 epochs were [18.08,227.24,1082.96,284.72], matching
the intended mild sampler. Full CV5 confirmation remains required.

After L2 fold 0 completed, O2 confirmation task **749_1** started normally on
slurm-b40a-worker-3 with NVIDIA RTX 5090; Vesta remains excluded. Startup
output confirms fold 1, seed 42, the frozen assignment SHA, LR 1e-5 and
sampling power 0.25. W&B run:
https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/juamjlss
Tasks 749_2--4 remain legitimately pending for resources and must not be
restarted.

O2 fold 1 completed a finite first epoch with realized sampled counts
[13,224,1108,269] (total 1,614), four expected initial AMP-skipped updates,
Macro-F1 0.5574411353, accuracy 0.8362282878, QWK 0.6691791045, class F1
[0,0.712644,0.893268,0.623853] and no severe errors. This is only a startup
observation; the A case is not yet recognized and no gate conclusion is drawn.

After L2 fold 1 finished, O2 task **749_2** started on slurm-b20a-master-0
with NVIDIA RTX 5090 and Vesta excluded; tasks 749_3--4 remain pending. Startup
confirmed the frozen fold-2 manifest/assignment SHA, seed 42, LR 1e-5 and
sampling power 0.25. W&B run:
https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/y81irdos
Its first epoch completed with finite losses, realized sampled counts
[11,253,1056,294] (total 1,614), five initial AMP-skipped updates, Macro-F1
0.5311797619, accuracy 0.8263027295, QWK 0.6196780543, class F1
[0,0.714286,0.889600,0.520833] and no severe errors. This is a startup
observation only; fold 2's A case is not yet recognized.

After A1 fold 4 completed, O2 task **749_3** started normally on
slurm-b40a-worker-3 with NVIDIA RTX 5090 and Vesta excluded; only task 749_4
remains pending. Startup confirms fold 3, seed 42, the frozen assignment SHA,
LR 1e-5 and sampling power 0.25. W&B run:
https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/cj100tf3

O2 task **749_4** subsequently started on slurm-b40a-worker-1 with NVIDIA RTX
5090 and Vesta excluded; all four confirmation folds are now running. W&B run:
https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/o4umnn2b
Its first epoch completed with finite losses, realized sampled counts
[17,223,1070,304] (total 1,614), Macro-F1 0.5325621385, accuracy 0.8411910670,
QWK 0.6179302581, class F1 [0,0.647887,0.901716,0.580645] and no severe
errors. This is a startup observation only.

## O3 low LR plus dropout-0.3 candidate prepared (2026-09-19)

O1 improved common-class behavior across all five folds, while D1's stronger
dropout produced a balanced-looking fold-0 result but missed the 0.75 gate.
O3 therefore uses O1 as its control and changes only model dropout from 0.1 to
0.3. Config: `configs/vindr_density_lr1e5_dropout30.yaml`, arm
`lr1e5_dropout30`. The immutable candidate deployment was cloned directly from
the completed O1 snapshot at
`/slurmshared/Ngoc/code/hcmus-density-lr1e5-dropout30-20260919-v1`; only the
new config was added. Local and remote config parity checks passed, including
the fixed assignment SHA, fold 0, seed 42 and full 50-epoch contract. The O1
snapshot's cluster suite passed 14/14 tests. O3 was initially held so queued
O2 confirmation folds retained GPU priority. After every O2 confirmation fold
was running, screening job **754_0** was submitted for fixed fold 0 only. It
started on slurm-b40a-worker-1 with NVIDIA RTX 5090;
`ExcNodeList=slurm-b40a-worker-2` confirms Vesta exclusion. Startup confirmed
the fixed assignment SHA/seed, LR 1e-5, dropout 0.3 and otherwise O1
configuration. W&B run:
https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/nwbn6oja
No folds 1--4 unless its completed fold-0 Macro-F1 reaches 0.75.

## Interim diagnostics while O2/O3 continue (2026-09-19)

Read-only comparison of the selected O2 predictions against completed O1
shows why the successful fold-0 screen is insufficient. At O2 epochs
[50,28,23,10,8], the selected fold-3 checkpoint recognizes one of its two A
cases but also predicts seven B cases as A; O1's selected fold-3 checkpoint
missed both A cases with no false A predictions. O2 selected B/C/D mean in
that fold is 0.687801 versus O1's 0.752560. Fold 2 currently misses its A case
despite better B/C/D mean (0.729237 versus 0.681368). Folds 1 and 4 still miss
their A cases. Prediction confusion matrices were checked against each
history's selected epoch before comparing. These are interim, differently
selected checkpoints; they do not establish a causal effect or final outcome.
Recompute after all O2 folds complete. Do not tune A thresholds on these DEV
cases or expand sampling strength based solely on their scores.

The A1 gain decomposition is now documented in its CV5 report: 91.94% of
the Macro-F1 improvement comes from A, and B/C/D declines in three folds.
Also see `reports/ordinal_loss_diagnostic_20260919.md`: the positive loss
floor implied by the saved ordinal threshold gaps means a large auxiliary
loss value alone is insufficient evidence of large or conflicting gradients.

## Reproducible CV5 artifact audit (2026-09-19)

Added read-only `scripts/audit_density_cv5.py` to standardize final result
verification. It checks exact 50-epoch histories, common learning config,
architecture/protocol provenance, assignment digest, FIT/DEV manifest content,
selected checkpoint agreement, unique prediction membership, finite normalized
probabilities and argmax, recomputed metrics, and full non-overlapping CV
coverage. Optional W&B checks require finished runs and matching best scores.
Slurm exit status and GPU allocation remain separate checks; this utility
does not claim to audit patient identities beyond the registered split.

Validated on completed A1: all five folds passed with the same reported
metrics; saved the output as `reports/vindr_auggeo_cv5_results_20260919.json`.
Validated the incomplete-run guard against live O2: it correctly stopped at
fold 1 with `incomplete epochs`. No training process or artifact was changed.

## L2 CV5 completed — target not met (2026-09-19)

Final task 746_4 completed exit 0 after 1h13m57s on RTX 5090 worker-3,
Vesta excluded. All five folds now pass the reproducible artifact audit,
including finished W&B runs and exact registered 2,017-case coverage.
Selected fold Macro-F1 values are [0.7754193814,0.5608266562,0.6349742341,
0.6060021436,0.6756181606]. Mean **0.6505681152**, sample SD **0.0813912892**;
mean accuracy 0.8254882932, QWK 0.6385604514. Mean class F1 is
[0.48,0.649944,0.889490,0.582839], B/C/D mean 0.707424. Epoch-50 mean F1 is
0.5074892544. L2 fails the 0.75 target; no multi-seed expansion for L2 alone.
Detailed report and raw audit output:
`reports/vindr_ordinal10_cv5_results_20260919.md` and companion `.json`.

## A2 preregistered screen: A1 augmentation with lower LR (2026-09-19)

Control is completed A1. Change only initial LR 5e-5 to 1e-5, retaining
shared geometry augmentation, natural sampling and all other A1 settings.
A1 has the strongest completed CV5 Macro-F1 but modest common-class gains;
O1's lower LR improved B/C/D across folds. Whether the combination helps is
an untested hypothesis. No ensemble, altered split or A-threshold tuning.

Config `configs/vindr_density_auggeo_lr1e5.yaml`, arm `auggeo_lr1e5`.
Snapshot `/slurmshared/Ngoc/code/hcmus-density-auggeo-lr1e5-20260919-v1` is
cloned from A1. Byte comparison confirms source/launcher unchanged; config
parity confirms only LR and arm metadata differ. Fold-0 configure validates
the fixed manifests and assignment SHA. The launcher excludes Vesta and
asserts RTX 5090. Screen fixed fold 0 only, seed 42, all 50 epochs. Expand
only after the completed screen reaches Macro-F1 >= 0.75; assess per-class
behavior and complete CV5 before any success claim or multi-seed validation.

Submitted task **755_0**, running on slurm-b20a-master-0 with verified NVIDIA
RTX 5090 and Vesta exclusion. W&B:
https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/o7pos4pv
Output: `/slurmshared/Ngoc/runs/hcmus-density-cv5-v1-755-fold0`.
First epoch had finite loss, natural class counts [5,156,1245,207], four
initial AMP-skipped updates and Macro-F1 0.2719324177 (accuracy 0.7821782178,
QWK 0.1380915438). Predictions initially concentrate on C; this is a startup
observation, not evidence of convergence or a gate result. O2/O3 continue.

## Verified CV5 summaries published to W&B (2026-09-19)

Published audited A1 and L2 aggregate reports using
`scripts/publish_cv5_summary.py`. These are summary runs (no new training),
with per-fold result tables, mean/sample-SD metrics, per-class means/support,
source-run links and audit JSON artifacts. No per-case records were uploaded.
Independent API verification confirmed both runs finished, exact aggregate
scores, 2,017 cases and flags `independent_test=False`,
`multi_seed_verified=False`. Existing training runs remain unchanged.

- A1 summary: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/f104a6w4
- L2 summary: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/lrodsj27

## O2 confirmation folds 1--2 completed (2026-09-19)

Tasks 749_1 and 749_2 completed exit 0 after 1h11m39s and 57m01s,
respectively, on RTX 5090 worker-3/master with Vesta excluded. Both have exact
epochs 1--50 and pass final checkpoint/history, fixed assignment/DEV label and
membership, normalized finite probability/argmax, recomputed metrics, and
W&B finished-state checks. All sampler draws sum to 1,614 per epoch.

- Fold 1: best epoch 1, Macro-F1 0.5574411353, accuracy 0.8362282878,
  QWK 0.6691791045, class F1 [0,0.712644,0.893268,0.623853];
  epoch-50 Macro-F1 0.4659304511. W&B `juamjlss` finished.
- Fold 2: best epoch 4, Macro-F1 0.5469278435, accuracy 0.8535980149,
  QWK 0.6462440302, class F1 [0,0.714286,0.911628,0.561798];
  epoch-50 Macro-F1 0.4877973659. W&B `y81irdos` finished.

Both selected checkpoints miss the true A case; fold 2 also predicts one B
case as A. The high fold-0 result does not replicate here. Confirmation folds
3--4 remain running, so no final O2 CV5 aggregate is claimed yet.

A2 interim numeric gate: fold 0 reached Macro-F1 **0.7927400468** at epoch
10, accuracy 0.8267326733, QWK 0.6580245719, class F1
[1,0.653061,0.885246,0.632653], no severe errors. B/C/D mean is 0.723653;
the single A case still has a large influence. The run was at epoch 12 when
observed and continues to 50. Per A2 preregistration, wait for the completed
screen and final artifact audit before launching confirmation folds.

Fold-0 history diagnostic at A2 epoch 15: only epoch 10 has Macro-F1 >=
0.75; its last five epochs average 0.513735 with A F1 zero in each. For
comparison, completed A1 had 19/50 epochs >=0.75 and a last-five mean of
0.782083, yet failed full CV5. Completed O1 had 2/50 epochs >=0.75 and O2
5/50; their fold-0 last-five means were 0.526395 and 0.523347, respectively.
These are within-run descriptive diagnostics, not new checkpoint-selection
rules or independent validation. A2 is still in progress, so its peak
stability cannot yet be assessed over the complete training schedule.

## O2 confirmation fold 3 completed (2026-09-19)

Task 749_3 completed exit 0 after 1h03m59s on worker-3; the log confirms
RTX 5090 and Slurm excludes worker-2/Vesta. Exact epochs 1--50,
checkpoint/history selection, fold/arm/assignment hash, DEV membership and
labels, finite normalized probabilities and argmax, recomputed Macro-F1,
accuracy, QWK and confusion matrix all passed read-only checks. W&B
`cj100tf3` is finished with 50 epochs and matching best Macro-F1.

Selected epoch 3: Macro-F1 0.5658505097, accuracy 0.7995049505,
QWK 0.6646443943; class F1 [0.2,0.543478,0.877722,0.642202].
One of two A cases is recognized, but seven B cases are falsely called A.
Epoch-50 Macro-F1 is 0.4993561155. Fold 4 remains live, so the final
O2 CV5 audit and aggregate publication are still pending. O3 and A2
screening runs also remain live; no additional folds were submitted.

## O2 full CV5 closed and published (2026-09-19)

Final task 749_4 completed exit 0 on worker-1, 1h04m53s, verified RTX 5090
and Vesta excluded. Full `audit_density_cv5.py` passed all five runs,
including exact 50 epochs, consistent configs, assignment/manifest checks,
checkpoint selection, recomputed predictions and finished W&B states.
Report: `vindr_lr1e5_sampling025_cv5_results_20260919.{md,json}`.

Macro-F1 mean **0.6058691026**, sample SD **0.1199382836**; accuracy
0.8284598187, QWK 0.6649660571; class means
[0.24,0.672919,0.889779,0.620779]. Epoch-50 mean 0.4856450521.
O2 loses 0.0293264736 versus its O1 control and fails the 0.75 target.
No multi-seed expansion. Six A cases remain insufficient for robustness
claims; pooled predictions recognize only two and misclassify eight B as A.

Published summary and independently verified finished cloud state, exact
mean, 2,017 cases, fold table and audit artifact; independent-test,
target-met and multi-seed flags are all false:
https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/x7sraegv

At this check O3 task 754_0 remained running at 49/50 epochs; A2 task
755_0 remained running at 34/50. A2 confirmation still requires completed
50-epoch screen audit; no confirmation jobs submitted yet.

## O3 completed screen: reject expansion (2026-09-19)

Task 754_0 completed all 50 epochs, exit 0, runtime 1h03m55s on worker-1.
Verified RTX 5090 log and Vesta exclusion. Read-only checks passed exact
history epochs, checkpoint selection/metrics, fold/arm/assignment hash,
DEV IDs/labels, finite normalized probabilities and argmax, recomputed
Macro-F1/accuracy/QWK/confusion matrix, and finished W&B `nwbn6oja` with
50 epochs and matching best score.

Best epoch 21: Macro-F1 **0.5534079029**, accuracy 0.8564356436,
QWK 0.6598141696, class F1 [0,0.707317,0.911076,0.595238].
Epoch-50 Macro-F1 0.5291645552. No A recognized at the selected checkpoint.
The screen fails 0.75: do not launch O3 folds 1--4 or multi-seed runs.
The earlier compacted context's provisional class metrics for O3 were not
authoritative; the values above are from the completed checkpoint and CSV.

https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/nwbn6oja

A2 task 755_0 remains running on master; last observed at 34/50 epochs,
best fold-0 Macro-F1 0.7927400468. Wait for completion and audit before
expanding A2; this is not evidence of meeting the CV5 objective.

## A3 preregistration: class-weight smoothing on A1 (2026-09-19)

Test `configs/vindr_density_auggeo_beta99.yaml`, arm `auggeo_beta99`.
Only loss beta changes 0.999 -> 0.99 relative to A1; same geometry,
LR 5e-5, natural sampling, loss coefficients, architecture, split and seed.
Motivation: A1 remains the best completed CV5 arm, but its gain is largely
driven by six A cases and B/C/D gains are weak. Test less extreme relative
rare-class weighting without changing data frequency or inference.

For fold-0 FIT counts [5,156,1245,207], focal weights change from
[3.744573,0.129304,0.026235,0.099888] to
[3.427788,0.212248,0.167996,0.191968]. FIT-expected weight changes
0.057181 -> 0.185457. Beta also changes binary class weights. Thus this
is a class-weight-group intervention, not a scale-invariant ratio-only
experiment. Risks include reduced A recall and changed auxiliary balance;
no causal claim is made from scalar loss magnitudes.

Screen fixed fold 0, training seed 42, exactly 50 epochs on RTX 5090,
exclude Vesta. Only after completion, artifact audit and best DEV Macro-F1
>=0.75 may folds 1--4 be launched. Preserve per-class reporting and use
completed CV5 before any multi-seed expansion. A2 continues unchanged.

A3 deployed as `/slurmshared/Ngoc/code/hcmus-density-auggeo-beta99-20260919-v1`,
cloned from A1. Verified source/launcher byte parity, config-only beta and
arm changes, fold-0 manifest/hash validation and GPU/Vesta guards using the
same `.deps` import path as the launcher. Initial validation without that
path failed to import cv2; no training was launched until validation passed.
Task **756_0** is running on master, log confirms NVIDIA GeForce RTX 5090,
Slurm explicitly excludes worker-2. W&B initialized:
https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/gvcsv9lm
No completed A3 epoch yet at the startup check. A2 task 755_0 was live at
38/50 epochs; it remains unchanged and awaits the completed screen audit.

## A2 completed screen and confirmation launch (2026-09-19)

Task 755_0 completed 50 epochs, exit 0, runtime 1h03m04s on master RTX
5090; Slurm excludes Vesta. Checkpoint/history selection, fold/arm/hash,
DEV prediction IDs/labels, finite normalized probabilities/argmax,
recomputed Macro-F1/accuracy/QWK/confusion matrix and finished W&B state
all passed. W&B `o7pos4pv` reports 50 epochs and matching best score.

Selected epoch 10: Macro-F1 **0.7927400468**, accuracy 0.8267326733,
QWK 0.6580245719, class F1 [1,0.653061,0.885246,0.632653].
Epoch 50 Macro-F1 0.5001490300; last-five mean 0.5006641746.
Only 2/50 epochs reach 0.75. A single A case determines a large share of
the selected score: this passes the preregistered numeric screening gate,
not the CV5 or stability objective.

Validated configs for all five folds against the completed checkpoint,
including fixed manifests/assignment hash and RTX5090/Vesta launcher
guards. Submit only folds 1--4 from the same immutable A2 snapshot/config;
retain completed fold 0, train fresh ImageNet initialization per fold,
seed 42 and 50 epochs. A3 remains running unchanged.

Confirmation submitted as array **757_1--757_4**. All four tasks have
explicit worker-2/Vesta exclusion verified in Slurm. Outputs follow
`/slurmshared/Ngoc/runs/hcmus-density-cv5-v1-757-fold{1,2,3,4}`.
Check individual GPU startup logs/W&B run IDs when scheduled; no duplicate
fold-0 training is needed.

Startup verified for all A2 confirmation tasks: each log reports NVIDIA
GeForce RTX 5090. Fold 1 runs on master; folds 2--4 on worker-1, not Vesta.
W&B IDs in fold order 1--4: `5hh89fjy`, `dswzbxag`, `2jzzgke6`, `fwngpu65`.
Fold 1 completed its first epoch with finite loss 1.0243195758; the other
folds initialized W&B and remain running at this check.

A3 provisional gate at epoch 14: Macro-F1 0.7752373149, accuracy
0.7920792079, QWK 0.6347826087; F1 A/B/C/D
[1,0.634615,0.856164,0.610169]. Only one DEV A case supports A F1=1.
At the check A3 had reached epoch 15, not 50; do not expand before the
preregistered completed-screen audit. This is not a CV5 success claim.

## A3 screen completed; expand to confirmation (2026-09-19)

Task 756_0 completed exactly 50 epochs, exit 0, runtime 1h10m10s on master
RTX 5090 with Vesta excluded. Read-only checks passed selected checkpoint
versus history, fold/arm/assignment hash, DEV IDs/labels, finite normalized
probabilities and argmax, recomputed Macro-F1/accuracy/QWK/confusion matrix,
and finished W&B `gvcsv9lm` with 50 epochs and matching best score.

Best epoch 14: Macro-F1 **0.7752373149**, accuracy 0.7920792079,
QWK 0.6347826087; class F1 [1,0.634615,0.856164,0.610169].
Only 1/50 epochs exceeds 0.75; epoch-50 Macro-F1 0.6412269026,
last-five mean 0.6402348659. Epoch 50 recognizes the single A but has three
false A predictions (two B, one C). Selected DEV success is not stable
CV5 or independent-test evidence.

Numeric completed-screen gate passed. Validated all five manifests/configs
against the completed checkpoint and verified RTX5090/Vesta launcher guards.
Proceed with fresh ImageNet folds 1--4 only, seed 42, 50 epochs, same A3
snapshot/config. Retain completed fold 0; A2 confirmation continues unchanged.

A3 confirmation submitted as **761_1--761_4**; per-task Slurm Vesta
exclusion verified. Outputs:
`/slurmshared/Ngoc/runs/hcmus-density-cv5-v1-761-fold{1,2,3,4}`.
Verify allocated GPU and W&B IDs at startup; do not resubmit pending tasks.

A3 confirmation startup verified: all four logs explicitly report NVIDIA
GeForce RTX 5090. Fold 1 runs on master, fold 2 on worker-1, folds 3--4 on
worker-3; no Vesta. W&B IDs for folds 1--4 respectively:
`sfdz24yr`, `m8s2uyk6`, `mo99kw4x`, `jud6l8uz`.
All four tasks are running; first epochs pending at this startup check.
A2 confirmation tasks 757_1--4 also remain running (34--37 epochs).

## A2 confirmation fold 1 completed (2026-09-19)

Task 757_1 completed exactly 50 epochs, exit 0, runtime 1h10m02s on master.
GPU log confirms RTX 5090; Slurm excludes worker-2/Vesta. Checks passed
checkpoint/history selection, fold/arm/assignment hash, unique DEV IDs and
labels, finite normalized probabilities/argmax, recomputed Macro-F1,
accuracy, QWK and confusion matrix. W&B `5hh89fjy` is finished with 50
epochs and matching best Macro-F1.

Best epoch 4: Macro-F1 **0.5501173584**, accuracy 0.8387096774,
QWK 0.6611824661, class F1 [0,0.666667,0.896440,0.637363].
The selected checkpoint misses the only A case (predicts B).
Epoch-50 Macro-F1 0.5102514333. Fold-0 success has not replicated on this
fold. Folds 2--4 remain running, so no final A2 CV5 aggregate is claimed.

## A2 completed CV5 audit (2026-09-19)

All five runs completed 50 epochs; full prediction/checkpoint/split/W&B audit PASS.
Tasks 757_2--4 independently rechecked COMPLETED, exit 0, worker-1, Vesta excluded.
Mean Macro-F1 **0.6612749364**, sample SD 0.0939601958; accuracy 0.8319239368,
QWK 0.6426477659. Class F1 means [0.513333,0.645082,0.893987,0.592698].
B/C/D mean 0.7105888042; epoch-50 mean 0.5185089841.
A2 is below A1 by 1.87 percentage points and does not meet the 0.75 target.
No multi-seed expansion. See vindr_auggeo_lr1e5_cv5_results_20260919.json/.md.
A3 tasks 761_1--4 rechecked RUNNING on master/worker-1/worker-3; no resubmission.

A2 W&B summary `vui0tplb` published and independently verified finished,
with matching mean, 2017 cases, fold table and cv5-audit artifact; independent
test and multi-seed flags remain false. A3 confirmation has reached epochs
24/19/23/23 on folds 1/2/3/4 respectively, all still running.

## A4 preregistration: ordinal coefficient on augmentation (2026-09-19)

Arm `auggeo_ordinal10`; reference A1. Change only loss.ordinal 0.5 to 0.1.
L2's B/C/D mean 0.707424 versus B0 0.693730 supports testing whether the
auxiliary-loss adjustment adds benefit to A1, not an assumption of additivity.
Large ordinal loss values alone do not establish gradient domination.
Keep A1 augmentation, LR 5e-5, beta .999, natural sampling, dropout .1,
DenseNet121/hierarchical fusion and flat-only single-checkpoint inference.
Same frozen grouped split, seed 42, fresh ImageNet, 50 epochs, RTX5090 only,
worker-2/Vesta excluded. Screen fixed fold 0 only. Complete and audit all
50 epochs; expand folds 1--4 only if best DEV Macro-F1 >= .75. Full CV5 and
multi-seed stability remain required; no independent-test claim.
A3 confirmation continues unchanged. No ensemble or altered selection rule.

A4 snapshot `/slurmshared/Ngoc/code/hcmus-density-auggeo-ordinal10-20260919-v1`
validated: Python/launcher source byte parity with A1, exact config diff,
all five frozen manifests and assignment hash, RTX5090 assertion and Vesta
exclusion. Submitted fixed fold-0 screen as **765_0**. Output directory
`/slurmshared/Ngoc/runs/hcmus-density-cv5-v1-765-fold0`.

765_0 startup verified RUNNING on master, explicit worker-2 exclusion;
GPU startup reports RTX 5090. W&B run `3bjbsz4j` initialized online.

## Paired-fold follow-up diagnostic (2026-09-19)

Recomputed from completed audited JSON reports, selected DEV checkpoints:
A2 minus A1 mean class-F1 deltas A/B/C/D are
[-0.100000, +0.004407, +0.002966, +0.017825]. B/C/D improves in only
2/5 folds, with deltas [-0.016171,-0.013658,+0.071188,+0.002384,-0.001746].
The mean D gain is concentrated in fold 2 (+0.108140); D declines in 3/5
folds. Thus lowering LR does not show consistent B/C/D benefit despite a
positive mean, and A2 should not replace A1 based on that secondary metric.

L2 minus A1 B/C/D deltas are
[-0.039265,+0.000621,+0.069084,-0.016189,+0.011923]. This comparison changes
both augmentation and ordinal coefficient and is descriptive, not causal.
A4 is the registered one-factor test needed to isolate the ordinal change
on the A1 reference. No significance or independent-test claim is made.

## A3 completed CV5 audit (2026-09-19)

All five runs completed 50 epochs; tasks 761_1--4 independently verified
COMPLETED exit 0 on master/worker-1/worker-3 with worker-2 excluded.
Full checkpoint/history/manifest/prediction/W&B audit PASS, 2017 unique cases.
Mean Macro-F1 **0.6741231752**, sample SD 0.1129381921; accuracy 0.8319399061,
QWK 0.6419252803. Mean F1 A/B/C/D [0.583333,0.632516,0.894165,0.586478].
B/C/D mean 0.7043864558; epoch-50 mean 0.5529984318.
A3 is 0.585 percentage points below A1 and has larger fold dispersion.
Target not met; no multi-seed expansion for A3. These are selected DEV scores.
Reports: vindr_auggeo_beta99_cv5_results_20260919.json/.md.
W&B summary `2f1pwfl6` published and independently checked finished with
matching metrics, fold table, audit artifact and non-independent/non-multiseed flags.
A4 fold-0 screen 765_0 remains the current training experiment; no ensemble.

A4 provisional gate: at epoch 30, DEV Macro-F1 reached 0.7863606796.
Job 765_0 is verified RUNNING, not completed. Do not expand yet: finish
50 epochs and audit checkpoint/predictions/provenance/W&B first. A single
fold gate is not evidence of CV5 success or multi-seed stability.

## A4 completed screening audit; expand folds 1--4

765_0 now has exactly epochs 1--50 and W&B `3bjbsz4j` is finished.
Slurm has expired this job's record (Invalid job id); do not claim a newly
verified exit code. Completion is supported by full history, final sync log,
finished W&B and completed_epochs=50. RTX5090 startup/runtime verified;
master allocation and explicit Vesta exclusion were recorded at launch.
Read-only audit PASS: checkpoint/history, exact configured protocol and seed,
frozen assignment hash and manifests, unique DEV IDs/labels, probabilities,
argmax, recomputed metrics and W&B selected epoch/score.
Best epoch 32: Macro-F1 **0.7951533696**, accuracy 0.8490099010,
QWK 0.6560406431; class F1 [1,0.617284,0.904239,0.659091].
Only 4/50 epochs reach .75; epoch-50 F1 0.5442349138. One DEV A case remains
the rare-class limitation. Numeric screen gate passed, not CV5 success.
All remaining fold manifests and launcher GPU/exclusion guards validated.
Proceed with fresh folds 1--4, same A4 snapshot/config, seed42, 50epochs;
retain completed fold0. No ensemble, no independent-test claim.

A4 confirmation submitted as **766_1--766_4**. Outputs follow
`/slurmshared/Ngoc/runs/hcmus-density-cv5-v1-766-fold{1,2,3,4}`.
Per-task Vesta exclusion verified in Slurm; verify startup GPU and W&B
run IDs before reporting all tasks training. Never resubmit pending jobs.

A4 confirmation startup verified: all four tasks RUNNING; each log reports
NVIDIA GeForce RTX 5090. Folds 1--2 on master, folds 3--4 on worker-1;
no Vesta. W&B IDs in fold order: `5d86ou47`, `dldfsfhr`, `u3dnrb4d`,
`b6xx5bxr`. All initialized online; first epochs pending at this check.

A4 partial completion check: task 766_4 independently verified Slurm
COMPLETED, ExitCode=0:0, worker-1, worker-2 explicitly excluded;
EndTime=2026-09-19T09:08:17. History has 50 epochs, best DEV Macro-F1
0.6354538362180315. Task 766_3 has 50 history epochs but remains RUNNING
at this check; folds 1/2 have 48/47 epochs and remain RUNNING. All recorded
training losses finite. Full CV5 audit and summary publication still pending.

Subsequent Slurm check: 766_3 COMPLETED, ExitCode=0:0, worker-1,
worker-2 explicitly excluded, EndTime=2026-09-19T09:08:42. History has
50 epochs, best DEV Macro-F1 0.5602209077695116. Folds 1/2 remain
RUNNING with 48 epochs each; do not infer complete CV5 from partial results.

Task 766_1 subsequently verified COMPLETED, ExitCode=0:0 on master,
worker-2 excluded, EndTime=2026-09-19T09:11:09. Task 766_2 still RUNNING
at this terminal-state check. No new training submitted.

## A4 completed CV5 audit (2026-09-19)

766_2 verified COMPLETED ExitCode=0:0, master, worker-2 excluded,
EndTime=2026-09-19T09:11:28. All five runs completed 50 epochs.
Full checkpoint/history/manifest/prediction/W&B audit PASS, 2017 unique cases.
Mean Macro-F1 0.6526148621123234; sample SD 0.09636315843367353.
Accuracy 0.842334717342702; QWK 0.6560994857754112.
Mean F1 A/B/C/D [0.433333,0.685194,0.900582,0.591350];
B/C/D mean 0.7257087050386535. Epoch-50 mean 0.5156552271275029.
A4 falls below A1 by 2.736 percentage points; target not met, no multiseed
expansion. Best completed CV5 remains A1 at 0.6799754745. These are
selected DEV results, not independent-test or ensemble results.
Reports: vindr_auggeo_ordinal10_cv5_results_20260919.json/.md.
W&B summary hpjh9blm published; finished state, matching mean, 2017 cases,
fold table, audit artifact and non-independent/non-multiseed flags verified.
No training jobs remain from A4 and no next trial has yet been submitted.

## A5 preregistration: dropout 0.3 on A1

A1 remains the best complete CV5 reference. Test only model.dropout 0.1 ->
0.3 with its augmentation, LR, losses, seed and frozen split unchanged.
The selected-vs-final-epoch gap motivates a regularization test but does not
prove overfitting. D1 (dropout on B0) and O3 (dropout on low LR) did not pass
the screen; neither isolated dropout in the A1 augmentation setting.
Config: vindr_density_auggeo_dropout30.yaml; arm auggeo_dropout30.
Fresh ImageNet initialization, fixed fold0, 50 epochs, RTX5090, no Vesta.
Finish and audit fold0 before expansion; gate best DEV Macro-F1 >=0.75.
Do not treat a single A case as robust evidence, change the gate/split,
ensemble checkpoints, or claim independent-test/multiseed success.

A5 deployment cloned from immutable A1 snapshot to
`/slurmshared/Ngoc/code/hcmus-density-auggeo-dropout30-20260919-v1`.
Verified exact one-factor config difference, source/launcher byte parity,
all five frozen manifests and assignment hash, RTX5090 and exclusion guards.
Submitted fold0 only as 770_0; verified RUNNING on master, worker-2 excluded.
Startup reports NVIDIA GeForce RTX5090. W&B run `dw97b5oh` initialized:
https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/dw97b5oh
Output `/slurmshared/Ngoc/runs/hcmus-density-cv5-v1-770-fold0`.
No result yet at startup; await full 50 epochs and audit before expansion.

A5 provisional screening gate reached at epoch20: DEV Macro-F1
0.7654421854687274, accuracy 0.7970297029702971, QWK 0.6126648582920213.
Class F1 [1.0,0.6086956522,0.8637873754,0.5892857143]; one DEV A case.
Only 1 of the first20 epochs exceeds .75. Slurm770_0 verified RUNNING;
all recorded train loss values finite. This is not a completed-screen audit
or CV5 success. Finish50 and audit before submitting any confirmation folds.

## A5 completed screening audit; expand folds1--4

770_0 independently verified Slurm COMPLETED ExitCode=0:0 on master,
worker-2 excluded, EndTime=2026-09-19T10:10:20. Exactly50 history epochs;
all recorded training losses finite; W&B dw97b5oh finished completed_epochs50.
Read-only audit PASS: exact configured checkpoint/protocol/seed42/hash,
checkpoint selection/history, unique exact DEV IDs/labels, finite normalized
probabilities/argmax, recomputed F1/accuracy/QWK/class F1/confusion matrix,
matching W&B score/epoch. Remaining four frozen manifests validated.
Best epoch30 Macro-F1 0.7896498561536562, accuracy 0.8267326732673267,
QWK 0.6486083499005965. ClassF1 [1,0.641975309,0.885993485,0.630630631].
Only5/50 epochs reach .75; epoch50 Macro-F1 0.5147925057537399.
Numeric gate passed, not CV5/multiseed success. One DEV A case remains a
limitation. Proceed with fresh folds1--4 on same snapshot/config, retaining
completed fold0; no ensemble or independent-test claim.

A5 confirmation submitted as array771 folds1--4. All four tasks verified
RUNNING, RTX5090 startup confirmed, worker-2 explicitly excluded. Folds1/2
on master, folds3/4 on worker-1. W&B initialization seen for fold1 bdqa6i73,
fold2 v9o9ybpf, fold4 sw2g78c4; fold3 metadata pending at this check.
Outputs `/slurmshared/Ngoc/runs/hcmus-density-cv5-v1-771-fold{1,2,3,4}`.
Do not resubmit; monitor these handles through completion.

A5 subsequent startup check: all four tasks remain RUNNING and W&B metadata
now exists for every fold. Fold3 run ID is 26mytlgm (others unchanged).
First epoch pending for all four at this check; no training metrics yet.

## A5 completed CV5 audit (2026-09-19)

All five folds completed50; confirmation771 tasks verified COMPLETED exit0,
master folds1/2 and worker1 folds3/4, worker2 excluded. End times f1
11:23:01, f2 11:23:04, f3 11:20:22, f4 11:19:52. Read-only full audit
PASS including finished W&B and exact frozen prediction membership.
Report: `vindr_auggeo_dropout30_cv5_results_20260919.{json,md}`.
Mean DEV Macro-F1 0.7028282800839902, sample SD 0.1172888127211152;
accuracy 0.8373756234184212, QWK 0.6707563557578502.
Class means [0.6,0.6818263058327866,0.8937691979216775,0.635717616581497];
BCD 0.7371043734453203; epoch50 mean 0.5598344538246729.
New highest completed mean, +2.2853pp over A1, but higher fold dispersion,
zero A F1 in folds1/3, and persistent selected-versus-final gap. Below .75;
not independent-test or multi-seed success. No ensemble.
W&B summary bj99x9ia independently verified finished, exact mean, 2017
cases, fold table, audit artifact and false independent/multi-seed flags.
No next arm submitted yet; inspect paired errors/dynamics before choosing
the next controlled fixed-fold0 screen.

## A5 follow-up diagnostic

Saved `vindr_a5_followup_diagnostic_20260919.md` and raw history extracts
`vindr_a5_training_dynamics_20260919.json`. A5 improves D in four folds,
B in three and C in three; mean A F1 slightly decreases. D-to-C errors
127 -> 96, with C-to-D 66 -> 92. Last10 fold means approximately
[.498406,.510217,.494195,.517960,.734042]; late deterioration persists.
Sparse AMP skipped updates occur throughout training (totals16/18/16/17/15),
not only startup; no evidence yet of causal responsibility. Scalar loss
magnitudes alone do not prove gradient domination or overfitting.
Next candidate question: modest sampling_power=.25 on A5, one-factor
fixed-fold0 screen. Prior O2 failure on low-LR parent remains contrary
evidence; any benefit on A5 must be demonstrated. A6 not yet configured
or submitted; complete preregistration and snapshot validation first.

## A6 preregistration: tempered sampling on A5

Config `configs/vindr_density_auggeo_dropout30_sampling025.yaml`, arm
`auggeo_dropout30_sampling025`. Only training sampling changes from natural
shuffle without replacement to FIT-only inverse-frequency power .25,
with replacement and unchanged draws per epoch. Keep loss weights fixed;
effective training class exposure changes deliberately, not DEV membership.
Hypothesis: modest minority exposure may improve B/D and A retention on
A5; prior O2 failure on a different parent is acknowledged. No promised gain.
Fresh fixed fold0, seed42, full50, original frozen manifests/cache,
shared DenseNet121/hierarchical fusion and single-checkpoint inference.
RTX5090 guard and worker2 exclusion mandatory. No ensemble.
Only expand folds1--4 after completed50 audit and fold0 best DEV F1 >= .75;
retain screen fold0, no favorable-fold selection. Success still requires
mean CV5 >= .75 plus multiple seeds; selected DEV is not independent test.
Snapshot planned: `/slurmshared/Ngoc/code/hcmus-density-auggeo-dropout30-sampling025-20260919-v1`.

A6 deployed and validated: config differs only in sampling power plus arm
metadata, source/scripts byte-identical to A5, all5 frozen manifests and
assignment hash validated, seed42/full50 and GPU/exclusion guards intact.
Fold0 FIT expected sampling probabilities A/B/C/D:
[.0107289955,.1416364423,.6725252186,.1751093435], 1613 draws/epoch.
Submitted fixed fold0 as 775_0; verified RUNNING on master with startup
GPU NVIDIA GeForce RTX5090. W&B initialized qla23v5w:
https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/qla23v5w
Output `/slurmshared/Ngoc/runs/hcmus-density-cv5-v1-775-fold0`.
No result yet. Monitor this handle; do not resubmit or expand before
completed50 and screen audit.

## A6 completed screen; expand folds1--4

775_0 completed50, Slurm COMPLETED exit0 on master, worker2 excluded,
EndTime 2026-09-19T12:24:29. Read-only screen audit PASS including all5
frozen manifests, exact checkpoint/predictions and finished W&B qla23v5w.
Best epoch4 DEV Macro-F1 0.782979257528481, accuracy 0.8143564356435643,
QWK 0.6444663475077442, class F1
[1,.5957446808510638,.8756218905472637,.6605504587155964]. Only1/50
epochs >=.75; epoch50 .5547746826816594. Screen passes numeric gate but is
slightly below A5 fold0 .7896498562 and contains one A case. Not CV5,
multiseed or independent-test success. Report:
`vindr_a6_sampling025_screen_20260919.{json,md}`. Retain this fold0 and
launch fresh folds1--4 from the same immutable snapshot; no ensemble.

A6 confirmation submitted as array776 folds1--4 after screen audit. Config
SHA256 `3d351ee2ce8a5ce3eb2723d2a36eb8ea60dc7252bc77b746a91b5bb6454f75ad`.
All four tasks independently verified RUNNING: folds1/2 on master and
folds3/4 on worker1; each reports NVIDIA GeForce RTX5090 and explicitly
excludes worker2. Outputs `/slurmshared/Ngoc/runs/hcmus-density-cv5-v1-776-fold{1,2,3,4}`.
Do not resubmit. Monitor through completed50, then combine with retained
775-fold0 for full audit and W&B summary.

## A6 completed CV5 audit (2026-09-19)

All five folds completed50. Confirmation776 tasks independently verified
COMPLETED with ExitCode=0:0; folds1/2 ran on master, folds3/4 on worker1,
worker2 excluded, and RTX5090 startup previously verified. Full read-only
audit PASS: common config/architecture, checkpoint/history, all frozen
manifests/hash, exact prediction membership/labels, normalized probabilities,
recomputed metrics, 2017-case union, and all five W&B source runs finished50.

Fold Macro-F1 values are [.7829792575, .6194960833, .6868304061,
.6552764923, .6381746803], best epochs [4,25,12,3,8]. Mean 0.6765513839,
sample SD 0.0644461991; accuracy 0.8205365698, QWK 0.6528158653. Mean class
F1 [0.56, .6417969022, .8837216711, .6206869623], BCD .7154018452;
epoch50 mean .5297036255. Support remains [6,196,1556,259].

A6 is 2.6277 percentage points below A5 and lowers every mean class F1;
lower fold dispersion does not offset the mean loss. Reject sampling_power
.25 on A5 and retain A5 as best completed CV5 (.7028282801). Target .75 is
not met; results are selected DEV, not independent test or multiseed success.
Reports: `vindr_auggeo_dropout30_sampling025_cv5_results_20260919.{json,md}`.
Audited W&B summary `nixhkmas` was independently verified finished with exact
mean/SD, 2017 cases, fold table, audit artifact, and all success/test flags
false as appropriate:
https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/nixhkmas
No next arm submitted by this audit.

## A7 preregistration: stronger AdamW weight decay on A5

Config `configs/vindr_density_auggeo_dropout30_wd5e4.yaml`, arm
`auggeo_dropout30_wd5e4`. Return to A5 as the parent because A6 sampling
reduced every mean class F1. Change only `training.weight_decay` from 1e-4
to 5e-4. Keep A5 augmentation, dropout .3, LR 5e-5, losses, natural FIT
sampling, stretch512 preprocessing, seed42, frozen split and shared
DenseNet121/hierarchical fusion unchanged. Inference remains the flat head
from one best checkpoint; no ensemble.

Rationale: A5 has the best completed CV5 mean, but selected checkpoints are
often much earlier than epoch50 and late deterioration persists. A moderate
fivefold increase in decoupled weight decay is a one-factor regularization
test; this pattern does not prove it will help. Run fixed fold0 for all 50
epochs first. Expand fresh folds1--4 only after a completed audit with best
DEV Macro-F1 >= .75; retain fold0 if expanded. Success still requires CV5
mean >= .75 and multiple seeds. Selected DEV is not an independent test.
RTX5090 guard and worker2 exclusion remain mandatory.

A7 snapshot `/slurmshared/Ngoc/code/hcmus-density-auggeo-dropout30-wd5e4-20260919-v1`
was cloned from immutable A5. Semantic config diff is exactly arm metadata plus
weight_decay 1e-4 -> 5e-4; source/scripts are byte-identical to A5. Config
SHA256 `3d7fdf0f82224a219e274ebc34d9e053e174245dc63e7d5816275e5344cde050`.
Frozen fold0 manifests validated against assignment SHA256
`43daa86936ee7b1bae1b200836fb1afdfe0c8294c7c865d8f5758bf989f12a9a`.
Submitted only fold0 as job780_0. Verified RUNNING on master, NVIDIA GeForce
RTX 5090, worker2 excluded, no requeue. Output
`/slurmshared/Ngoc/runs/hcmus-density-cv5-v1-780-fold0`; W&B `k0rg6gfh`:
https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/k0rg6gfh
Do not expand before completed50 audit and the preregistered >=.75 gate.

## A7 completed screen; expand folds1--4

780_0 completed50 and Slurm reports COMPLETED, ExitCode=0:0 on master,
worker2 excluded, no requeue, EndTime=2026-09-19T19:25:17. Read-only screen
audit PASS including all5 frozen manifests, exact checkpoint/predictions and
finished W&B k0rg6gfh. Best epoch30 DEV Macro-F1 0.7896498561536562,
accuracy 0.8267326732673267, QWK 0.6486083499005965, class F1
[1,.6419753086419753,.8859934853420195,.6306306306306306]. Five/50
epochs reached .75; epoch50 was .5147925057537399. No severe errors and all
logged training losses were finite.

The result is exactly equal to A5 fold0, so stronger weight decay has not
shown a screen improvement. It nevertheless passes the preregistered numeric
gate. Report: `vindr_a7_wd5e4_screen_20260919.{json,md}`. Retain this fold0
and launch fresh folds1--4 from the same immutable snapshot; no ensemble.
CV5, multiseed and independent-test success remain unverified.

A7 confirmation submitted as array781 folds1--4 after the passing screen
audit. Config SHA256 remains
`3d7fdf0f82224a219e274ebc34d9e053e174245dc63e7d5816275e5344cde050`.
All four tasks were independently verified RUNNING: folds1/2 on master and
folds3/4 on worker1; each reports NVIDIA GeForce RTX 5090, explicitly excludes
worker2, has requeue disabled, and uses the identical immutable snapshot.
Outputs are `/slurmshared/Ngoc/runs/hcmus-density-cv5-v1-781-fold{1,2,3,4}`.
Do not resubmit. Monitor these handles through completed50, then combine with
retained 780-fold0 for the full CV5 audit and W&B summary.

A7 confirmation W&B runs initialized: fold1 `sk8n4sx4`, fold2 `7wx8eyje`,
fold3 `5uvzzdwk`, fold4 `w576p0g1`. All are under
`TN_Mammo_BreastDensity/HCMUS-paper1`; continue monitoring job781 rather than
resubmitting.

## A7 runtime diagnostic: configured decay is a float32 no-op

During confirmation, A7 reproduced every completed A5 validation record and
logged train scalar exactly: fold0 50/50, folds1/2 26/26, folds3/4 27/27 at
the diagnostic snapshot. Selected checkpoint state dictionaries for all five
folds are bit-for-bit identical with matching SHA256, even though checkpoint
configs correctly store A5 wd=1e-4 and A7 wd=5e-4. Source passes the setting
to AdamW, so this is not a missing-config wiring error.

Direct runtime arithmetic explains the identity. With LR 5e-5,
`float32(1 - lr*1e-4) == 1.0` and `float32(1 - lr*5e-4) == 1.0`; both
decoupled decay updates are numerically zero. wd=1e-3 is the first tested
value producing a representable factor (0.9999999403953552). A7 is therefore
a no-op replication and must not be interpreted as a negative regularization
result. Finish job781 to preserve the full50 audit. A subsequent controlled
screen should use a materially effective value such as 1e-2, with all other
A5 factors fixed. Diagnostic: `vindr_a7_weight_decay_noop_diagnostic_20260919.md`.

## A7 completed CV5 audit (2026-09-19)

Fold0 job780 and confirmation array781 folds1--4 all completed50. Scheduler
records report COMPLETED ExitCode=0:0; folds1/2 ran on master, folds3/4 on
worker1, worker2 excluded, and RTX5090 startup was previously verified. Full
read-only CV5 audit PASS including common config/architecture, frozen split
hash/manifests, checkpoint/history, exact predictions, recomputed metrics,
2017-case union and five finished W&B source runs.

Fold Macro-F1 values are [.7896498562, .5792311841, .7991001000,
.5701863354, .7759739248], best epochs [30,8,5,3,27]. Mean 0.7028282801,
sample SD 0.1172888127; accuracy 0.8373756234, QWK 0.6707563558. Mean class
F1 [.6,.6818263058,.8937691979,.6357176166], BCD .7371043734; epoch50
mean .5598344538. Support [6,196,1556,259].

All results and selected tensors are exactly identical to A5 because both
configured AdamW factors round to one in float32 at LR5e-5. A7 is a no-op
replication, below the .75 target, and provides no new substantive model
result. Reports: `vindr_auggeo_dropout30_wd5e4_cv5_results_20260919.{json,md}`.
Selected DEV is not independent test evidence and multiseed remains false.

A7 audited W&B summary `iepzqnaa` was independently verified finished with
the exact mean/SD, 2017 cases, five source IDs, fold table, audit artifact,
and false target/independent/multiseed flags:
https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/iepzqnaa

## A8 preregistration: numerically effective AdamW weight decay

Config `configs/vindr_density_auggeo_dropout30_wd1e2.yaml`, arm
`auggeo_dropout30_wd1e2`. Return to substantive parent A5 and change only
`training.weight_decay` from 1e-4 to 1e-2. Keep A5 augmentation, dropout .3,
LR5e-5, losses, natural FIT sampling, stretch512 preprocessing, seed42,
frozen split and shared DenseNet121/hierarchical fusion unchanged. Inference
remains one flat-head checkpoint; no ensemble.

Unlike A7, the configured float32 AdamW factor is representably below one:
`float32(1 - 5e-5*1e-2) = 0.9999995231628418`. Hypothesis: materially
effective decoupled regularization may reduce A5's late deterioration and
improve B/D stability; no gain is assumed. Run fresh fixed fold0 for all50
epochs first. Expand fresh folds1--4 only after completed audit and best DEV
Macro-F1 >=.75; retain fold0 if expanded. Success still requires CV5 mean
>=.75 and multiple seeds. DEV is not an independent test. RTX5090 guard,
worker2 exclusion and no-requeue are mandatory.

A8 deployed from immutable A5 snapshot to
`/slurmshared/Ngoc/code/hcmus-density-auggeo-dropout30-wd1e2-20260919-v1`.
Semantic config diff is exactly arm metadata plus weight_decay 1e-4 -> 1e-2;
source/scripts are byte-identical to A5. Config SHA256
`2d0424bbd5f27f3673fe49ba541a8e66a70b29ca267dab4c1e4c51f957b1a749`
and frozen assignment SHA256 remains
`43daa86936ee7b1bae1b200836fb1afdfe0c8294c7c865d8f5758bf989f12a9a`.
Submitted only fixed fold0 as job785_0. Verified RUNNING on master with NVIDIA
GeForce RTX 5090, worker2 excluded and requeue disabled. Output
`/slurmshared/Ngoc/runs/hcmus-density-cv5-v1-785-fold0`. Do not expand before
completed50 audit and the preregistered >=.75 gate.

A8 W&B initialized as `s9v0d7rc`:
https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/s9v0d7rc
Epoch1 confirms this is not a no-op replication. A8 DEV Macro-F1
0.5498785544 versus A5 0.5306046243; train loss 0.9834280020 versus
0.9755466363. Validation records and train scalars differ while sampled class
counts remain identical, as required for the one-factor comparison. Continue
job785_0 through full50 before screen audit or expansion.

A8 provisional gate reached at epoch17: fold0 DEV Macro-F1
0.7695135209104663, accuracy 0.8366336633663366, QWK 0.6144592249855407,
class F1 [1,.6279069767,.8975155280,.5526315789]. Confusion matrix
`[[1,0,0,0],[0,27,13,0],[0,19,289,3],[0,0,31,21]]`; no severe errors.
This is below A5 fold0 0.7896498562 and includes only one A case, so it is
not an improvement or success claim. Job785_0 remains RUNNING; finish50 and
audit before any folds1--4 expansion.

A8 provisional best improved at epoch25 to fold0 DEV Macro-F1
0.7922563838314439, 0.2607 percentage points above A5 fold0. Accuracy
0.8292079207920792, QWK 0.6502208391889179, class F1
[1,.6478873239,.8878048780,.6333333333], confusion matrix
`[[1,0,0,0],[0,23,17,0],[0,8,273,30],[0,0,14,38]]`, no severe errors.
Three of the first25 epochs are >=.75. This remains a provisional selected-DEV
screen with one A case, not a completed audit or CV5 success. Finish50 before
expansion.

A8 provisional best improved again at epoch29 to DEV Macro-F1
0.805019305019305, 1.5369 percentage points above A5 fold0. Accuracy
0.8514851485148515, QWK 0.6726801339526844, class F1
[1,.6486486486,.9047619048,.6666666667], confusion matrix
`[[1,0,0,0],[0,24,16,0],[0,10,285,16],[0,0,18,34]]`, no severe errors.
Six of the first29 epochs are >=.75. This is encouraging but still selected
DEV with one A case; job785_0 must finish50 and pass audit before expansion.

## A8 completed screen; expand folds1--4

785_0 completed50 and Slurm reports COMPLETED ExitCode=0:0 on master,
worker2 excluded, no requeue, EndTime=2026-09-19T21:39:50. Read-only screen
audit PASS including all5 frozen manifests, exact checkpoint/predictions and
finished W&B s9v0d7rc. Best epoch29 DEV Macro-F1 0.805019305019305,
accuracy 0.8514851485148515, QWK 0.6726801339526844, class F1
[1,.6486486486,.9047619048,.6666666667]. Twelve/50 epochs reached .75;
epoch50 was .5284265250941791. No severe errors; train losses finite.

A8 is 1.5369 percentage points above A5 fold0 and passes the preregistered
numeric gate. Report: `vindr_a8_wd1e2_screen_20260919.{json,md}`. Retain this
fold0 and launch fresh folds1--4 from the identical immutable snapshot. This
is not CV5, multiseed or independent-test success; no ensemble.

A8 confirmation submitted as array786 folds1--4 after the passing screen
audit. Config SHA256 remains
`2d0424bbd5f27f3673fe49ba541a8e66a70b29ca267dab4c1e4c51f957b1a749`.
All four tasks were verified RUNNING: folds1/2 on master, folds3/4 on worker1;
each reports NVIDIA GeForce RTX 5090, explicitly excludes worker2, has requeue
disabled and uses the identical snapshot/config. Outputs are
`/slurmshared/Ngoc/runs/hcmus-density-cv5-v1-786-fold{1,2,3,4}`. Do not
resubmit; monitor to completed50, then combine with retained 785-fold0 for
full CV5 audit and W&B summary.

A8 confirmation W&B runs initialized: fold1 `tygbgf0f`, fold2 `dm2fjrmx`,
fold3 `1oomcq89`, fold4 `kvyyftup`. All are under
`TN_Mammo_BreastDensity/HCMUS-paper1`; first epochs were still pending at
this check. Continue monitoring job786 and do not resubmit.

## A8 completed CV5 audit (2026-09-19)

Fold0 job785 and confirmation array786 folds1--4 all completed50. Scheduler
records report COMPLETED ExitCode=0:0 with no restart/requeue; folds0--2 ran
on master, folds3/4 on worker1, worker2 was excluded, and RTX5090 startup was
previously verified. Full read-only CV5 audit PASS including common
config/architecture, frozen split hash/manifests, checkpoint/history, exact
predictions, recomputed metrics, 2017-case union and five finished W&B runs.

Fold Macro-F1 values are [.8050193050, .5685669490, .7817985393,
.7093373275, .6253638411], best epochs [29,15,42,18,32]. Mean
0.6980171924, sample SD 0.1007878795; accuracy 0.8413409331, QWK
0.6449785726. Mean class F1 [.6333333333,.6620012689,.9001940430,
.5965401243], BCD .7195784787; epoch50 mean .5251450156. Support
[6,196,1556,259] and no selected prediction has a severe error.

A8 is substantive but 0.4801 percentage points below A5 and below the .75
target. Effective wd=.01 improved fold0 and fold2 and reduced fold SD, but it
did not generalize across fold1/4 and weakened B/D mean F1. A5 remains the
best substantive arm. Selected DEV is not independent test evidence and
multiseed remains false. Reports:
`vindr_auggeo_dropout30_wd1e2_cv5_results_20260919.{json,md}`.

A8 audited W&B summary `irjubusx` was independently read back through the
API and verified finished with exact mean 0.6980171923866632, sample SD
0.10078787949981632, 2017 cases, all five source IDs, the fold-results table,
the audit artifact, and false target/independent/multiseed flags:
https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/irjubusx

## A9 preregistration: dropout 0.5 on A5

Config `configs/vindr_density_auggeo_dropout50.yaml`, arm
`auggeo_dropout50`. Return to substantive best A5 and change only
`model.dropout` from 0.3 to 0.5. Keep augmentation, LR5e-5, wd1e-4, loss
coefficients, natural FIT sampling, stretch512 preprocessing, seed42, frozen
split and shared DenseNet121/hierarchical fusion unchanged. Inference remains
one flat-head checkpoint; no ensemble.

Rationale: increasing dropout from A1's 0.1 to A5's 0.3 raised CV5 mean by
2.2853 percentage points and improved mean B/C/D F1, whereas lower LR,
sampling, ordinal reweighting and effective weight decay did not surpass A5.
Testing 0.5 asks whether stronger stochastic feature regularization extends
that gain; monotonic improvement is not assumed, and A8's negative result is
contrary evidence for generic extra regularization.

Run only fixed fold0 for all50 epochs first. Expand fresh folds1--4 only after
a completed read-only audit and best DEV Macro-F1 >=.75; retain fold0 if
expanded. Success still requires CV5 mean >=.75 and multiple seeds. DEV is
not an independent test. RTX5090 guard, worker2 exclusion and no-requeue are
mandatory.

A9 deployed from immutable A5 snapshot to
`/slurmshared/Ngoc/code/hcmus-density-auggeo-dropout50-20260919-v1`.
Semantic config diff is exactly arm metadata plus dropout 0.3 -> 0.5;
source/scripts are byte-identical to A5. Config SHA256
`f84bb8a3e10205ea0cbce176ec4a376925c67835b105e6cc1da66d0b8286deba`
and frozen assignment SHA256 remains
`43daa86936ee7b1bae1b200836fb1afdfe0c8294c7c865d8f5758bf989f12a9a`.
Submitted only fixed fold0 as job790_0. Verified RUNNING on master with NVIDIA
GeForce RTX 5090, worker2 excluded, requeue disabled and fresh ImageNet
initialization. Output `/slurmshared/Ngoc/runs/hcmus-density-cv5-v1-790-fold0`.
Do not expand before completed50 audit and the preregistered >=.75 gate.

A9 W&B initialized as `wpzkdvb6`:
https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/wpzkdvb6

A9 epoch1 completed with finite loss 0.9910876041, Macro-F1 0.4976938956
and four normal AMP-skipped updates. It differs from A5 epoch1 (loss
0.9755466363, Macro-F1 0.5306046243), confirming the dropout treatment is
active rather than a no-op replication. Continue job790_0 through full50;
the first epoch is not a screening decision.

A9 provisional gate reached at epoch18: fold0 DEV Macro-F1
0.7983834791246115, accuracy 0.8366336633663366, QWK 0.6632653061224489,
class F1 [1,.6666666667,.8932038835,.6336633663], confusion matrix
`[[1,0,0,0],[0,29,11,0],[0,18,276,17],[0,0,20,32]]`, no severe errors.
This passes the numeric screen and is above A5 fold0 .7896498562 by only
0.8734 percentage points, but contains one A case. It is provisional selected
DEV evidence, not CV5 success. Finish job790_0 through epoch50 and audit
before expanding folds1--4.

## A9 completed screen; expand folds1--4

790_0 completed50 and Slurm reports COMPLETED ExitCode=0:0 on master,
worker2 excluded, no restart/requeue. Read-only screen audit PASS including
all5 frozen manifests, exact checkpoint/predictions and finished W&B
`wpzkdvb6`. Best epoch18 DEV Macro-F1 0.7983834791246115, accuracy
0.8366336633663366, QWK 0.6632653061224489, class F1
[1,.6666666667,.8932038835,.6336633663]. Three/50 epochs reached .75;
epoch50 was .5661339637136076. No selected severe errors; train losses finite.

A9 is 0.8734 percentage points above A5 fold0 and passes the preregistered
numeric gate. Report: `vindr_a9_dropout50_screen_20260919.{json,md}`. Retain
this fold0 and launch fresh folds1--4 from the identical immutable snapshot.
This is not CV5, multiseed or independent-test success; no ensemble.

A9 confirmation submitted as array791 folds1--4 after the passing screen
audit. All four tasks were independently verified RUNNING with RTX 5090:
folds1/2 on master and folds3/4 on worker1; worker2 is excluded and
requeue/restarts are zero. Outputs are
`/slurmshared/Ngoc/runs/hcmus-density-cv5-v1-791-fold{1,2,3,4}`. Do not
resubmit; monitor to completed50 and combine with retained 790-fold0.

A9 confirmation W&B runs: fold1 `v0sftza9`, fold2 `5l4utdd3`, fold3
`j28m5ozw`, fold4 `1gkkuyw7`, all under
`TN_Mammo_BreastDensity/HCMUS-paper1`.

## A9 completed CV5 audit (2026-09-20)

Fold0 job790 and confirmation array791 folds1--4 all completed50. Scheduler
records report COMPLETED ExitCode=0:0 with no restart/requeue; folds0--2 ran
on master, folds3/4 on worker1, worker2 was excluded, and RTX5090 startup was
previously verified. Full read-only CV5 audit PASS including common
config/architecture, frozen split hash/manifests, checkpoint/history, exact
predictions, recomputed metrics, 2017-case union and five finished W&B runs.

Fold Macro-F1 values are [.7983834791, .5569145775, .7578714628,
.6431991883, .6046581573], best epochs [18,28,19,34,25]. Mean
.6722053730, sample SD .1024152650; accuracy .8225032553, QWK .6314935199.
Mean class F1 [.6163636364,.6115190727,.8901661405,.5707726425], BCD
.6908192852; epoch50 mean .5354832714. Support [6,196,1556,259] and no
selected prediction has a severe error.

A9 is substantive but 3.0623 percentage points below A5 and below the .75
target. Dropout .5 improved fixed fold0 but reduced B/D discrimination and
did not generalize. A5 remains the best substantive arm. Selected DEV is not
independent-test evidence and multiseed remains false. Reports:
`vindr_auggeo_dropout50_cv5_results_20260920.{json,md}`.

A9 audited W&B summary `khwckzem` was independently read back through the
API and verified finished with exact mean .6722053729986357, sample SD
.10241526502859342, 2017 cases, all five source IDs, fold-results table,
audit artifact, and false target/independent/multiseed flags:
https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/khwckzem

## A9 fold1 root-cause audit

Read-only paired diagnosis against A5 confirms fold1 is not density-count
imbalanced or cache-corrupt: DEV support is [1,39,312,51], membership/hash
passes, and all inspected views are finite valid arrays. Fold1 is
systematically around .55--.62 across all audited arms because one missed A
case sets A-F1 to zero and A contributes 25% of four-class Macro-F1.

A9 also introduces a real failure. At selected epoch28 it recognizes the one
A but predicts nine B cases as A, eight with p(A)>.995. A5 predicts none of
those B cases as A. Paired predictions are 16 corrections versus 31
regressions; A9 selected BCD mean is .6820, and even its best-BCD epoch reaches
only .7364 versus A5 .7723. Fold1 FIT contains five A cases and beta=.999
weights A about 29x B and 143x C; dropout .5 in both relation-fusion stages
destabilizes this highly weighted rare boundary. Do not alter the split or
discard fold1. Reject A9 and retain A5. Full diagnostic:
`vindr_a9_fold1_diagnostic_20260920.md`.

## A10 preregistration: modest label smoothing on A5

Return to substantive best A5 and change only flat-head focal target label
smoothing from 0 to 0.05. Keep dropout .3, augmentation, LR5e-5, wd1e-4,
effective-number beta=.999, all auxiliary losses, natural FIT sampling,
stretch512 preprocessing, seed42, frozen split, architecture and flat-head
inference unchanged. Config:
`configs/vindr_density_auggeo_dropout30_labelsmooth005.yaml`, arm
`auggeo_dropout30_labelsmooth005`.

Rationale: audited selected predictions show material overconfidence even in
A5 (mean confidence .9725, mean confidence on errors .9477, 202/328 errors
above .99 confidence). A9 worsened those figures and its rare A/B boundary.
Smoothing .05 is a modest one-factor test intended to reduce logit saturation,
not a promised F1 gain. Its implementation applies the effective-number
weight only to the observed class, avoiding leakage of the very large A weight
into every smoothed target. A value of zero takes the exact established code
path, preserving prior arms.

Run only fixed fold0 for all50 epochs first on RTX5090, with worker2/Vesta
excluded and no requeue. Expand fresh folds1--4 only after a completed audit
and best four-class DEV Macro-F1 >=.75; retain fold0 if expanded. Success still
requires CV5 mean >=.75 and multiple seeds. DEV is not an independent test,
and the single fold0 A case must not be treated as sufficient evidence.

A10 deployment cloned from immutable A5 to
`/slurmshared/Ngoc/code/hcmus-density-auggeo-dropout30-labelsmooth005-20260920-v1`.
All 17 unit/integration tests pass in the cluster runtime, including exact
zero-smoothing backward compatibility, opt-in smoothed focal behavior, finite
backpropagation and invalid-range rejection. Semantic config comparison proves
the only treatment is label_smoothing 0 -> .05 plus arm metadata. Other
runtime source/scripts remain A5; `loss.py` contains only the opt-in treatment.
Config SHA256 is
`9f8c9c7e58eda25f011ed1eeb4965c49f79613786ed5615841af33be72714f61`;
frozen assignment SHA remains
`43daa86936ee7b1bae1b200836fb1afdfe0c8294c7c865d8f5758bf989f12a9a`.

Submitted only fixed fold0 as job803_0. Verified RUNNING on
slurm-b20a-master-0 with NVIDIA GeForce RTX 5090, worker2 excluded, requeue0,
restarts0, fresh ImageNet initialization and correct label_smoothing=.05
config. Output `/slurmshared/Ngoc/runs/hcmus-density-cv5-v1-803-fold0`.
W&B initialized as `xtmvoors` under `TN_Mammo_BreastDensity/HCMUS-paper1`.
Do not expand before completed50 audit and the preregistered >=.75 gate.

A10 epoch1 completed with finite losses and identical natural sampled counts
[5,156,1245,207] to A5. The focal component differs (.1521952144 versus
.1531079734) and DEV Macro-F1 differs (.5355348674 versus .5306046243),
confirming the opt-in treatment is active rather than a no-op. Continue
job803_0 through full50; do not interpret or expose single-epoch fluctuation.

A10 epoch10 checkpoint: best so far is epoch8 Macro-F1 .5481450566,
accuracy .8217821782, QWK .6619561175, class F1
[0,.6111111111,.8814691152,.7], no severe errors. This is only +.2896
percentage points over A5's best in its first10 epochs (.5452488632), has no
epoch >=.75, and current selected prediction confidence remains high (mean
.9722; 34/72 errors above .99). There is no evidence yet that smoothing .05
solves calibration or clears the gate. Job803_0 remains RUNNING; continue to
the next 10--20 epoch checkpoint without expansion.

A10 provisional numeric gate reached at epoch19: fold0 DEV Macro-F1
.7743055556, accuracy .8094059406, QWK .6146141372, class F1
[1,.5555555556,.875,.6666666667], confusion matrix
`[[1,0,0,0],[0,30,10,0],[0,37,266,8],[0,1,21,30]]`. One severe D->B error
is present. This is +.8863 percentage points versus A5's best within its first
20 epochs (.7654421855), but below completed A5 fold0 .7896498562 and again
depends on one correctly classified A case. Selected mean confidence .9818
and 58/77 errors exceed .99, so smoothing .05 has not yet improved calibration.
This is provisional selected DEV only. Finish job803_0 through epoch50 and
audit before any expansion.

A10 epoch30 checkpoint: best remains epoch19 at .7743055556; only one of 30
epochs is >=.75. A5 has reached its completed fold0 best .7896498562 by the
same epoch horizon, so A10 is now 1.5344 percentage points lower. A10 best
BCD mean is .6991 versus A5 .7195, and the A10 checkpoint retains one severe
D->B error plus high confidence. The numeric screen is not a substantive
improvement. Job803_0 remains RUNNING; finish50 and audit before rejection or
expansion.

A10 epoch40 checkpoint is unchanged: selected epoch19 Macro-F1 .7743055556,
and only 1/40 epochs reaches .75. It remains 1.5344 percentage points below
A5 fold0, with lower accuracy/QWK, lower BCD mean and one selected severe
error. Epoch40 itself is .5603850 and has two severe errors. There is no new
evidence for expansion; job803_0 remains RUNNING to the mandatory epoch50
audit.

## A10 completed screen; expand folds1--4

803_0 completed50 and Slurm reports COMPLETED ExitCode=0:0 on master,
worker2 excluded, no restart/requeue. Read-only screen audit PASS including
all5 frozen manifests, exact checkpoint/predictions and finished W&B
`xtmvoors`. Best epoch19 DEV Macro-F1 .7743055556, accuracy .8094059406,
QWK .6146141372, class F1 [1,.5555555556,.875,.6666666667]. Only 1/50
epochs reaches .75; epoch50 is .6400411737. One selected severe error.

A10 is 1.5344 percentage points below A5 fold0 and does not improve
calibration, but it passes the preregistered completed-audit numeric gate.
Changing the expansion rule after observing the result would be invalid.
Report: `vindr_a10_labelsmooth005_screen_20260920.{json,md}`. Retain this
fold0 and launch fresh folds1--4 from the identical snapshot. This is not CV5,
multiseed or independent-test success; no ensemble.

A10 confirmation submitted as array808 folds1--4 after the passing screen
audit. All four tasks were verified RUNNING with NVIDIA GeForce RTX 5090:
folds1/2 on worker1 and folds3/4 on worker3; worker2/Vesta is explicitly
excluded, requeue0 and restarts0. Outputs are
`/slurmshared/Ngoc/runs/hcmus-density-cv5-v1-808-fold{1,2,3,4}`. W&B runs:
fold1 `tisnlj5n`, fold2 `5b9sxa0q`, fold3 `bws0jj96`, fold4 `ubyreidu`.
Do not resubmit; monitor to completed50 and combine with retained 803-fold0.

A10 confirmation checkpoint after every fold reached at least epoch10:
fold1--4 best Macro-F1 [.5605285498,.5570013599,.5523447365,
.5480723611]. All four currently miss every DEV A case. Combined with retained
fold0, provisional selected mean is .5984505126 (sample SD .0984184998), while
mean BCD F1 is .7312673501. This is early selected-DEV evidence only; all jobs
remain RUNNING with finite losses and no restart. Continue to epoch20 without
intervention.

A10 confirmation checkpoint after all folds reached epoch20 (folds3/4 had
22): fold1--4 best Macro-F1 [.5605285498,.7777574787,.5863494758,
.6128367003]. Combined with retained fold0, provisional selected mean is
.6623555520 (sample SD .1054136930); mean class F1 is
[.5527272727,.6237505727,.8884700408,.5844743220] and BCD mean .6988983118.
Fold2's high score again includes its sole correct A; fold3 has one severe
error. This remains below A5 and is not stable evidence. All tasks remain
RUNNING with finite losses; continue to epoch30 without intervention.

A10 confirmation checkpoint after every fold reached at least epoch30
(folds3/4 at34): fold1--4 best Macro-F1 [.5605285498,.7777574787,
.7189233954,.6145617367]. Combined with retained fold0, provisional mean is
.6892153432 (sample SD .0975910781). Mean class F1 is
[.6133333333,.6476419966,.8928492465,.6030367965], BCD .7145093466.
Fold3 improved substantially at epoch34 with zero severe errors, but the
provisional mean remains 1.3613 percentage points below A5. All jobs remain
RUNNING with finite losses; continue to epoch40.

A10 verified wait: array808 tasks1--4 are RUNNING on worker1/worker3;
histories reached [43,42,47,47] epochs, with finite scalar training losses.
Selected best scores remain unchanged from the preceding checkpoint.
Fold1 diagnostic was qualified to separate numerical cache checks from
visual/label verification and single-seed observations from causal claims.
A3 tested beta=.99 on A1, not A5; it does not rule out that controlled
experiment on A5. Do not interrupt or duplicate the active A10 jobs.

A10 partial completion: scontrol confirms 808_3 and 808_4 COMPLETED,
ExitCode=0:0, Restarts=0, Requeue=0 on worker3, worker2 excluded, end
2026-09-20T03:26:21 (scheduler timestamp). Both histories contain50 epochs
and finite scalar training losses. Tasks808_1/2 remain authoritatively
RUNNING on worker1 at46/45 epochs. Full CV5 audit/publication remains
pending; do not treat partial completion as a completed experiment.

A10 completed: 808_1/2 also COMPLETED ExitCode0:0, no restarts/requeue,
worker1, worker2 excluded. Full50 CV5 audit PASS including finished W&B
source runs. Mean .689215343247612, sample SD .09759107813789597,
accuracy .8314387145910621, QWK .6398358961418336, BCD .7145093466.
Report vindr_auggeo_dropout30_labelsmooth005_cv5_results_20260920.json.
Published summary jjjwj8l0. Reject A10 as improvement: 1.3613pp below A5;
retain A5. A11 beta=.99 on A5 is prepared but not submitted yet.

## A11 submitted: beta .99 on A5

After completed A10 audit, submitted fixed fold0 only as830_0. Snapshot
/slurmshared/Ngoc/code/hcmus-density-auggeo-dropout30-beta99-20260920-v1
is copied from immutable A5; all Python source/scripts and sbatch scripts
compared byte-identical. Parsed config differs only in loss.beta and arm.
Config SHA256 6578471429566a77730a7ec8c0fa72f3f4881bc5a79c6246d25a003b6c59cecd.
Verified RUNNING on master, startup GPU NVIDIA GeForce RTX5090,
worker2 excluded, Restarts=0/Requeue=0. Output
/slurmshared/Ngoc/runs/hcmus-density-cv5-v1-830-fold0.
Follow full50 screen/audit gate before any expansion; do not duplicate job.

A11 startup confirmed first completed epoch with finite training losses,
natural FIT sampled counts [5,156,1245,207], unfrozen backbone and four AMP
skipped updates. W&B initialized as xls5diws under HCMUS-paper1. Job830_0
remains RUNNING. The treatment is active (first-epoch focal .1784488358
versus A5 .1531079734); no inference about final benefit from one epoch.
Next result checkpoint at10 completed epochs, not per-epoch reporting.

A11 epoch10 checkpoint: best epoch6 Macro-F1 .5551281627070788,
accuracy .8193069306930693, QWK .6787643778319972, class F1
[0,.6481481481481481,.8767123287671232,.6956521739130435], zero severe
errors. A5 best within first10 is .5452488631717199: A11 is +.98793pp,
but still misses DEV A and is far below expansion gate. Job830_0 verified
RUNNING with finite scalar training losses. Continue unchanged to epoch20;
no expansion or claim of final improvement.

A11 epoch20 checkpoint: best epoch20 Macro-F1 .7134904360591527,
accuracy .844059405940594, QWK .6477861143400612, class F1
[.6666666666666666,.6451612903225806,.9001584786053882,.6419753086419753].
Selected CM [[1,0,0,0],[0,30,10,0],[1,23,284,3],[0,0,26,26]]:
one severe C->A error. A5 at same20 horizon reaches .7654421854687274;
A11 has better B/C/D F1 but lower A precision and lower four-class score.
Still below .75 gate, so no expansion. Job830_0 RUNNING, scalar training
losses finite; continue unchanged through50 with next update at30.

A11 epoch30: selected epoch28 Macro-F1 .7988504202283031, accuracy
.844059405940594, QWK .6642570704938793, class F1
[1,.6292134831460674,.8995215311004785,.6666666666666666], no severe
errors. Three of first30 epochs reach .75. A5 best at same horizon is
.7896498561536562: +.92006pp, with modest BCD mean improvement as well.
This is provisional fold0 DEV only and includes one correct A case.
Job830_0 remains RUNNING with finite training losses. Complete50 and audit
before any folds1--4 expansion; next result update at40.

A11 epoch40 checkpoint: best epoch32 Macro-F1 .8191309545894915,
accuracy .8613861386138614, QWK .6977986749305407, class F1
[1,.6666666666666666,.910828025477707,.6990291262135923], zero severe
errors. Twelve of40 epochs reach .75; epoch40 itself .8155008826125332.
Above completed A5 fold0 by2.94811pp, with B/C/D each improved at selected
checkpoint. Still single-fold selected DEV including one A case; not CV5
or seed stability evidence. Job830_0 RUNNING with finite scalar losses.
Finish50 and audit before expanding folds1--4.

A11 completed50 screen: job830_0 COMPLETED ExitCode0:0, master,
worker2 excluded, Restarts=0/Requeue=0. Screen audit PASS, finished W&B
xls5diws; best epoch43 .819363312392079, accuracy .8638613861386139,
QWK .697374155589453, class F1 [1,.6666666667,.9131121643,.6976744186].
Zero selected severe errors; epoch50 .811754225568901, 22/50 >=.75.
Report vindr_a11_beta99_screen_20260920.{json,md}. Gate passed; submitted
fresh folds1--4 as array843 (max4 concurrent), same immutable snapshot and
verified unchanged config SHA. Retain830-fold0; outputs for confirmation
/slurmshared/Ngoc/runs/hcmus-density-cv5-v1-843-fold{1,2,3,4}.
Do not resubmit. This is not yet CV5 or multi-seed success.

A11 confirmation startup: all843_1--4 verified RUNNING, fold1 on master,
folds2--4 on worker1. Each startup log confirms NVIDIA GeForce RTX5090.
W&B metadata initialized: fold1 ey9tr9vs, fold2 r6fc72v9, fold3 hyoelr3s,
fold4 dqsycgev, all under TN_Mammo_BreastDensity/HCMUS-paper1.
No completed history yet at this check; next result checkpoint after all
four reach10 epochs. Keep retained830-fold0 for the final CV5 audit.

A11 confirmation first10-epoch common horizon (actual progress13/10/10/10):
selected fold1--4 Macro-F1 [.5584428851144086,.5328153988868274,
.5554252673062635,.5289415171795353]. Each selected checkpoint misses
all DEV A cases. Fold3 selected checkpoint has one severe D->B error;
others zero. All four jobs RUNNING with finite scalar training losses.
These are first10 selected DEV scores, not final CV5. Continue unchanged
to the next common20 horizon; retain full50 fold0 separately.

A11 confirmation first20-epoch common horizon (actual progress26/20/20/20):
selected fold1--4 Macro-F1 [.5584428851144086,.5359221568728612,
.5676297187477672,.531568716926748], selected epochs [2,15,12,19].
Accuracy [.8610421836,.8287841191,.8638613861,.8213399504];
QWK [.6614359867,.6121595046,.6845900522,.6244661300].
Selected class F1 rows:
[0,.6956521739,.9144634526,.6236559140],
[0,.7323943662,.8920634921,.5192307692],
[0,.7142857143,.9170579030,.6391752577],
[0,.6588235294,.8849270665,.5825242718].
All selected checkpoints miss DEV A, with zero severe errors. Jobs843_1--4
verified RUNNING on master/worker1; all observed scalar losses finite.
No final CV5 conclusion. Continue unchanged to50; next common-horizon
report at30. Fold1 interim diagnosis saved separately in
vindr_a11_fold1_interim_diagnostic_20260920.md; visual review still pending.

A11 confirmation first30-epoch common horizon (actual38/30/30/30):
selected fold1--4 Macro-F1 [.5584428851144086,.5359221568728612,
.5676297187477672,.6040863461346134], selected epochs [2,15,12,23].
Folds1--3 selected checkpoints unchanged from first20. Fold4 selected
accuracy .794044665012407, QWK .6162917417090155, class F1
[.4,.5858585858585859,.8679867986798679,.5625], confusion matrix
[[1,0,0,0],[3,29,7,0],[0,31,263,17],[0,0,25,27]].
Fold4 Macro-F1 improvement is driven by A while B/C/D each decline versus
its first20 selection; not evidence of broad improvement. All four jobs
verified RUNNING on master/worker1, recorded scalar losses finite.
Continue unchanged to50; next common-horizon report40. Not final CV5.

A11 fold1 completed50: scheduler843_1 (JobId844) COMPLETED ExitCode0:0,
Restarts=0/Requeue=0, master, worker2 excluded; EndTime2026-09-20T05:42:58.
History best epoch38 Macro-F1 .5639564704060698, accuracy .8734491315136477,
QWK .6714936466075281, class F1 [0,.75,.9235474006116208,.5822784810126582].
Confusion [[0,1,0,0],[0,27,12,0],[0,5,302,5],[0,0,28,23]], zero severe.
All50 epochs miss DEV A; all scalar training losses finite. Epoch50
Macro-F1 .5401164421997755. Full checkpoint/prediction/W&B audit pending
completion of folds2--4 (verified RUNNING at38 each). No final CV5 claim.

A11 first40 common horizon (actual50/40/40/40): best fold1--4 Macro-F1
[.5639564704060698,.5359221568728612,.5676297187477672,.6040863461346134],
selected epochs [38,15,12,23]. Folds2--4 unchanged from first30 selections;
fold1 matches its completed50 selection above. All recorded losses finite.
843_2--4 verified RUNNING on worker1; fold1 already completed successfully.
Continue remaining folds to50 and then perform complete CV5 audit and W&B
summary. No broad improvement or final CV5 success established.

A11 completed CV5 audit PASS: mean .6181916009106782, sampleSD
.11503828758684345, accuracy .8448001375819965, QWK .6563818201449779.
Class means [.28,.68984106660163,.902753551725075,.6001717853160075];
BCD .7309221345475708. Reject relative to A5 .7028282800839902.
All843 confirmation jobs COMPLETED ExitCode0:0, no restart, allowed nodes.
Reports vindr_auggeo_dropout30_beta99_cv5_results_20260920.{json,md}.
Published W&B summary6kdi88iz; retain A5 parent. No new job submitted.

A12 subsequently preregistered: A5 focal gamma2->1 only, arm
auggeo_dropout30_gamma1. Immutable A5 copy at
/slurmshared/Ngoc/code/hcmus-density-auggeo-dropout30-gamma1-20260920-v1.
Parsed config differs only in gamma/arm; src/scripts Python and sbatch bytes
verified identical to A5. Config SHA256
a6e8bf555f7060dacf2eada9716f7dc71b5aafd407159a950375b7e2c0df3f49.
Submitted fixed fold0 screen847_0, full50 epochs, same split and seed42.
Do not resubmit. Confirmation requires completed screen audit and >=.75.
Report vindr_a12_gamma1_preregistration_20260920.md. Goal not achieved.

A12 first10 epochs: job847_0 verified RUNNING on master, startup RTX5090;
W&B fax28rks. Best epoch5 Macro-F1 .5487076648841355,
accuracy .8341584158415841, QWK .6663873003352396, class F1
[0,.6909090909090909,.8921568627450981,.611764705882353], zero severe.
All recorded scalar losses finite. Screen not yet qualified; continue
unchanged through50. Next result update20. No confirmation submitted.

A12 first20: best epoch17 Macro-F1 .6951398373858266, accuracy
.8168316831683168, QWK .6206928926861328, class F1
[.6666666666666666,.5925925925925926,.8826446280991735,.6386554621848739].
Confusion [[1,0,0,0],[1,24,15,0],[0,15,267,29],[0,2,12,38]], two severe
D->B errors. A5 first20 selected Macro-F1 .7654421854687274 (epoch20),
class F1 [1,.6086956521739131,.8637873754152824,.5892857142857143].
A12 has higher C/D but lower A/B at these selected checkpoints; no overall
screening pass yet. Job847_0 RUNNING on master, all scalar losses finite.
Continue unchanged through50, next result checkpoint30. No expansion.

A12 first30: best epoch27 Macro-F1 .7946366892484166, accuracy
.844059405940594, QWK .6576823757262751, class F1
[1,.6593406593406593,.9001584786053882,.6190476190476191], zero severe.
Confusion [[1,0,0,0],[0,30,10,0],[0,21,284,6],[0,0,26,26]].
Job847_0 RUNNING on master, all recorded scalar losses finite.
Provisional fold0 DEV exceeds .75 but is not completed-screen audit or CV5
success. Finish50 before confirmation; next result update40. No expansion.

A12 first40: selected checkpoint remains epoch27 Macro-F1
.7946366892484166, unchanged from first30. Job847_0 verified RUNNING
on master; all recorded scalar losses finite. Finish50 and audit before
any confirmation expansion. Next result update at screen completion.

A12 completed50 screen audit PASS; job847_0 COMPLETED ExitCode0:0,
no restart/requeue. Selected epoch27 Macro-F1 .7946366892484166;
only2 epochs >=.75, final .5973763269497734. A unchanged versus A5fold0,
B/C improve and D decreases. No stability or CV5 success claim.
Reports vindr_a12_gamma1_screen_20260920.{json,md}.
Immutable config hash rechecked matching preregistration. Submitted array848
fresh folds1--4 only, retaining847fold0. Do not resubmit. Same seed/split,
50 epochs, RTX5090 assertion, worker2 excluded. Next metrics at common10.

A12 confirmation startup verified: all848_1--4 RUNNING; folds1/2 master,
folds3/4 worker1. Each startup log explicitly reports NVIDIA GeForce RTX5090.
W&B fold1 o23kdllx, fold2 in4e70uo, fold3 1i85kqaz, fold4 kmmw9n97.
Initial snapshot has no completed epochs yet; no finite-loss claim until
nonempty histories are available. Retain847fold0; no duplicate submissions.

A12 common first10 snapshot: array848 all RUNNING, scalar losses finite.
Selected first10 fold0--4 Macro-F1 [.5487076648841355,.5753719449613244,
.5890315753846532,.5507577843731195,.5390319168086487]; mean
.5605801772823763, sample SD .020796886351062457. A5 same horizon
mean .6052666352654212. Fold1 A F1=0, B/C/D [.7848101265822784,
.9040650406504065,.6126126126126126]. Fold2 A F1=.3333 with4 B->A
false positives; D F1=.493827. No early rejection or success claim.
Continue registered50 unchanged; next metrics common20. Detailed snapshot
vindr_a12_gamma1_first10_20260920.json includes matched-horizon A5.

A12 common first20: array848 all RUNNING, all recorded scalar losses finite.
Selected fold scores [.6951398373858266,.5753719449613244,.5890315753846532,
.5507577843731195,.5390319168086487]; mean .5898666117827145, SD
.062062289829236755; accuracy .8279623123602683, QWK .6470162208112356.
Class means [.2,.6797783067959856,.8904267463378341,.5892613939970383].
A5 same20 mean .6749582268293596, class means [.5333333333333333,
.6597280956786045,.8905405302035468,.6162309481019537].
A12 B improves, C nearly unchanged, D/A worse at selected checkpoints.
Confirmation folds1--4 selected scores unchanged since first10; finish50
unchanged. Next metrics common30. Detailed first20 JSON saved; no success claim.

A12 common first30: array848 all RUNNING, scalar losses finite.
Selected fold scores [.7946366892484166,.5753719449613244,.5923266149870801,
.5507577843731195,.5896881993483378]; mean .6205562465836557,
sample SD .0987005514151425, accuracy .8274525219271307, QWK
.6387067545748017. Class means [.36,.6605791390548016,.8913534452699232,
.570292402009898]. A5 same horizon mean .7028282800839902.
All four class means below A5: deficit is not solely rare A. Selected
fold2/4 each have3 B->A false positives and29 D->C errors. Continue50
unchanged; next common40. Exact matched-horizon JSON saved as first30.

A12 common first40: array848 all RUNNING, recorded scalar losses finite.
Selected fold scores [.7946366892484166,.5753719449613244,.5955795592068516,
.5521248178727538,.5896881993483378]; mean .6214802421275368,
SD .09823553898728177, accuracy .8363781539444267, QWK .6381084466002989.
Class means [.36,.6605213336551757,.8985955965112578,.5668040383437138].
A5 same40 mean .7028282800839902. C mean now slightly higher than A5,
but A/B/D lower. Continue registered50 unchanged; next report completion
and fullCV5 audit. Exact first40 matched-horizon JSON saved.

A12 completed50 fullCV5 audit PASS. All848 jobs COMPLETED ExitCode0:0,
no restarts/requeue, allowed nodes; all scalar losses finite. Mean .6214802421275368,
SD .09823553898728177; BCD .7086403228367157. Reject versus A5 .7028282800839902.
C slightly better, A/B/D lower; retain A5 parent. Reports
vindr_auggeo_dropout30_gamma1_cv5_results_20260920.{json,md}. No new job submitted.
Published summary nwuuq6k9; independently verified finished, exact aggregate
scalars, source IDs, 2017 cases, false independent-test/multi-seed flags,
fold table and cv5-audit artifact. Goal remains unmet.

Post-A12 read-only ordinal diagnostic: fixed checkpoint threshold spacing
imposes approximate FIT-weighted minimum summed BCE .54718 (A5epoch30)
and .56438 (A12epoch27), close to recorded .55701/.57742. No loss-target
bug identified; scalar magnitude does not establish gradient dominance.
Report vindr_ordinal_bias_diagnostic_20260920.md. Candidate next factor:
ordinal-bias LR only on A5, pending tests/preregistration. No job submitted.

Implemented opt-in ordinal_bias_lr_multiplier in isolated optim.py and
engine builder. Default1 preserves single-group legacy AdamW exactly.
Three CPU unit tests PASS in cluster paper_1 environment (local Python lacks
torch): exact default updates, unique parameter coverage/bias-only LR10x,
unchanged weight_decay, cosine ratio and invalid multiplier rejection.
Test staging /slurmshared/Ngoc/optim-test-BnEonC. No training submitted yet;
A13 config, preregistration and immutable A5-based deployment still required.
Note LR scaling also scales AdamW bias decay per update; no claim that
threshold spacing alone causes the generalization deficit.

A13 preregistered: A5 ordinal_bias LR multiplier10 only; new immutable
deployment /slurmshared/Ngoc/code/hcmus-density-auggeo-dropout30-ordlr10-20260920-v1.
Config SHA256 4679acb7f2ffba6b755a7e8f067978e334460efc78d51372bf06abcbac2f9d6b.
Parsed config delta and existing src/scripts bytes checked against A5;
only engine optimizer construction changes plus new optim.py. Real DensityModel
optimizer integration PASS. Submitted fixed fold0 screen852_0, full50.
Do not resubmit. No confirmation until completed screen audit >=.75.
Preregistration vindr_a13_ordlr10_preregistration_20260920.md.

A13 startup verified RTX5090 master, W&B zk46dx49. First10 completed;
job852_0 RUNNING, scalar losses finite. Best epoch10 Macro-F1 .58654084800213,
accuracy .7252475247524752, QWK .5569825337864538, classes
[.5,.4423076923076923,.8084358523725835,.5954198473282443], zero severe.
A5 first10 selected .5452488631717199 with A0 and higher B/C/D.
A13 ordinal train loss epoch10 .340564 versus A5 .874890: optimization
change reduces this loss but does not yet establish generalization gain.
Screen below gate; continue full50 unchanged, next metrics20. No expansion.
Exact paired first10 report saved.

A13 first20: job852_0 verified RUNNING on master, all scalar losses finite.
Selected epoch20 Macro-F1 .7580533506398416, accuracy .7970297029702971,
QWK .5906446690825864, classes [1,.5656565656565656,.8665568369028006,.6].
One severe D->B error. A5 matched first20 .7654421854687274, QWK .6126648582920213.
Ordinal train loss reduced .652431->.113145 but no generalization gain established.
Provisional screen threshold crossed; continue full50 and audit before expansion.
No confirmation submitted. First20 report saved; next metrics30.

A13 first30: job852_0 RUNNING on master; all recorded scalar train losses finite.
Selected epoch20 unchanged, Macro-F1 .7580533506398416, QWK .5906446690825864.
A5 matched first30 selects epoch30, Macro-F1 .7896498561536562, QWK .6486083499005965.
A13 lower on each B/C/D F1, accuracy and QWK; no generalization gain established.
Continue full50 unchanged, audit before expansion; no confirmation submitted.
Exact first30 comparison saved; next metrics40.

A13 first40: job852_0 RUNNING on master; all recorded scalar train losses finite.
Selected epoch20 unchanged: Macro-F1 .7580533506398416, QWK .5906446690825864.
A5 matched first40 .7896498561536562, QWK .6486083499005965; A13 still below
A5 on B/C/D, accuracy and QWK. First40 report saved. Continue full50 unchanged;
next report completion plus screen audit. No confirmation submitted.

A13 completed50: job852_0 COMPLETED ExitCode0:0, no restarts/requeue;
master, worker2 excluded. Screen audit PASS including live W&B finished.
Selected epoch20 .7580533506398416, QWK .5906446690825864, only1 epoch>=.75;
epoch50 .5358465566354522 with A0. Total AMP skipped updates17.
Gate passed numerically, no evidence of stability or improvement over A5.
Exact screen JSON/MD saved. No confirmation submitted during audit.
User-approved stability requirements: mean>=.70, sample SD<=.05,
minimum fold>=.65, seed42 only; A5 does not satisfy these jointly.

A13 confirmation submitted as array860 folds1--4 only, fresh ImageNet,
unchanged deployed config SHA4679acb7f2ffba6b755a7e8f067978e334460efc78d51372bf06abcbac2f9d6b.
Retain screened852-fold0; no rerun0 or ensemble. Completed screen passed .75
and audit; confirmation measures actual dispersion, not presumed improvement.
RTX5090 startup assertion, worker2 excluded, no-requeue, full50 retained.
Unrelated rankoff jobs853--855 were not modified. Next verify startup/W&B.
Acceptance follows revised_goal_seed42_20260920.md: mean>=.70, SD<=.05,
minimum fold>=.65, seed42; supersedes old multi-seed preregistration goal text.

Array860 startup verified: all four tasks RUNNING; folds1/2 master,
folds3/4 worker1. Each log explicitly reports NVIDIA GeForce RTX5090.
W&B metadata IDs: fold1 o5r423ax, fold2 aryla87q, fold3 ozldszzr,
fold4 jv4hxhef. No completed epochs at this startup snapshot, so no
training-loss health inference yet. Next quantitative report common first10.

A13 common first10: all860 tasks RUNNING, scalar train losses finite.
All five folds restricted to first10 (including completed852-fold0).
Mean .5566859963242436, sample SD .020331683596175643,
minimum .5386815624752397, accuracy .8210512738618775, QWK .6369314255306814.
Class means [.1,.6442677839990981,.8833496937251732,.599126507572703].
A5 matched first10 mean .6052666352654212, SD .10996283311285104,
minimum .5325666937276081. All A13 class means below A5; small dispersion
reflects similarly low performance, not successful stability improvement.
Neither mean nor minimum meets acceptance. Full50 unchanged; next common20.
Exact paired fold metrics saved in vindr_a13_ordlr10_cv5_first10_20260920.json.

A13 common first20: all860 tasks RUNNING, recorded scalar losses finite.
All folds restricted to first20, including completed852-fold0. Mean
.5943567169497129, sample SD .09196868576542751, minimum .5452580875800117,
accuracy .8294523745178488, QWK .6283648236232485. Class means
[.26666666666666666,.6649559588733195,.892992402256296,.5528118400025697].
A5 matched mean .6749582268293596, SD .10480808249500159, min .5701863354037267.
A13 B/C slightly higher on average, A/D lower; all three acceptance thresholds
unmet. Fold4 selected20 has4 B->A false positives and36 D->C errors.
Continue registered50 unchanged, next common30. Exact paired first20 JSON saved.

A13 common first30: all860 tasks RUNNING, scalar train losses finite.
All folds limited to first30. Mean .6052924479438352, SD .08610544880238348,
minimum .5549891535588053, accuracy .8225044836989902, QWK .6322178959827968.
Class means [.3238095238095238,.6189613729107273,.8896669360349794,.5887319590201103].
A5 matched mean .7028282800839902, SD .1172888127211152, min .5701863354037267.
All A13 class means below A5; smaller SD does not meet joint acceptance.
Fold2 selected23 recognizes A but has5 B->A false positives; fold1/3 selected A0.
Continue full50 unchanged, next common40. Exact paired first30 JSON saved.

A13 common first40: all860 tasks RUNNING, recorded scalar train losses finite.
All folds limited to first40. Mean .6083934605957435, SD .08403430838315352,
minimum .5632771274097002, accuracy .8319337640960126, QWK .6395174220721775.
Class means [.31666666666666665,.6267935407428951,.8963272367566016,.5937863982168106].
A5 matched mean .7028282800839902, SD .1172888127211152, min .5701863354037267.
C slightly higher, A/B/D lower; all joint acceptance thresholds still unmet.
Fold2 selected36 has6 B->A false positives and31 D->C errors.
Continue registered50 unchanged; next completion plus CV5 audit.
Exact paired first40 JSON saved. No new experiment submitted.

A13 full50 completed: 860_1--4 COMPLETED ExitCode0:0, Restarts0/Requeue0,
master/worker1, worker2 excluded, scalar train losses finite. CV5 audit including
live W&B PASS, 2017 unique cases, retained852-fold0. Selected metrics unchanged
from first40: mean .6083934605957435, sample SD .08403430838315352,
minimum .5632771274097002; accuracy .8319337640960126, QWK .6395174220721775.
Epoch50 mean .5245928851595144. All joint criteria fail. Reject A13, keep A5
as comparison baseline; reduced dispersion here is not successful stabilization.
Exact JSON/MD: vindr_auggeo_dropout30_ordlr10_cv5_results_20260920.

A13 summary5lipxk3w published and independently API-verified finished,
aggregates/source IDs/2017 cases/false independent-test and multi-seed flags,
fold table and audit artifact present.

A14 registered: A5 plus letterbox resize only, arm auggeo_dropout30_letterbox.
Immutable snapshot hcmus-density-auggeo-dropout30-letterbox-20260920-v1;
all src/scripts Python bytes identical to A5. Config SHA256
6645098ae30b7649d9c4d5f642bec9a6788adc0c36c8245ef31af0207229b19d.
Preflight PASS: config differs only resize/arm, all five frozen manifests
validated, synthetic letterbox geometry and real FIT tensor shape/finite PASS.
Submitted fixed fold0 screen job878, full50 freshImageNet seed42; no other
folds submitted. Preregistration vindr_a14_letterbox_preregistration_20260920.md.

A14 startup verified RUNNING on master; log reports NVIDIA GeForce RTX5090.
W&B source p5m57omo, https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/p5m57omo.
Keep registered50 unchanged; no additional folds before completed screen audit.

A14 first10: job878_0 RUNNING, all scalar train losses finite. Selected epoch10
Macro .5588157368155812, accuracy .7896039603960396, QWK .6110809096674821,
classes [.2857142857,.4556962025,.8688524590,.625]. Matched A5 first10 best
.5452488631717199 at epoch7, accuracy .8217821782178217, QWK .6538131962296487.
A14's small Macro advantage is entirely sensitive to the single fold0 A case;
B/C/D, accuracy and QWK are lower. Both have7 AMP-skipped updates through10.
No conclusion or expansion; continue registered50, next report20.

A14 first20: job878_0 RUNNING, finite scalar train losses. Selected remains
epoch10 Macro .5588157368155812, accuracy .7896039603960396, QWK
.6110809096674821; epoch20 Macro .5021215677905819. Matched A5 first20 best
epoch20 Macro .7654421854687274, accuracy .7970297029702971, QWK
.6126648582920213. Both have11 AMP-skipped updates. A14 trails by .20663 and
has not met gate; continue registered50, no confirmation submitted, next30.

A14 first30: job878_0 RUNNING, finite scalar train losses. Selected remains
epoch10 Macro .5588157368155812, accuracy .7896039603960396, QWK
.6110809096674821; epoch30 Macro .49964733931424354. Matched A5 first30 best
epoch30 Macro .7896498561536562, accuracy .8267326732673267, QWK
.6486083499005965. A14/A5 AMP skips14/12. A14 trails .23083 and remains
below gate; continue registered50, no confirmation submitted, next40.

A14 first40: job878_0 RUNNING, finite scalar train losses. Selected remains
epoch10 Macro .5588157368155812, accuracy .7896039603960396, QWK
.6110809096674821; epoch40 Macro .5161113080863919. Matched A5 first40 best
epoch30 Macro .7896498561536562, accuracy .8267326732673267, QWK
.6486083499005965. A14/A5 AMP skips16/14. A14 trails .23083 and remains
below gate; continue to completed50/audit, no confirmation submitted.

A14 completed50 and screen audit PASS including live W&B finished. Selected
epoch10 Macro .5588157368155812, accuracy .7896039603960396, QWK
.6110809096674821, classes [.2857142857,.4556962025,.8688524590,.625].
Epoch50 Macro .5171638803336838; 0/50 epochs >=.75; AMP skips18. Reject A14:
it fails expansion gate and is substantially worse than A5 fold0 .7896498562.
No folds1--4 submitted. Exact report vindr_a14_letterbox_screen_20260920.

A15 registered: A5 plus freeze DenseNet features/BN epochs1--5, unfreeze at6;
arm auggeo_dropout30_warmup5. Immutable snapshot
hcmus-density-auggeo-dropout30-warmup5-20260920-v1; all src/scripts Python
bytes identical to A5. Config SHA256
02568df47a77d934bb8e74b48bde3b53d545e945d1fb66d8cc74794554e046bd.
Preflight PASS: only warmup/arm differs, all frozen manifests, real FIT tensor,
and freeze-at5/unfreeze-at6 state transition validated. Submitted fixed fold0
screen job905 only, full50 freshImageNet seed42; no other folds. Startup RUNNING
on master and log explicitly NVIDIA GeForce RTX5090; worker2/Vesta excluded.
Preregistration vindr_a15_warmup5_preregistration_20260920.md.
W&B source cjdw2zo6:
https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/cjdw2zo6.

A15 first10: job905_0 RUNNING, finite scalar train losses; epochs1--5 frozen
and6--10 unfrozen exactly. Selected epoch6 Macro .5668603551539351, accuracy
.849009900990099, QWK .6907439012147375, classes
[0,.6451612903,.9022801303,.72], severe0. Matched A5 first10 .5452488631717199;
A15 improves B/C/D, accuracy and QWK but both have A0. AMP skips6 vs7.
Below gate; continue registered50, no confirmation, next20.

A15 first20: job905_0 RUNNING, finite scalar train losses; epochs1--5 frozen
and6--20 unfrozen exactly. Selected epoch17 Macro .6286564490092774, accuracy
.8366336633663366, QWK .6659156279961649, classes
[.3333333333,.6315789474,.8985507246,.6511627907], severe1. Matched A5
first20 selected epoch20 Macro .7654421854687274, accuracy .7970297029702971,
QWK .6126648582920213. A15 is better on accuracy/QWK/B/C/D, but trails Macro
by .1367857365 because A5 correctly predicts the single fold0 A case. AMP
skips10 vs11. Below gate; continue registered50, no confirmation, next30.

A15 first30: job905_0 RUNNING, finite scalar train losses; epochs1--5 frozen
and6--30 unfrozen exactly. Selected epoch26 Macro .7145881415028787, accuracy
.8539603960396039, QWK .6663867428059568, classes
[.6666666667,.6301369863,.909375,.6521739130], severe0. Matched A5 first30
selected epoch30 Macro .7896498561536562, accuracy .8267326732673267, QWK
.6486083499005965. A15 improves accuracy/QWK/C/D but trails Macro by
.0750617147, primarily because of the single fold0 A case, with slightly lower
B too. Both have12 AMP skips. A15 exceeds .70 but not the .75 expansion gate;
continue registered50, no confirmation, next40.

A15 first40: job905_0 RUNNING, finite scalar train losses; epochs1--5 frozen
and6--40 unfrozen exactly. Selected remains epoch26 Macro .7145881415028787,
accuracy .8539603960396039, QWK .6663867428059568, classes
[.6666666667,.6301369863,.909375,.6521739130], severe0. Matched A5 first40
still epoch30 Macro .7896498561536562, accuracy .8267326732673267, QWK
.6486083499005965. A15 remains better on accuracy/QWK/C/D but trails Macro by
.0750617147; AMP skips15 vs14. Below .75 gate; continue to completed50 screen
audit, no confirmation folds submitted.

A15 completed50 and screen audit PASS including job completion, checkpoint,
predictions, frozen manifests, live W&B finished, and the registered freeze
transition. Selected remains epoch26 Macro .7145881415028787, accuracy
.8539603960396039, QWK .6663867428059568, classes
[.6666666667,.6301369863,.909375,.6521739130], severe0. Epoch50 Macro
.5404630542519797; 0/50 epochs >=.75; AMP skips15. Reject A15: it fails the
expansion gate. No folds1--4 submitted. Exact JSON/MD:
vindr_a15_warmup5_screen_20260920.

A16 registered: A5 plus a 0.1x DenseNet-features LR only; fusion and heads
retain the 5e-5 base LR. This tests continuous discriminative fine-tuning after
A15's hard freeze/unfreeze failed its gate. Immutable snapshot
hcmus-density-auggeo-dropout30-backbonelr01-20260920-v1; config SHA256
443a5e9128022c8de60960ef948c0094b50dea492e7f57f5af8c831a156b4d06.
Cluster suite 22/22 PASS. Preflight PASS: parsed config differs from A5 only
in arm/backbone multiplier, all five manifests validate, real FIT tensor is
finite `[4,3,512,512]`, and optimizer groups cover every parameter exactly
once: all362 backbone parameters at5e-6 and20 non-backbone at5e-5. Fixed fold0
full50 freshImageNet seed42 only; no confirmation before audited .75 gate.
Preregistration vindr_a16_backbonelr01_preregistration_20260920.md.

A16 submitted as fixed fold0 job906 only. Startup verified RUNNING on
slurm-b20a-master-0 with `NVIDIA GeForce RTX 5090`; worker2/Vesta is excluded
and no-requeue remains active. Output
`/slurmshared/Ngoc/runs/hcmus-density-cv5-v1-906-fold0`. W&B source en6zi94h:
https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/en6zi94h.
Keep the registered full50 unchanged; first comparison at epoch10.

A16 first10: job906_0 RUNNING, finite scalar train losses, backbone trainable
throughout. Selected epoch4 Macro .5522557246650255, accuracy
.8292079207920792, QWK .666555023923445, classes
[0,.6315789474,.8877887789,.6896551724], severe0. Matched A5 first10 selected
.5452488631717199; A16 is only +.0070068615. Both have7 AMP skips. A16 epoch10
drops to .48390220442083576 with11 severe errors and35 false-A predictions,
so monitor instability without changing the registered run. Below gate;
continue full50, no confirmation, next20.

A16 first20: job906_0 RUNNING, finite scalar train losses, backbone trainable
throughout. Selected epoch20 Macro .6647013473177328, accuracy
.8292079207920792, QWK .6636583011583012, classes
[.5,.6206896552,.8910569106,.6470588235], severe0. Matched A5 first20 Macro
.7654421854687274, accuracy .7970297029702971, QWK .6126648582920213. A16
improves B/C/D separately (descriptive mean .7196017964 vs .6872562473),
accuracy and QWK, but trails four-class Macro by .1007408382 because the
single fold0 A yields F1 .5 vs1. Both have11 AMP skips. Below .75 gate;
continue full50, no confirmation, next30.

A16 first30: job906_0 RUNNING, finite scalar train losses, backbone trainable
throughout. Selected remains epoch20 Macro .6647013473177328, accuracy
.8292079207920792, QWK .6636583011583012, classes
[.5,.6206896552,.8910569106,.6470588235], severe0. Matched A5 first30 selected
epoch30 Macro .7896498561536562. A16 trails by .1249485088, while selected
B/C/D means are effectively identical (.7196017964 vs .7195331415). AMP skips
14 vs12. Below .75 gate; continue full50, no confirmation, next40.

A16 first40: job906_0 RUNNING, finite scalar train losses, backbone trainable
throughout. Selected remains epoch20 Macro .6647013473177328, accuracy
.8292079207920792, QWK .6636583011583012, classes
[.5,.6206896552,.8910569106,.6470588235], severe0; epoch40 Macro
.5651880272841501. Matched A5 first40 remains .7896498561536562. A16 trails
by .1249485088; AMP skips17 vs14. Below .75 gate; continue to completed50
screen audit, no confirmation folds submitted.

A16 completed50 and screen audit PASS including job completion, checkpoint,
predictions, frozen manifests and live W&B finished. Selected remains epoch20
Macro .6647013473177328, accuracy .8292079207920792, QWK
.6636583011583012, classes [.5,.6206896552,.8910569106,.6470588235],
severe0. Epoch50 Macro .5668188358910276; 0/50 epochs >=.75; AMP skips20.
Reject A16: it fails the expansion gate and trails A5 fold0 by .1249485088.
No folds1--4 submitted. Exact JSON/MD:
vindr_a16_backbonelr01_screen_20260920.

A17 preregistered: A5 plus weighted case sampling power .10 only. This is a
smaller interpolation than A6 power .25, which reduced CV5 SD from .11729 to
.06445 but reduced mean from .70283 to .67655. A17 tests whether weaker
sampling pressure can preserve more mean while improving stability. Fixed
fold0 full50 fresh ImageNet seed42; .75 audited expansion gate; no ensemble,
resplit or independent-test claim. RTX5090 only, worker2/Vesta excluded.
Deployment target hcmus-density-auggeo-dropout30-sampling010-20260920-v1;
config SHA256 2740940652db1870ac9aa5570916561b163ceb6ab7bedd6d9e4870f7e5a688dd.
Cluster preflight PASS: 22/22 tests, all five frozen manifests, exact A5 config
delta, finite real FIT tensor `[4,3,512,512]`, and sampler construction over
1613 fold0 FIT cases validated.

A17 submitted as fixed fold0 job907 only. Startup verified RUNNING on
slurm-b20a-master-0 with NVIDIA GeForce RTX5090; worker2/Vesta excluded and
no-requeue active. Output hcmus-density-cv5-v1-907-fold0. W&B djz4e32c:
https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/djz4e32c.
Keep registered full50 unchanged; first comparison at epoch10.

A17 first10: job907_0 RUNNING, finite scalar train losses. Selected epoch8
Macro .7556740297265725, accuracy .7797029702970297, QWK
.5971948377845492, classes [1,.6464646465,.8499156830,.5263157895], severe0.
It provisionally crosses the .75 screen threshold but trails A6 first10
.7829792575. More importantly, A17's selected B/C/D mean is .6742320396 versus
A5 .7269984842, while the single fold0 A supplies F1=1. Aggregate sampled
counts are [95,1876,11853,2306]; AMP skips7, matching A5/A6. Do not expand on
this fragile early checkpoint; continue registered50 unchanged, next report20.

A17 first20: job907_0 RUNNING, finite scalar train losses. Selected improves
to epoch17 Macro .7914694342156339, accuracy .8267326732673267, QWK
.6559945504087192, classes [1,.6285714286,.8856209150,.6516853933], severe0.
Five checkpoints through20 reach .75. B/C/D mean .7219592456 now slightly
exceeds A5's completed selected B/C/D mean .7195331415, while Macro is
.0018195781 above A5 fold0 .7896498562. Epoch20 itself falls to .5092051746,
so checkpoint variability remains large. AMP skips10; sampled aggregate
[175,3616,23775,4694]. Promising screen evidence only; continue full50 and do
not submit folds1--4 before completed audit, next report30.

A17 first30: job907_0 RUNNING, finite scalar train losses. Selected remains
epoch17 Macro .7914694342156339, accuracy .8267326732673267, QWK
.6559945504087192, classes [1,.6285714286,.8856209150,.6516853933], severe0.
Nine checkpoints through30 reach .75 versus A5 three and A6 one at the matched
horizon. Epoch30 itself is .5383710440 with A F1=0, so rare-A-driven
per-epoch movement remains large. B/C/D selected mean remains .7219592456.
AMP skips13; sampled aggregate [246,5401,35681,7062]. Continue registered50,
no confirmation yet, next report40.

A17 first40: job907_0 RUNNING, finite scalar train losses. Selected remains
epoch17 Macro .7914694342156339, accuracy .8267326732673267, QWK
.6559945504087192, classes [1,.6285714286,.8856209150,.6516853933], severe0.
Twelve checkpoints through40 reach .75 versus A5 five and A6 one at the
matched horizon. Epoch40 Macro .6788652025; AMP skips16; sampled aggregate
[326,7194,47530,9470]. Continue to completed50 audit, no confirmation yet.

A17 completed50 and screen audit PASS including job completion, checkpoint,
predictions, frozen manifests and live W&B finished. Selected remains epoch17
Macro .7914694342156339, accuracy .8267326732673267, QWK
.6559945504087192, classes [1,.6285714286,.8856209150,.6516853933], severe0.
Epoch50 Macro .5301002144; 12/50 checkpoints >=.75; AMP skips18. A17 exceeds
A5 fold0 by .0018195781 and passes the preregistered .75 expansion gate.
Retain completed job907 fold0 and launch fresh folds1--4 from the identical
snapshot. Exact JSON/MD: vindr_a17_sampling010_screen_20260920.

A17 confirmation submitted as array908 folds1--4 from the identical immutable
snapshot. All four tasks started RUNNING immediately: folds1/2 on master and
folds3/4 on worker1, each explicitly reporting NVIDIA GeForce RTX5090;
worker2/Vesta remains excluded, no-requeue active. Outputs are
hcmus-density-cv5-v1-908-fold{1,2,3,4}. Initial W&B sources: fold1 txm9bun2,
fold2 7jtlt2gq; folds3/4 are still completing W&B startup. Do not resubmit;
monitor all four to full50 and combine with retained job907 fold0.

A17 CV5 matched first10: all confirmation tasks RUNNING with finite scalar
losses. Selected fold Macro values [.7556740297,.5531327474,.5376961279,
.6468795307,.6112213946]; mean .6209207660, sample SD .0872466808, minimum
.5376961279, accuracy mean .8096356534, QWK mean .6245859213, class means
[.4363636364,.6173852317,.8805988408,.5493353553]. Only fold0 has crossed
.75, so the early result is below all final criteria and confirms the screen
is not CV evidence. Continue all registered50 unchanged; next report20. W&B
fold1 txm9bun2, fold2 7jtlt2gq, fold3 7uqvm3ct, fold4 fpbres7g.

A17 CV5 matched first20: all confirmation tasks active and finite. Selected
fold Macro values [.7914694342,.5531327474,.5376961279,.6468795307,
.6759116090]; mean .6410178898, sample SD .1028187513, minimum .5376961279,
accuracy mean .8120937032, QWK mean .6454029273, class means
[.4696969697,.6074907987,.8801560137,.6067277772], and B/C/D mean
.6981248632. Mean rises .0200971238 from first10 but SD worsens .0155720705.
Only fold0 has crossed .75; folds1--4 have not. Continue all registered50
unchanged; next report30. Exact report:
vindr_a17_sampling010_cv5_first20_20260920.md.

A17 CV5 matched first30: selected fold values and all aggregate metrics remain
unchanged from first20: mean .6410178898, sample SD .1028187513, minimum
.5376961279, accuracy .8120937032 and QWK .6454029273. No fold found a new
best checkpoint in epochs21--30. Fold0 has nine checkpoints >=.75, while
folds1--4 still have none. Continue all registered50 unchanged; next report40.
Exact report: vindr_a17_sampling010_cv5_first30_20260920.md.

A18 infrastructure prepared while A17 continues: optional
`training.freeze_backbone_batchnorm` keeps DenseNet BatchNorm running
statistics fixed while convolution and BatchNorm affine parameters remain
trainable. The default is false and preserves all existing arms. Remote test
environment with campaign dependencies passes 23/23 unit tests. Do not
register or launch A18 until A17 completes and its audit determines the next
single-factor experiment.

A5 BatchNorm diagnostic: all 121 DenseNet BN layers show material selected-
checkpoint drift from ImageNet initialization. Mean standardized running-mean
drift by fold is [.227054,.177374,.148428,.126159,.228714], while mean
absolute log running-variance ratios are [.418065,.356957,.346639,.317155,
.396144]. The amount partly tracks selected epoch, so this is motivation, not
causal proof. Exact report: vindr_a5_batchnorm_drift_diagnostic_20260920.md.

A18 candidate config prepared but not registered or launched:
`vindr_density_auggeo_dropout30_bnfreeze.yaml`, SHA256
2f00484753e48424da6ca53a78149d9c35dcb5bb3a824af0b639154a59d4c6a1.
Textual comparison to A5 changes only arm metadata and enables
`training.freeze_backbone_batchnorm`; remote campaign environment again
passes 23/23 tests, including all 121 DenseNet BN modules fixed in eval mode
while convolution weights still update. Wait for completed A17 audit.

Sampling/loss interaction diagnostic: with fold0 FIT counts [5,156,1245,207],
the normalized static focal class pressure A/B/C/D is
[.2030,.2187,.3541,.2242] for A5, [.2833,.2164,.2847,.2156] for A17, and
[.4291,.1956,.1885,.1868] for A6. Thus A6's .25 sampling and beta .999
double-compensate A, consistent with its better rare-class stability but lower
mean in every class. Using A6 as parent and changing beta only to .995 would
yield [.2644,.1592,.4110,.1654] while keeping its higher A draw exposure.
This is a candidate rationale, not a registered arm or causal conclusion.
Exact report: vindr_sampling_weight_interaction_diagnostic_20260920.md.

A17 CV5 matched first40: selected checkpoints and aggregate metrics remain
unchanged from first20/30. Fold values [.7914694342,.5531327474,.5376961279,
.6468795307,.6759116090] give mean .6410178898, sample SD .1028187513 and
minimum .5376961279; mean accuracy .8120937032, QWK .6454029273, class means
[.4696969697,.6074907987,.8801560137,.6067277772]. Fold0 has twelve epochs
>=.75, folds1--4 zero. Continue unchanged to completed50 audit. Exact report:
vindr_a17_sampling010_cv5_first40_20260920.md.

A17 completed CV5 audit PASS. Array908 folds1--4 all COMPLETED ExitCode0:0;
folds1/2 used master, folds3/4 worker1, with worker2/Vesta excluded. All five
histories have exactly50 epochs; common config/architecture, frozen split
hash/manifests, selected checkpoints, predictions, 2017-case union and live
finished W&B sources pass. Fold Macro values [.7914694342,.5531327474,
.5376961279,.6468795307,.6759116090], mean .6410178898, sample SD
.1028187513, minimum .5376961279, accuracy .8120937032, QWK .6454029273,
class means [.4696969697,.6074907987,.8801560137,.6067277772]. Reject A17:
mean is .0618103903 below A5 and every mean class F1 is lower; it fails mean,
SD and minimum-fold criteria. Retain A5 as best completed mean. Exact JSON/MD:
vindr_a17_sampling010_cv5_results_20260920.

A17 audited W&B summary `x1z8npaa` published and independently read back as
finished with exact mean .641017889812455, SD .10281875126033156, audit true,
independent-test false and target false:
https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/x1z8npaa.

A18 formally preregistered after completed A17 rejection: return to A5 and
change only DenseNet BatchNorm running-statistics policy. All 121 backbone BN
modules remain in eval mode while convolutions and BN affine parameters keep
gradients. Architecture, single flat-head inference, data, split, seed42 and
all other A5 settings remain fixed. Run only fresh fold0 full50 first and
expand only after completed audit with selected four-class Macro-F1 >=.75.
RTX5090 only; worker2/Vesta excluded; no ensemble. Exact preregistration:
vindr_a18_bnfreeze_preregistration_20260920.md.

A18 deployed to
`/slurmshared/Ngoc/code/hcmus-density-auggeo-dropout30-bnfreeze-20260920-v1`.
Config SHA256 2f00484753e48424da6ca53a78149d9c35dcb5bb3a824af0b639154a59d4c6a1.
Preflight PASS: 23 tests, exact A5 config behavior delta, frozen assignment
SHA, real finite `[4,3,512,512]` FIT tensor, natural sampling, all 121 BN
modules fixed with backbone gradients retained, and RTX5090/exclusion guards.
Submitted fixed fold0 only as job932. Verified RUNNING on master RTX5090,
Requeue0/Restarts0, worker2 excluded. W&B `zdit2tcj`:
https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/zdit2tcj.

A18 failed before epoch1: job932 FAILED NonZeroExitCode1 after22s with
non-finite loss. Three deterministic no-W&B GPU reproductions isolate the
failure to batch150. Inputs and every parameter are finite; AMP head outputs
and all losses become NaN, while an immediate FP32 retry of the same model and
input is finite (loss1.7531044483). Reject A18 under the fixed A5 AMP contract;
do not launch folds1--4. Disabling AMP would add a confounded second treatment
and is not substituted. Temporary diagnostic code removed. Exact report:
vindr_a18_bnfreeze_failure_20260920.md.

A19 preregistered: use completed A6 sampling-power .25 as parent and change
only class-weight beta .999->.995. Static fold0 focal pressure shifts from
[.4291,.1956,.1885,.1868] to [.2644,.1592,.4110,.1654], retaining increased
A draw exposure while reducing A double compensation and restoring C weight.
Architecture, A6 sampling, all other settings, seed42 and split remain fixed.
Run fold0 full50 first; expand only after audited selected Macro>=.75.
RTX5090 only, worker2/Vesta excluded, no ensemble. Exact preregistration:
vindr_a19_sampling025_beta995_preregistration_20260920.md.

A19 deployed from immutable A6 to
`/slurmshared/Ngoc/code/hcmus-density-auggeo-dropout30-sampling025-beta995-20260920-v1`.
Config SHA256 3eddbde358c9dd39cd974bd77e08d8e3f67b4a036d596480e842bee890038019.
Preflight PASS: 16/16 parent-snapshot tests, exact A6 semantic delta, frozen
split hash, real finite `[4,3,512,512]` tensor, expected sampling probabilities
and finite class/binary weights. Submitted fixed fold0 only as job936; verified
RUNNING on master RTX5090, Requeue0/Restarts0, worker2/Vesta excluded. W&B
`6wtyzm62`: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/6wtyzm62.
Epoch1 completed with finite scalar losses and expected sampled count sum1613;
continue unchanged to first report at epoch10.

A19 first10: job936 RUNNING with finite scalar losses. Selected epoch5 Macro
.7506524214, accuracy .7846534653, QWK .5914543426, classes
[1,.5473684211,.8552412646,.6], severe0; epoch10 Macro .6720768043. One of
ten checkpoints reaches .75. Matched A6 is .7829792575 and higher in every
B/C/D F1, accuracy and QWK; sampled totals and AMP skips are identical,
isolating beta as the treatment. Continue fold0 full50 unchanged; no
confirmation yet. Exact report: vindr_a19_sampling025_beta995_first10_20260920.md.

A19 first20: selected improves to epoch11 Macro .7623856925, accuracy
.7772277228, QWK .6014556296, classes [1,.6419753086,.8464163823,
.5611510791], severe0. Three checkpoints reach .75. Matched A6 remains
.7829792575 and A5 reaches .7654421855. A19 improves B versus A6 but lowers
C/D, especially D by .0993993796; it has not improved substantive parent
performance. Continue fold0 full50 unchanged; no confirmation. Exact report:
vindr_a19_sampling025_beta995_first20_20260920.md.

A19 first30: selected remains epoch11 Macro .7623856925, accuracy
.7772277228, QWK .6014556296 and classes [1,.6419753086,.8464163823,
.5611510791]. No improvement in epochs21--30; epoch30 Macro .5474753244.
Matched A5 is now .7896498562 and A6 .7829792575. A19 trails A5 by
.0272641636 and has lower C/D. Continue unchanged full50; no confirmation.
Exact report: vindr_a19_sampling025_beta995_first30_20260920.md.

A19 first40: selected still epoch11 Macro .7623856925, accuracy .7772277228,
QWK .6014556296, classes [1,.6419753086,.8464163823,.5611510791]. No new
best from epochs12--40; epoch40 Macro .5448053440. Matched A5 remains
.7896498562 and A6 .7829792575. Continue to completed50 screen audit; no
confirmation yet. Exact report: vindr_a19_sampling025_beta995_first40_20260920.md.

A19 completed50 fold0 screen audit PASS. Job936 COMPLETED ExitCode0:0 on
master RTX5090 with Requeue0/Restarts0 and worker2/Vesta excluded. Selected
remains epoch11 Macro .7623856925, accuracy .7772277228, QWK .6014556296,
classes [1,.6419753086,.8464163823,.5611510791], severe0; epoch50 Macro
.5481421172, three/50 checkpoints >=.75 and AMP skips16. The score trails A5
and A6 fold0 and B/C/D mean is only .6831809233, but it passes the
preregistered numeric expansion gate. Retain job936 fold0 and launch fresh
folds1--4 from the identical snapshot. Exact JSON/MD:
vindr_a19_sampling025_beta995_screen_20260920.

A19 folds1--4 confirmation launched as Slurm array job937 from the identical
immutable snapshot and config. Tasks 937_1--937_4 started RUNNING on
slurm-b20a-master-0 and slurm-b40a-worker-1; every task reports NVIDIA GeForce
RTX 5090, Requeue0/Restarts0, and explicitly excludes slurm-b40a-worker-2.
Fold0 remains the completed audited job936 and is not rerun. W&B run IDs:
fold1 3pg4lxtt, fold2 bt0zxehl, fold3 elnl4jhq, fold4 rbqwq3cv. Next planned
review is the common epoch10 milestone unless a task fails earlier.

A19 job937 common epoch10 milestone: all folds1--4 remain RUNNING without task
failure. Best-so-far Macro-F1 values are fold1 .5640520897 (epoch5), fold2
.6043886973 (epoch9), fold3 .5972447287 (epoch7), and fold4 .5301278061
(epoch4). Combined provisionally with completed fold0 .7623856925 gives mean
.6116398029, sample SD .0892929392 and min .5301278061. This is an incomplete
milestone, not final CV5 evidence; continue all tasks unchanged to full50.
Exact report: vindr_a19_sampling025_beta995_cv5_first10_20260920.{json,md}.

A19 job937 common epoch20 milestone: folds1--3 retain their first10 bests;
fold4 improves to .5587366168 at epoch20. The provisional vector including
completed fold0 is [.7623856925,.5640520897,.6043886973,.5972447287,
.5587366168], mean .6173615650, sample SD .0834921623, min .5587366168.
This remains incomplete evidence. Continue all tasks unchanged to full50.
Exact report: vindr_a19_sampling025_beta995_cv5_first20_20260920.{json,md}.

A19 job937 common epoch30 milestone: fold2 improves to .6815972921 at epoch25
and fold3 to .6458490326 at epoch24; fold1/fold4 retain .5640520897 and
.5587366168. With completed fold0, provisional mean is .6425241447, sample SD
.0852683552 and min .5587366168. This remains incomplete evidence. Continue
all tasks unchanged to full50. Exact report:
vindr_a19_sampling025_beta995_cv5_first30_20260920.{json,md}.

A19 job937 common epoch40 milestone: no fold improves its selected checkpoint
during epochs31--40. Provisional CV5 therefore remains mean .6425241447,
sample SD .0852683552, min .5587366168. Continue all tasks unchanged to the
required epoch50 completion and final audit. Exact report:
vindr_a19_sampling025_beta995_cv5_first40_20260920.{json,md}.

A19 final CV5 audit PASS. Job937 folds1--4 all completed50 with ExitCode0:0,
Requeue0/Restarts0 on RTX5090; W&B source runs are finished and match the
selected checkpoints. Final folds are [.7623856925,.5640520897,.6815972921,
.6458490326,.5587366168], mean .6425241447, sample SD .0852683552, min
.5587366168, accuracy mean .8245215340 and QWK mean .6165255554. A19 fails the
agreed mean>=.70, SD<=.05, min>=.65 criteria and trails direct parent A6
(.6765513839/.0644461991/.6194960833). Reject A19; beta .995 did not correct
the fold instability. Exact audited report:
vindr_a19_sampling025_beta995_cv5_results_20260920.{json,md}.

A19 audited CV5 summary published to W&B run cggh4pmr. API readback verifies
state finished, exact mean .6425241447489184, sample SD .08526835523350905,
accuracy mean .82452153403926, QWK mean .6165255554140378, audit_passed true,
independent_test false, the five expected source run IDs and the fixed split
digest. URL: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/cggh4pmr

A20 preregistered after A19 rejection: return to A5 and change only physical
case batch size 2->4. This tests whether larger per-update BatchNorm samples
reduce instability without the AMP failure seen when A18 fixed BN statistics.
No LR scaling or other treatment is allowed. Architecture, loss, natural
sampling, augmentation, seed42, split/cache and single-checkpoint inference
remain fixed. Require real RTX5090 batch4 update preflight, then fixed fold0
full50; expand folds1--4 only after completed audit reaches Macro-F1>=.75.
Preregistration: vindr_a20_batch4_preregistration_20260920.md.

A20 deployed from immutable A5 snapshot to
`/slurmshared/Ngoc/code/hcmus-density-auggeo-dropout30-batch4-20260920-v1`.
Config SHA256 `f2a09b877788aba027baa150f690f3c791348a7c3a37f30b87bd973c6c0d117f`;
semantic diff is exactly arm metadata plus batch_size 2->4. Remote suite 16/16
PASS and fixed assignment digest verified. Real RTX5090 preflight completed a
finite forward/backward/optimizer update for `[4,4,3,512,512]`, loss
1.3961549997, finite grad norm 10.6492013931 and peak allocated 5.3037 GiB.
Submitted fixed fold0 only as job943_0; verified RUNNING on master RTX5090,
Requeue0/Restarts0 with worker2/Vesta excluded. W&B run yamwkalh:
https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/yamwkalh
No result yet; monitor unchanged to the common epoch10 milestone.

A20 first10: job943_0 remains RUNNING on master RTX5090 with finite scalar
losses. Selected epoch7 Macro .7264230375, accuracy .8490099010, QWK
.6877344146, classes [.6666666667,.6896551724,.9035369775,.6458333333],
severe0; five AMP-skipped updates. This exceeds A5 matched first10 .5452488632
and improves B/C/D mean, accuracy and QWK, but remains below the .75 screen
gate. Epoch10 falls to .5325876408. Continue unchanged full50; next review20.
Exact report: vindr_a20_batch4_first10_20260920.md.

A20 first20: selected improves to epoch13 Macro .7733284878, accuracy
.8168316832, QWK .6123846074, classes [1,.6486486486,.8810289389,
.5636363636], severe0. One/20 checkpoints reaches .75. This is .0078863023
above A5 at the matched horizon and has higher B/C/D mean, but still depends
on fold0's single A case; epoch20 is .5217901889. Continue job943_0 unchanged
to full50 and audit before expansion. Exact report:
vindr_a20_batch4_first20_20260920.md.

A20 first30: selected remains epoch13 Macro .7733284878, accuracy .8168316832,
QWK .6123846074 and classes [1,.6486486486,.8810289389,.5636363636]. No
improvement in epochs21--30; epoch30 is .5108122411. A20 now trails A5 matched
first30/completed fold0 .7896498562 by .0163213684, and only one/30 checkpoint
reaches .75. Continue unchanged full50 and audit; no confirmation submitted.
Exact report: vindr_a20_batch4_first30_20260920.md.

A20 first40: selected remains epoch13 Macro .7733284878; no new best in
epochs14--40, epoch40 is .5093559012, and only one/40 checkpoint reaches .75.
It remains below A5 fold0 .7896498562. Continue unchanged through epoch50 and
complete the screen audit before any expansion. Exact report:
vindr_a20_batch4_first40_20260920.md.

A20 completed50 fold0 screen audit PASS. Job943_0 COMPLETED ExitCode0:0 in
00:47:45 on master RTX5090, Requeue0/Restarts0, worker2/Vesta excluded, and
W&B yamwkalh verified finished. Selected epoch13 Macro .7733284878, accuracy
.8168316832, QWK .6123846074, classes [1,.6486486486,.8810289389,
.5636363636], severe0; epoch50 .5384676299, one/50 checkpoints>=.75 and AMP
skips11. A20 trails A5/A6 fold0 and B/C/D mean is only .6977713171, but passes
the preregistered numeric expansion gate. Retain job943 fold0 and launch fresh
folds1--4 from the identical snapshot. Exact report:
vindr_a20_batch4_screen_20260920.{json,md}.

A20 confirmation folds1--4 launched as Slurm array944 from the identical
immutable snapshot/config. Tasks944_1--944_4 verified RUNNING on master and
worker1 RTX5090, Requeue0/Restarts0, with worker2/Vesta excluded. Fold0 remains
completed audited job943 and is not rerun. W&B runs: fold1 mplewjjl, fold2
p2jvocsh, fold3 65jauqmu, fold4 39rvupck. Monitor unchanged to common epoch10;
do not resubmit or alter the registered experiment.

A20 common epoch10: all job944 confirmation tasks remain RUNNING without
failure. Matched first10 fold values are [.7264230375,.5588510546,
.7722986814,.5553449026,.6557844283], mean .6537404209, sample SD
.0975047072, min .5553449026; A5 matched first10 is .6052666353/.1099628331/
.5325666937. Combining completed audited fold0 .7733284878 with incomplete
folds1--4 gives provisional mean .6631215109, SD .1079434927, min
.5553449026. Not final CV5 evidence; continue unchanged full50, next common20.
Exact report: vindr_a20_batch4_cv5_first10_20260920.md.

A20 common epoch20: selected fold vector [.7733284878,.5588510546,
.7722986814,.5778164946,.7491879335], mean .6862965304, sample SD
.1083241982, min .5588510546. A5 matched horizon is .6749582268/.1048080825/
.5701863354. A20 mean is +.0113383035 but SD is worse and minimum lower.
Folds1--4 remain incomplete; continue unchanged full50, next common30.
Exact report: vindr_a20_batch4_cv5_first20_20260920.md.

A20 common epoch30: selected vector [.7733284878,.5588510546,.7722986814,
.5778164946,.7685728925], mean .6901735222, sample SD .1114399429, min
.5588510546. A5 matched/completed is .7028282801/.1172888127/.5701863354.
A20 has slightly lower dispersion but lower mean and minimum. Continue all
tasks unchanged full50; next common40. Exact report:
vindr_a20_batch4_cv5_first30_20260920.md.

A20 common epoch40: no fold improves its selected checkpoint during
epochs31--40. Provisional mean remains .6901735222, sample SD .1114399429,
min .5588510546. Continue all tasks unchanged to required epoch50 and final
audit. Exact report: vindr_a20_batch4_cv5_first40_20260920.md.

A20 final CV5 audit PASS. Array944 folds1--4 all completed50 with ExitCode0:0,
Requeue0/Restarts0 on RTX5090; W&B sources are finished and exact. Final folds
[.7733284878,.5588510546,.7722986814,.5778164946,.7685728925], mean
.6901735222, sample SD .1114399429, min .5588510546, accuracy .8235007248,
QWK .6385918897. It fails mean>=.70, SD<=.05 and min>=.65. Relative to A5 it
loses .0126547579 mean, .0113352808 minimum and .0302063439 BCD mean while SD
improves only .0058488698. Reject A20; batch4 does not solve instability and
A5 remains the strongest completed mean-CV5 reference. Exact report:
vindr_a20_batch4_cv5_results_20260920.{json,md}.

A20 audited summary published to W&B run w9yalojh. Independent API readback
verifies finished state, exact mean .690173522169526, sample SD
.11143994288963992, accuracy .8235007247623025, QWK .6385918896626532,
audit_passed true, independent_test false, fixed digest and all five expected
source IDs. URL: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/w9yalojh

A21 preregistered after A20 rejection: return to A5 and multiply only the
primary flat-head focal term by2.0. This is a moderate interpolation between
A5 scale1 and the failed B0 full FIT-expectation normalization (~17.49x).
Architecture, auxiliary coefficients, natural sampling, augmentation, batch2,
optimizer, seed42, split/cache and single-checkpoint inference remain fixed.
Run fixed fold0 full50 after exact-default and finite-gradient preflight; only
expand after completed audited Macro-F1>=.75. Preregistration:
vindr_a21_focalscale2_preregistration_20260920.md.

A21 deployed from immutable A5 to
`/slurmshared/Ngoc/code/hcmus-density-auggeo-dropout30-focalscale2-20260920-v1`.
Config SHA256 `fa883f29feb33910ff985ce50b3866084f0c33ad5e7fc1f7d8fda0dcc852025f`;
semantic config delta is exactly arm metadata plus focal_scale2. Remote A5
suite 16/16 PASS; additional assertions verify scale1 bit-exact default,
scale2 changes only focal contribution, finite gradients/validation and fixed
split digest. A real RTX5090 cache batch completed finite forward/backward/
update: loss1.6025793552, scaled focal .0309424289, grad norm18.5060977936,
peak2.7021GiB. Submitted fixed fold0 only as job949_0; verified RUNNING on
master RTX5090, Requeue0/Restarts0, worker2/Vesta excluded. W&B xcitmw7c:
https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/xcitmw7c
No result yet; next review epoch10.

A23 first10: job955_0 remains RUNNING with finite losses. Selected epoch4
Macro .6504998124, accuracy .7227722772, QWK .5895798563, classes
[.6666666667,.5343511450,.7963302752,.6046511628], BCD mean .6451108610,
severe0; seven AMP skips, sampled counts [286,2626,10108,3110], and zero/10
checkpoints>=.75. It exceeds A5 matched first10 .5452488632 but trails direct
parent A6 .7829792575 and has weaker B/C/D. Continue unchanged; next review
epoch20. Exact report: vindr_a23_sampling035_first10_20260921.{json,md}.

A23 first20: selected remains epoch4 Macro .6504998124; no improvement in
epochs11--20. Accuracy .7227722772, QWK .5895798563, BCD mean .6451108610,
eleven AMP skips, cumulative sampled counts [563,5144,20303,6250], and zero/20
checkpoints>=.75. It trails A5 .7654421855 and A6 .7829792575 at the matched
horizon. Continue registered fold0 unchanged; next review epoch30. Exact
report: vindr_a23_sampling035_first20_20260921.{json,md}.

A23 first30: selected remains epoch4 Macro .6504998124; no improvement in
epochs11--30. Epoch30 .5380251657, thirteen AMP skips, cumulative sampled
counts [837,7742,30424,9387], and zero/30 checkpoints>=.75. Continue unchanged
through epoch50; next review epoch40. Exact report:
vindr_a23_sampling035_first30_20260921.{json,md}.

A23 first40: selected remains epoch4 Macro .6504998124, accuracy .7227722772,
QWK .5895798563; epoch40 Macro .5106178428. Finite training losses, sixteen
AMP skips and zero/40 checkpoints>=.75. Job955_0 verified RUNNING at44:05.
Continue full50 then audit; no confirmation folds launched. Report:
vindr_a23_sampling035_first40_20260921.md.

A23 completed50 screen audit PASS including saved predictions/checkpoint,
all fold manifests and W&B finished. Best remains epoch4 Macro .6504998124,
accuracy .7227722772, QWK .5895798563; zero/50 checkpoints>=.75, AMP skips17.
Epoch50 Macro .5039295807. Reject without confirmation folds. Report:
vindr_a23_sampling035_screen_20260921.md.

A24 registered after A23 rejection: A5 with training.amp=false only (plus
arm metadata). Real FP32 batch2/512 forward/backward/update preflight passed
with finite parameters and5.1951GiB peak allocation. Deployment from immutable
A5: /slurmshared/Ngoc/code/hcmus-density-auggeo-dropout30-fp32-20260921-v1.
Remote semantic config and fixed assignment digest checks PASS; config SHA
a2948d41e6c7235eb53098ac2701e19bec855bd40b1027ca7bac0ffdc5483fc6.
Submitted fixed fold0 full50 only as957_0. Verified RUNNING on master RTX5090,
Requeue0/Restarts0 and worker2 excluded. W&B ikzls2eb:
https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/ikzls2eb
Expand only after completed audited fold0 Macro>=.75. Next milestone10.

A24 first10: selected epoch8 Macro .5699346405, accuracy .8490099010,
QWK .6932383987; class F1 [0,.7111111111,.9019607843,.6666666667].
Finite losses, zero skipped updates and zero/10 checkpoints>=.75. Macro is
+.0246857774 over A5 matched first10. Epoch10 has13 false-A predictions,
so early evidence does not show elimination of boundary instability by FP32.
Continue full50; next milestone20. Report: vindr_a24_fp32_first10_20260921.md.

A22 first10: job950_0 remains RUNNING with finite losses. Selected epoch10
Macro .5607156940, accuracy .8341584158, QWK .6563623991, classes
[.2,.4375,.9053627760,.7], severe1; seven AMP skips and zero/10 checkpoints
>=.75. This is +.0154668308 versus A5 at the matched first10 horizon. Continue
the registered fold0 unchanged; next review epoch20. Exact report:
vindr_a22_ordinal025_first10_20260920.{json,md}.

A22 first20: selected moves to epoch18 Macro .6888524590, accuracy
.8094059406, QWK .6254214430, classes [.6666666667,.6133333333,
.8754098361,.6], severe0; ten AMP skips and zero/20 checkpoints>=.75. This is
-.0765897265 versus A5 at the matched first20 horizon (.7654421855). Continue
the registered fold0 unchanged through epoch50; next review epoch30. Exact
report: vindr_a22_ordinal025_first20_20260920.{json,md}.

A22 first30: selected moves to epoch22 Macro .7718528369, accuracy
.8019801980, QWK .6258219876, classes [1,.5957446809,.8666666667,.625],
severe0; thirteen AMP skips and one/30 checkpoint>=.75. This is
-.0177970193 versus A5's final selected fold0 (.7896498562), and class A is
only one DEV study. Continue unchanged through epoch50, audit the saved
checkpoint, and only then evaluate the expansion gate; next review epoch40.
Exact report: vindr_a22_ordinal025_first30_20260920.{json,md}.

A22 first40: selected remains epoch22 Macro .7718528369; no improvement in
epochs31--40. Epoch40 Macro .5396075191; sixteen cumulative AMP skips and
one/40 checkpoint>=.75. Continue unchanged through epoch50 and audit before
any folds1--4 launch. Exact report:
vindr_a22_ordinal025_first40_20260921.{json,md}.

A22 fold0 completed50 and audit PASS. Job950_0 COMPLETED ExitCode0:0 in
00:55:47 on master RTX5090 with Requeue0/Restarts0 and worker2/Vesta excluded;
W&B gdne1bkg verified finished. Selected epoch22 Macro .7718528369, accuracy
.8019801980, QWK .6258219876, classes [1,.5957446809,.8666666667,.625],
severe0; epoch50 .5179132318, one/50 checkpoints>=.75 and AMP skips17.
Checkpoint/prediction/split/probability/W&B audit passed. The registered fold0
gate therefore passed, and confirmation job951_[1-4] was launched for folds
1--4 only. All four tasks started RUNNING on RTX5090 nodes with Requeue0,
Restarts0 and worker2/Vesta excluded. Exact screen report:
vindr_a22_ordinal025_screen_20260921.{json,md}.
Confirmation W&B runs: fold1 8jhy78kl, fold2 43295usj, fold3 p96msbjn,
fold4 dj5bsgwx.

A22 CV5 first10: all confirmation tasks remain RUNNING on RTX5090 with no
requeue/restart and finite losses. Best-through-10 fold Macro-F1 values are
[.5607156940,.5662064283,.6818484501,.5488877418,.5246701355], giving mean
.5764656900, sample SD .0610372092 and min .5246701355. This is early selected
DEV evidence only; continue all confirmation folds unchanged through epoch50,
next review epoch20. Exact report:
vindr_a22_ordinal025_cv5_first10_20260921.{json,md}.

A22 CV5 first20: best-through-20 fold Macro-F1 values are [.6888524590,
.5662064283,.6818484501,.5932826717,.5246701355], giving mean .6109720289,
sample SD .0722040817 and min .5246701355. Mean class F1 A/B/C/D is
[.3333333333,.6473786115,.8838711803,.5793049906]. All confirmation tasks
remain RUNNING on RTX5090 with finite losses and no requeue/restart. Continue
unchanged; next review epoch30. Exact report:
vindr_a22_ordinal025_cv5_first20_20260921.{json,md}.

A22 CV5 first30: best-through-30 fold Macro-F1 values are [.7718528369,
.5662064283,.6818484501,.5932826717,.5626107987], giving mean .6351602372,
sample SD .0903277855 and min .5626107987. Mean accuracy .8170601676, mean
QWK .6343549801 and mean class F1 [.45,.6218929177,.8841858883,.5845621426].
All tasks remain RUNNING on RTX5090 with finite losses and no requeue/restart.
Continue unchanged; next review epoch40. Exact report:
vindr_a22_ordinal025_cv5_first30_20260921.{json,md}.

A22 CV5 first40: no fold selected a new best checkpoint in epochs31--40, so
the aggregate remains mean .6351602372, sample SD .0903277855, min
.5626107987, mean accuracy .8170601676, mean QWK .6343549801 and mean class
F1 [.45,.6218929177,.8841858883,.5845621426]. All confirmation tasks remain
RUNNING on RTX5090 with finite losses and no requeue/restart. Continue through
epoch50 and audit. Exact report:
vindr_a22_ordinal025_cv5_first40_20260921.{json,md}.

A22 final CV5 audit PASS. Job951 folds1--4 all COMPLETED50 with ExitCode0:0,
Requeue0/Restarts0 on RTX5090 and worker2/Vesta excluded; all five W&B runs
verified finished. Selected fold vector [.7718528369,.5662064283,.6818484501,
.5932826717,.5626107987] gives mean .6351602372, sample SD .0903277855, min
.5626107987, accuracy .8170601676, QWK .6343549801 and class means
[.45,.6218929177,.8841858883,.5845621426]. It fails mean>=.70, SD<=.05 and
min>=.65, and trails A5 mean by .0676680429. Reject A22 and retain A5 as the
best completed mean-CV5 reference. Exact report:
vindr_a22_ordinal025_cv5_results_20260921.{json,md}.
A22 audited summary uytf37nh was published and independently read back from
the W&B API as finished with exact mean .6351602372, sample SD .0903277855
and audit_passed true:
https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/uytf37nh

A23 preregistered after A22 rejection: use A6 as the direct parent and change
only FIT sampling power .25->.35. A6 has the strongest completed stability so
far (mean .6765513839, sample SD .0644461991, min .6194960833); power .35
moderately raises expected fold0 FIT A/B/D exposure while reducing C exposure,
without full balancing. Architecture, losses, augmentation, optimizer, batch2,
seed42, fixed split/cache and single flat-head checkpoint inference remain
unchanged. Run fixed fold0 full50 first and expand only after completed audited
Macro-F1>=.75. Preregistration:
vindr_a23_sampling035_preregistration_20260921.md.

A23 deployed from immutable A6 to
`/slurmshared/Ngoc/code/hcmus-density-auggeo-dropout30-sampling035-20260921-v1`.
Config SHA256 `0b788b8671c3aced01b34bbb246847433f450312096c130a3cdb7be106f6f75d`;
semantic delta is exactly arm metadata plus sampling power .25->.35. Remote
suite 16/16 PASS, all fixed manifests/digest validated, and the deterministic
fold0 sampler drew [17,284,1005,307] A/B/C/D cases over 1613 draws with all
classes present. Submitted fixed fold0 only as job955_0; verified RUNNING on
master RTX5090, Requeue0/Restarts0, worker2/Vesta excluded. W&B hk1ukax3:
https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/hk1ukax3
No result yet; next review epoch10.

A21 first10: job949_0 remains RUNNING with finite losses. Selected epoch6
Macro .5507002801, accuracy .8217821782, QWK .6655936724, classes
[0,.6666666667,.8806722689,.6554621849], severe0; eight AMP skips. This is
only +.0054514169 over A5 matched first10 .5452488632 and below the .75 gate.
Epoch10 is .5348861615 with four severe errors. Continue unchanged full50;
next review20. Exact report: vindr_a21_focalscale2_first10_20260920.md.

A21 first20: selected remains epoch6 Macro .5507002801; no improvement in
epochs11--20, epoch20 .5137244133, zero/20 checkpoints>=.75 and cumulative
AMP skips13. A5 reaches .7654421855 at the matched horizon. Continue the
registered fold0 unchanged full50; no confirmation, next review30. Exact
report: vindr_a21_focalscale2_first20_20260920.md.

A21 first30: selected moves to epoch30 but improves only to Macro .5509488356,
accuracy .8316831683, QWK .6594942985, classes [0,.6966292135,.8903436989,
.6168224299], severe0; zero/30 checkpoints>=.75 and cumulative AMP skips15.
A5 is .7896498562 at the matched horizon. Continue unchanged full50 for audit;
no confirmation, next review40. Exact report:
vindr_a21_focalscale2_first30_20260920.md.

A21 first40: selected remains epoch30 Macro .5509488356; no improvement in
epochs31--40, epoch40 .5208919319, zero/40 checkpoints>=.75 and cumulative AMP
skips16. Continue unchanged through epoch50 and audit; reject without
confirmation unless the registered gate is reached. Exact report:
vindr_a21_focalscale2_first40_20260920.md.

A21 completed50 screen audit PASS. Job949_0 COMPLETED ExitCode0:0 in 00:55:59
on master RTX5090 with Requeue0/Restarts0 and worker2/Vesta excluded; W&B
xcitmw7c verified finished. Selected epoch30 Macro .5509488356, accuracy
.8316831683, QWK .6594942985, classes [0,.6966292135,.8903436989,
.6168224299], severe0; epoch50 .5302099892, zero/50 checkpoints>=.75 and AMP
skips17. Reject A21 without folds1--4: it trails A5 fold0 by .2387010206 and
does not recover class A. Exact report:
vindr_a21_focalscale2_screen_20260920.{json,md}.

A22 preregistered after A21 rejection: return to A5 and change only ordinal
loss coefficient .5->.25. The CORAL diagnostic found a substantial ordinal
loss floor; weight1.0 previously hurt CV5, while focal-scale2 failed its
screen. A22 tests reduced potentially competing ordinal gradient without
removing the head. Architecture, all other losses, natural sampling,
augmentation, batch2, optimizer, seed42, fixed split/cache and single flat-head
checkpoint inference remain unchanged. Fixed fold0 full50 first; expand only
after completed audited Macro-F1>=.75. Preregistration:
vindr_a22_ordinal025_preregistration_20260920.md.

A22 deployed from immutable A5 to
`/slurmshared/Ngoc/code/hcmus-density-auggeo-dropout30-ordinal025-20260920-v1`.
Config SHA256 `9e5e64be05fb4158a9775b3fa1a10ab7e4587fa81b3ec8bf71a2d6a4ad1b7f7e`;
semantic config delta is exactly arm metadata plus ordinal .5->.25. Remote A5
suite 16/16 PASS and the fixed split digest remains
`43daa86936ee7b1bae1b200836fb1afdfe0c8294c7c865d8f5758bf989f12a9a`.
Submitted fixed fold0 only as job950_0; verified RUNNING on master RTX5090,
Requeue0/Restarts0, worker2/Vesta excluded. W&B gdne1bkg:
https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/gdne1bkg
No result yet; next review epoch10.
## A30 final CV5 and decision

A30 (`auggeo_dropout40_sampling025`) completed 50 epochs on all five folds:
job981 fold0 plus job982 folds1–4. All jobs completed 0:0 on permitted RTX
5090 nodes, with no Vesta use. Full read-only provenance/data/prediction/W&B
audit PASS; all source runs are finished and the frozen assignment SHA256 is
`43daa86936ee7b1bae1b200836fb1afdfe0c8294c7c865d8f5758bf989f12a9a`.

Selected Macro-F1 values are [.7025951909, .7584943371, .6402752997,
.6864294858, .7618615908], giving mean .7099311809, sample SD .0512670358,
and minimum .6402752997. Mean accuracy is .8334041717, mean QWK .6258195383,
and mean B/C/D F1 .7021304634. Mean >=.70 passes; SD <=.05 and minimum >=.65
fail narrowly. A30 is not accepted as stable. Results are selected DEV on one
seed, not independent test; class A has six cases. Audited W&B summary:
https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/n8yrk899

A31 remains a one-factor screen from A6: global LR 5e-5 -> 2.5e-5. Its fold0
expansion gate is amended to .70 before submission; final stability gates
remain mean>=.70, sample SD<=.05, minimum>=.65. No ensemble or split change.

## A31 first-20 checkpoint

A31 job986 fold0 runs on master RTX5090 with worker2/Vesta excluded. The
best first-20 selected DEV Macro-F1 is .6851250647 at epoch6, unchanged from
first10 and below the .70 expansion gate. Accuracy .7871287129, QWK
.6311990489, class F1 [.666667,.596491,.854701,.622642], zero severe errors.
All observed losses are finite. Continue unchanged to50; no other folds are
submitted. Next review at40, then completed screen audit.

## A31 final screen and A32 decision

A31 job986 fold0 completed50 on master RTX5090, ExitCode0:0, no restart or
requeue, worker2/Vesta excluded. Screen audit PASS and W&B `9v7h7cr0` is
finished. Selected epoch6 Macro-F1 .6851250647, accuracy .7871287129, QWK
.6311990489, class F1 [.666667,.596491,.854701,.622642]. This is below the
.70 expansion gate; reject A31 without folds1–4.

A32 is preregistered from near-passing A30 with only dropout .40 -> .45.
Everything else remains fixed, including sampling .25 and architecture.
This is a bounded interpolation given A9 dropout .50 was harmful, not a
claim of monotonic improvement. Screen fold0 full50; expand only if audited
>=.70. Final gates remain mean>=.70, sample SD<=.05, minimum>=.65.

## A32 completed screen

A32 job987 fold0 completed50 on master RTX5090, ExitCode0:0, no restart or
requeue, worker2/Vesta excluded. Screen audit PASS and W&B `4fyhjmkw` is
finished. Selected epoch4 Macro-F1 .7771719287, accuracy .7871287129, QWK
.6339685642, class F1 [1,.607143,.851138,.650407], one severe error; epoch50
.5180146711. It passes the .70 expansion gate. Preserve job987 fold0 and run
only folds1–4 from the identical immutable A32 snapshot/config. Full gates
remain mean>=.70, sample SD<=.05, minimum>=.65; selected DEV, not independent.

## A32 final CV5 and A33 decision

A32 jobs987/988 completed all folds50 on permitted RTX5090 nodes. Full audit
PASS; all W&B sources finished and 2017-case union/split provenance exact.
Fold scores [.7771719287,.5566693818,.5645674658,.7015347952,.7542818388]
give mean .6708450821, sample SD .1043311692, minimum .5566693818, accuracy
.8170650812, QWK .6311131110. A32 fails all gates and is rejected. Audited
summary: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/qjxsgo3w

A33 is preregistered from A30 with only neighbor loss .20 -> .10. It targets
A30's weak D discrimination; A25 supplies limited fold0 prior but did not
test this sampling/dropout interaction. Screen fold0 full50 first; expand
only after audited >=.70. Final gates remain mean>=.70, SD<=.05, min>=.65.

A33 job992 fold0 completed50 on master RTX5090, ExitCode0:0, no restart or
requeue, worker2/Vesta excluded. Screen audit PASS and W&B `x6422mve` is
finished. Selected epoch2 Macro-F1 .8159754728, accuracy .8341584158, QWK
.6912124389, class F1 [1,.678899,.887755,.697248], BCD mean .754634, one
severe error. It passes the .70 expansion gate. Preserve job992 fold0 and
run only folds1–4 from the identical immutable snapshot/config.

## A33 final CV5 and A34 decision

A33 jobs992/993 completed all folds50 on permitted RTX5090 nodes; worker2/
Vesta was excluded. Full audit PASS, including all 2,017 cases, frozen split,
checkpoints, predictions and finished W&B sources. Fold scores
[.8159754728,.5455677048,.6194453040,.6704483700,.6509916301] give mean
.6604856963, sample SD .0990667973 and minimum .5455677048. A33 fails all
three gates and is rejected. Audited summary:
https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/hrrvh977

A34 is preregistered from A6 with only dropout .30 -> .35. This bounded
midpoint tests whether part of A30's mean gain can be retained without its
borderline dispersion; A32 already shows .45 is too strong. Screen fixed
fold0 for 50 epochs and expand only after audited Macro-F1 >=.70. Final gates
remain mean>=.70, sample SD<=.05, minimum>=.65; no ensemble or split change.

A34 deployed from immutable A6 to
`/slurmshared/Ngoc/code/hcmus-density-auggeo-dropout35-sampling025-20260921-v1`.
Exact parsed delta (arm plus dropout .30 -> .35), source/script/split parity,
fixed assignment digest and 16/16 tests PASS. Config SHA256
`b28bc4cc4d34017ba0f26f85478a637a27eb92ff353147bc95d33a5ddddfd9e7`.
Fold0 job997 is RUNNING on master RTX5090, Requeue0/Restarts0; worker2/Vesta
excluded. W&B: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/6bhg258e

A34 first10: selected epoch6 Macro-F1 .6290481887, accuracy .8118811881,
QWK .6551662174, class F1 [.4,.595745,.878939,.641509], severe0. It is above
A30 but below A6 at the matched horizon and below the .70 expansion gate.
Job997 remains RUNNING on master RTX5090 with finite losses and one AMP skip.
Continue unchanged; next score review epoch20. Exact report:
vindr_a34_dropout35_sampling025_first10_20260921.md.

A34 first20: selected remains epoch6 Macro-F1 .6290481887; epoch20 is
.5103016099, with finite losses and zero cumulative AMP skips. It remains
below the .70 gate and trails A6/A30 at the matched horizon. Continue fold0
unchanged through50; no confirmation folds. Next score review epoch40.
Exact report: vindr_a34_dropout35_sampling025_first20_20260921.md.

A34 first40: selected improves at epoch33 to Macro-F1 .7779130831, accuracy
.8391089109, QWK .6138535927, class F1 [1,.589744,.899687,.622222], with one
severe error. It exceeds the .70 numerical screen gate but includes only one
class-A DEV study. Job997 remains RUNNING on master RTX5090 with finite
losses and zero AMP skips. Continue unchanged to50, then audit before any
confirmation expansion. Exact report:
vindr_a34_dropout35_sampling025_first40_20260921.md.

A34 job997 completed50 on master RTX5090, ExitCode0:0, no restart/requeue and
no Vesta use. Screen audit PASS; W&B `6bhg258e` is finished. Selected epoch33
Macro-F1 .7779130831, accuracy .8391089109, QWK .6138535927, class F1
[1,.589744,.899687,.622222], severe1; epoch50 .5298463894. It passes the .70
expansion gate. Preserve job997 fold0 and run only folds1–4 from the identical
immutable A34 snapshot/config. Exact report:
vindr_a34_dropout35_sampling025_screen_20260921.{json,md}.

A34 confirmation job998 folds1–4 started from the identical immutable
snapshot/config on master and worker1 RTX5090; worker2/Vesta excluded,
Requeue0/Restarts0. W&B: fold1 `v9oaqxul`, fold2 `n12l50ul`, fold3
`g4a8wqyv`, fold4 `32h0eb36`. Retain audited fold0 job997. Run all folds to
50 and review only at common 10–20 epoch intervals. Details:
vindr_a34_confirmation_20260921.md.

A34 common first10: selected fold scores [.6290481887,.7297439218,
.6103683960,.6168008299,.5268655345] give provisional mean .6225653742,
sample SD .0722317856 and minimum .5268655345. Mean accuracy .817057711,
mean QWK .642011399, mean class F1 [.373333,.646087,.882636,.588205]. All
tasks remain RUNNING on permitted RTX5090 nodes with no restart/requeue.
Continue unchanged; next review common first20. Exact report:
vindr_a34_confirmation_first10_20260921.md.

Fold-difficulty review: A34 first10 currently ranks fold4 worst (.526866),
then fold2 (.610368) and fold3 (.616801). Across 25 completed CV5 result
files, however, fold1 is persistently hardest (mean .573657, median .563956),
mainly because mean class-A F1 is only .078987; fold3 is second-hardest
(mean .619210). Fold2 is persistently weak on D, while fold4 is weaker on B
and D. Do not alter/drop folds or infer resolution from one early checkpoint.
Evidence: vindr_fold_difficulty_review_20260921.md.

A34 common first20: selected fold scores [.6290481887,.7297439218,
.6392881231,.6168008299,.5510789005] give provisional mean .6331919928,
sample SD .064007498 and minimum .5510789005. Fold4 remains worst because its
single A case has not been recognized in epochs1–20, although selected BCD
mean is .734772. Fold3 is next-worst. All tasks remain RUNNING normally;
continue unchanged to common first40. Exact report:
vindr_a34_confirmation_first20_20260921.md.

## Screening protocol revision after fold-difficulty analysis

For every new arm after A34, screen the two fixed historically weakest folds
1 and 3 for full50 before CV5 expansion. The pair is frozen from aggregate
evidence across 25 completed CV5 reports, not chosen anew per arm. Expand only
if both audits PASS, their mean Macro-F1 >=.70, and neither is below .65.
Retain those runs for final CV5; never rerun/replace a weak screen. A34 was
already launched under its prior preregistration and continues unchanged.
Full details: goal_two_weakest_folds_revision_20260921.md.

A34 common first40: fold scores [.7779130831,.7297439218,.6583553955,
.6168008299,.5510789005] give provisional mean .6667784262, sample SD
.0898201717 and minimum .5510789005. Fold4 remains worst, fold3 second-worst,
and fold2 selected D F1 is .441558. All tasks remain RUNNING normally; finish
50 then audit. Under the later two-fold screen rule, fold1 .729744 plus fold3
.616801 would fail (mean .673272, minimum .616801), so A34 would not have
expanded. Exact report: vindr_a34_confirmation_first40_20260921.md.

## A34 final CV5 and A35 decision

A34 jobs997/998 completed all folds50 on permitted RTX5090 nodes; no Vesta.
Full audit PASS and all W&B sources finished. Fold scores [.7779130831,
.7297439221,.6583553960,.6168008301,.5510789005] give mean .6667784264,
sample SD .0898201723 and minimum .5510789005. A34 fails all gates and is
rejected. Audited summary:
https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/yv44es8x

A35 is preregistered from A30 with only neighbor loss .20 -> .30. It tests
stronger cost on ordinal-distance errors, especially D->C, after A33's .10
direction failed. Under the revised protocol, run only fixed folds1 and3
full50 first; expand to folds0/2/4 only if both audits PASS, two-fold mean
>=.70 and minimum>=.65. No ensemble, split or architecture change.

A35 deployed from immutable A30 with exact parsed delta (arm plus neighbor
.20 -> .30), source/script/split parity, fixed assignment digest, and 16/16
tests PASS. Config SHA256
`9b1f671b63dab1840ea44d2ed87547e74e12006517f2c5245725b32b61699147`.
Only folds1 and3 were submitted as job1002; both started on master RTX5090,
Requeue0/Restarts0, worker2/Vesta excluded. W&B fold1 `ksdm0x9c`, fold3
`jytyd5ja`. Review at common10–20 epochs; no other folds submitted.

## Goal revision: substantive architecture changes allowed

The prior requirement to remain close to DenseNet121 plus handcrafted
hierarchical fusion is superseded. Major model changes are now allowed when
they isolate a clear hypothesis. Dataset/cache, grouped split, seed42,
evaluation, two-fold screen (fixed folds1/3), RTX5090-only rule, no-ensemble
rule and audit/W&B requirements remain fixed.

Finish already-running A35 unchanged to close the neighbor-loss direction.
If it fails, the first architectural candidate will retain DenseNet121 but
replace fixed gate/difference/product fusion with explicit view/laterality
embeddings and learnable attention over four view tokens. Later candidates
may test small view-specific adapters, an ordinal-aware primary head, and
only then a backbone replacement, one architectural hypothesis per arm.
Full revised goal: goal_architecture_revision_20260921.md.

A35 common first10 on fixed stress folds1/3: scores [.5594039526,
.6628659941] give mean .6111349733, sample SD .0731587111 and minimum
.5594039526. Fold1 F1_A is zero; both expansion gates are unmet. Both tasks
remain RUNNING normally on RTX5090. Continue unchanged to common20. If the
completed screen fails, proceed to the registered architecture roadmap rather
than another small scalar tweak. Exact report:
vindr_a35_neighbor030_twofold_first10_20260921.md.

A35 common first20: fold1 remains .5594039526 while fold3 improves to
.6681361544, giving mean .6137700535, sample SD .0768852772 and minimum
.5594039526. Both expansion gates remain unmet. Continue unchanged to
common40. Prepare/test A36 attention fusion in parallel, but do not launch it
before A35 completes and is audited. Exact report:
vindr_a35_neighbor030_twofold_first20_20260921.md.

A36 attention-fusion snapshot is prepared but not launched. It replaces the
entire handcrafted relational fusion with a 2-layer/8-head, 256-dimensional
four-view attention encoder using explicit CC/MLO and left/right embeddings
plus an exam token. A30 training recipe and heads remain fixed. Parameter
count is 9,070,473 versus A30 11,163,787. Default relational mode is state-
dict and output bit-exact to immutable A30; 17/17 snapshot tests PASS. Wait
for completed A35 audit, then perform real RTX5090 cache preflight before any
fold1/3 launch. Preregistration:
vindr_a36_viewtoken_attention_preregistration_20260921.md.

A35 common first40: fold1 remains .5594039526 and fold3 improves to
.7042288276, giving mean .6318163901, sample SD .1024066512 and minimum
.5594039526. Fold1 still has F1_A zero. Both expansion gates fail; do not
expand A35. Finish50 and audit, then perform A36 RTX5090 preflight/launch.
Exact report: vindr_a35_neighbor030_twofold_first40_20260921.md.

A35 completed50 on fixed folds1/3. Both read-only audits PASS. Selected
Macro-F1 scores are [.5594039526, .7042288276], with two-fold mean
.6318163901 and minimum .5594039526. The screen fails both expansion gates,
so folds0/2/4 are not launched. Stronger neighbor loss is rejected and the
campaign moves to the preregistered A36 view-token attention architecture.
Exact report: vindr_a35_neighbor030_twofold_final_20260921.md.

A36 real-cache preflight PASS on the master NVIDIA GeForce RTX5090 with
batch shape [2,4,3,512,512]. Forward, multitask loss, backward, clipping and
AdamW update were finite; AMP recovered after two initial skipped updates.
Peak allocated GPU memory was 2.686 GiB. The attention checkpoint also passed
strict save/load bit-exact roundtrip. A36 is cleared for folds1/3 only.

A36 launched as job1007 on folds1/3 only. Both tasks run on
slurm-b20a-master-0 RTX5090; worker2/Vesta is excluded, requeue is disabled,
and restarts are zero. W&B IDs are fold1 v4vdj0ig and fold3 7be8i6ku.
Do not expand before completed audits and both registered numerical gates.
Exact report: vindr_a36_viewtoken_attention_launch_20260921.md.

A36 common first10 scores are fold1 .5628254127 at epoch6 and fold3
.7267061401 at epoch8. Their mean is .6447657764, sample SD .1158811737 and
minimum .5628254127. This improves both A35 first10 scores, especially fold3,
but fold1 still has F1_A zero and both expansion gates fail. Continue
unchanged to common20; do not expand. Exact report:
vindr_a36_viewtoken_attention_first10_20260921.md.

A36 common first20 is unchanged from first10: fold1 .5628254127 at epoch6,
fold3 .7267061401 at epoch8, mean .6447657764, sample SD .1158811737 and
minimum .5628254127. Continue immutable A36 to50 for audit but do not expand.
Prepare a conditional spatial-token attention candidate that retains regional
feature-map information while holding data/loss/optimizer/heads fixed. Exact
report: vindr_a36_viewtoken_attention_first20_20260921.md.

A37 is preregistered conditionally, not launched. It replaces A36's four
globally pooled view tokens with 64 regional tokens: a 4x4 grid from each of
four DenseNet feature maps, with spatial/view/laterality embeddings and the
same 2-layer/8-head transformer. All other experimental factors stay fixed.
The isolated snapshot passes 19/19 tests, strict checkpoint roundtrip, and
matched-seed backward-compatibility hashes. Real RTX5090 cache preflight is
pending because both permitted GPUs are occupied by A36; queued job1009 was
cancelled without running. Exact preregistration:
vindr_a37_spatial_attention_preregistration_20260922.md.

A36 common first40: fold1 .5631938748 at epoch21 and fold3 .7398416768 at
epoch35, mean .6515177758, sample SD .1249088587 and minimum .5631938748.
Fold3 improves strongly, but fold1 remains limiting with F1_A zero. Both
expansion gates fail; do not launch folds0/2/4. Finish50 and audit, then run
A37's pending RTX5090 cache preflight. Exact report:
vindr_a36_viewtoken_attention_first40_20260922.md.

A36 completed50 and both audits PASS. Final selected scores remain fold1
.5631938748 and fold3 .7398416768, mean .6515177758, sample SD .1249088587
and minimum .5631938748. Both expansion gates fail; folds0/2/4 are not run.
Reject four-view-vector attention and proceed to A37's real-cache preflight.
Exact report: vindr_a36_viewtoken_attention_twofold_final_20260922.md.

A37 real-cache preflight PASS on the master RTX5090 with batch shape
[2,4,3,512,512]. Forward/loss/backward/clipping/AdamW update were finite,
AMP recovered after one initial skipped update, and peak allocated memory was
2.686 GiB. A37 is cleared for the fixed folds1/3 screen only.

A37 launched as job1011 on folds1/3 only. Both tasks are on the master
RTX5090; worker2/Vesta is excluded, requeue is disabled and restarts are zero.
W&B IDs: fold1 jr97gvza and fold3 q6fj2umt. Do not expand before completed
audits and both registered numerical gates. Exact report:
vindr_a37_spatial_attention_launch_20260922.md.

A37 common first10 scores are fold1 .5708455271 at epoch1 and fold3
.6195316312 at epoch3, mean .5951885791, sample SD .0344262744 and minimum
.5708455271. Dispersion is lower than A36 but the mean is substantially worse;
both expansion gates fail. Continue unchanged to common20 to test whether
the 64-token model simply converges more slowly. Exact report:
vindr_a37_spatial_attention_first10_20260922.md.

A37 common first20 is unchanged from first10: fold1 .5708455271 at epoch1,
fold3 .6195316312 at epoch3, mean .5951885791, sample SD .0344262744 and
minimum .5708455271. The slow-convergence hypothesis is weakened; do not
expand. Continue to50 for audit. If rejected, test a monotonically constrained
ordinal-primary prediction head rather than further increasing fusion
capacity. Exact report: vindr_a37_spatial_attention_first20_20260922.md.

A38 monotonic ordinal-primary is preregistered conditionally, not launched.
It returns to A30's strongest relational fusion and changes only the primary
output parameterization to one scalar score plus three strictly ordered
thresholds. The resulting valid A/B/C/D distribution is the sole primary
training/inference path. The snapshot passes 18/18 tests, strict checkpoint
roundtrip and matched-seed bit-exact A30 backward compatibility. Real RTX5090
cache preflight waits until A37 releases the two permitted GPUs. Exact report:
vindr_a38_ordinal_primary_preregistration_20260922.md.

A37 original fold1 job1011_1 terminated after epoch25 due to a DataLoader
shared-memory unlink error, not a model/metric stop. The incomplete W&B run
jr97gvza and run directory are retained. One exact technical retry launched
as job1013_1/W&B zg75vjst from the same immutable snapshot/config/seed/split,
with no settings changed, on master RTX5090 and no Vesta. Compare its first25
history to the retained run; do not choose between reruns by score. Exact
report: vindr_a37_fold1_infrastructure_retry_20260922.md.

A37 fold1 retry first10 reproduces the retained failed run bit-for-bit after
excluding wall-clock seconds: losses, validation metrics/confusion matrices,
sampled counts, learning rates and AMP skip counts are identical. Continue to
common25 for the second reproducibility check, then finish50.

A37 fold1 retry common25 reproduces all 25 original records bit-for-bit after
excluding wall-clock seconds. Both histories select epoch1 Macro-F1
.5708455271. The retry is accepted as a faithful technical reproduction and
continues to50; no score-based choice between runs occurred.

A37 completed after the exact fold1 technical retry; both completed audits
PASS. Final scores are fold1 .5708455271 and fold3 .6195316312, mean
.5951885791, sample SD .0344262744 and minimum .5708455271. Both expansion
gates fail; folds0/2/4 are not run. Reject spatial-token attention and proceed
to A38 ordinal-primary preflight. Exact report:
vindr_a37_spatial_attention_twofold_final_20260922.md.

A38 real-cache preflight PASS on master RTX5090 with batch shape
[2,4,3,512,512]. Forward/loss/backward/clipping/AdamW update were finite,
AMP required zero skipped updates, and peak allocated memory was 2.702 GiB.
A38 is cleared for fixed folds1/3 only.

A38 launched as job1015 on folds1/3 only. Both tasks run on master RTX5090;
worker2/Vesta is excluded, requeue is disabled and restarts are zero. W&B IDs
are fold1 z534lziw and fold3 wwjt35v9. Do not expand before completed audits
and both registered numerical gates. Exact report:
vindr_a38_ordinal_primary_launch_20260922.md.

A38 common first10 collapses: fold1 .1190220635 and fold3 .1129950332, mean
.1160085483, sample SD .0042617540 and minimum .1129950332. The head predicts
A but sends most B/C cases to A/D. Initial ordinal threshold gaps of 1 cap
interior-class probability near .245 and give B/C no useful argmax region;
selected gaps have only grown to about 1.16–1.24. Continue unchanged to
common20, do not expand, and prepare a corrected head with a tested argmax
region for every class. Exact report:
vindr_a38_ordinal_primary_first10_20260922.md.

A39 is preregistered conditionally, not launched. It corrects A38's structural
initialization defect by changing only threshold spacing 1.0 -> 2.0, from
[-1,0,1] to [-2,0,2]. A direct test proves scalar scores [-5,-1,1,5] yield
argmax A/B/C/D, so every class has a valid initial decision region. The
snapshot passes 19/19 tests, checkpoint roundtrip and bit-exact A38 default
backward compatibility. Real RTX5090 preflight waits for A38. Exact report:
vindr_a39_ordinal_primary_wide_preregistration_20260922.md.

A38 common first20 improves only to fold1 .1486328757 and fold3 .1727257536,
mean .1606793146, sample SD .0170362373 and minimum .1486328757. Learned gaps
reach only 1.31–1.43, around the theoretical 1.386 boundary, so B/C remain
mostly mapped to A/D. A38 fails decisively; do not expand. Finish50/audit,
then preflight A39 spacing2. Exact report:
vindr_a38_ordinal_primary_first20_20260922.md.

A38 completed50 and both audits PASS. Final scores recover to fold1
.5521366746 and fold3 .4983092305, mean .5252229525, sample SD .0380617508
and minimum .4983092305, but remain far below the gates and A30. Folds0/2/4
are not run. Reject unit-gap A38 and proceed to A39 wide-gap preflight. Exact
report: vindr_a38_ordinal_primary_twofold_final_20260922.md.

A39 real-cache preflight PASS on master RTX5090 with batch shape
[2,4,3,512,512]. Forward/loss/backward/clipping/AdamW update were finite;
AMP recovered after two initial skipped updates and peak memory was 2.702 GiB.
A39 is cleared for fixed folds1/3 only.

A39 launched as job1018 on folds1/3 only. Both tasks run on master RTX5090;
worker2/Vesta is excluded, requeue is disabled and restarts are zero. W&B IDs
are fold1 fzts4z74 and fold3 1qqpu7sq. Do not expand before completed audits
and both numerical gates. Exact report:
vindr_a39_ordinal_primary_wide_launch_20260922.md.

A39 common first10 scores are fold1 .5410715782 and fold3 .5943430423, mean
.5677073102, sample SD .0376686135 and minimum .5410715782. This removes
A38's A/D collapse and improves its matched first10 mean from .116009, thereby
validating the gap diagnosis, but remains below both gates and fold1 F1_A is
zero. Continue unchanged to common20; do not expand. Exact report:
vindr_a39_ordinal_primary_wide_first10_20260922.md.

A39 common first20 reaches fold1 .5410715782 and fold3 .7053704434, mean
.6232210108, sample SD .1161768418 and minimum .5410715782. Fold3 validates
the corrected head, but fold1 remains stuck with F1_A zero; both expansion
gates fail. Continue to50/audit, do not expand. If rejected, return to A30
fusion/head/loss and isolate a major backbone replacement next. Exact report:
vindr_a39_ordinal_primary_wide_first20_20260922.md.

A40 ConvNeXt-Tiny is preregistered conditionally, not launched. It returns
fusion/head/loss/training to A30 and changes only the ImageNet backbone from
DenseNet121 to ConvNeXt-Tiny. The model has 30,387,819 parameters; overfitting
is an explicit risk. Snapshot tests pass 18/18, checkpoint roundtrip passes,
the old A30 path is matched-seed bit-exact, and official pretrained weights
load from shared cache. Real RTX5090 preflight waits for A39. Exact report:
vindr_a40_convnext_relational_preregistration_20260922.md.

A39 completed50 and both audits PASS. Final scores are fold1 .5427479530 and
fold3 .7053704434, mean .6240591982, sample SD .1149914658 and minimum
.5427479530. Both expansion gates fail; folds0/2/4 are not run. The wider gap
fixes A38's middle-class geometry but does not stabilize fold1, and A39 is
worse than the matched A30 two-fold mean .7224619115. Reject the ordinal
primary family and proceed to A40 ConvNeXt-Tiny preflight. Exact report:
vindr_a39_ordinal_primary_wide_twofold_final_20260922.md.

A40 real-cache preflight PASS on master RTX5090 with batch shape
[2,4,3,512,512]. Forward/loss/backward/clipping/AdamW update were finite,
AMP recovered after two skipped updates, and peak allocated memory was
2.632 GiB. A40 is cleared for fixed folds1/3 only. Exact report:
vindr_a40_convnext_relational_preflight_20260922.md.

A40 launched as job1022 on fixed folds1/3 only. Both tasks run on master
RTX5090; worker2/Vesta is excluded. W&B IDs are fold1 kgp5gj2y and fold3
itp6g9co. Do not expand before completed audits and both registered numerical
gates. Exact report: vindr_a40_convnext_relational_launch_20260922.md.

A40 common first10 selects fold1 .8126870715 at epoch4 and fold3 .6822455124
at epoch2, mean .7474662919, sample SD .0922361110 and minimum .6822455124.
The early numerical screen gates are met and the matched A30 two-fold first10
mean is only .6170961925, but the gain is concentrated in fold1 and rare-A
counts remain too small for a strong claim. Epoch10 scores have fallen to
.553647/.491479, so checkpoint sensitivity remains. Continue unchanged to
common20 and full50/audit; do not expand yet. Exact report:
vindr_a40_convnext_relational_first10_20260922.md.

A40 common first20 remains unchanged: fold1 .8126870715 at epoch4 and fold3
.6822455124 at epoch2, mean .7474662919, sample SD .0922361110 and minimum
.6822455124. The numerical screen gates still pass, but epoch20 scores have
decayed to .516132/.530603 and no checkpoint after epoch4 improves selection.
Continue unchanged to full50/audit; do not tune or expand from this
intermediate result. Exact report:
vindr_a40_convnext_relational_first20_20260922.md.

A40 common first30 is still unchanged: fold1 .8126870715 at epoch4 and fold3
.6822455124 at epoch2, mean .7474662919, sample SD .0922361110 and minimum
.6822455124. Epoch30 scores are .549780/.518714 and no later checkpoint has
improved selection. Continue unchanged to full50/audit; do not expand yet.
Exact report: vindr_a40_convnext_relational_first30_20260922.md.

A40 completed50 and both two-fold audits PASS. Fold1 selects .8126870715 at
epoch4 and fold3 improves to .6936746863 at epoch34, giving mean .7531808789,
sample SD .0841544646 and minimum .6936746863. Both registered expansion
gates pass. Preserve these screen runs and launch only folds0/2/4 from the
same immutable snapshot/config; final acceptance still requires all CV5
gates. Exact report: vindr_a40_convnext_relational_twofold_final_20260922.md.

A40 expanded as job1024 on folds0/2/4 only, preserving job1022 folds1/3.
Folds0/2 run on master RTX5090 and fold4 on worker1 RTX5090; no task uses
worker2/Vesta. W&B IDs are sqcl5ezc, o3ln0ceo and qfsuypzh. Final CV5 results
remain pending full50 and all five audits. Exact report:
vindr_a40_convnext_relational_cv5_expansion_launch_20260922.md.

A40 common CV5 first10 selects folds0--4 at .8212558177/.8126870715/
.5439920998/.6822455124/.7268438333. Mean .7174048669 passes, but sample SD
.1132044396 and minimum .5439920998 fail because fold2 is the new bottleneck.
This is not grounds to stop: completed screen fold3 improved only at epoch34.
Continue job1024 unchanged to common20 and full50/audit. Exact report:
vindr_a40_convnext_relational_cv5_first10_20260922.md.

A40 common CV5 first20 remains unchanged from first10: fold2 stays at
.5439920998 and keeps aggregate mean/SD/minimum at .7174048669/.1132044396/
.5439920998. Only the mean gate passes. Fold0 epoch20 itself remains strong
at .8078927073, while other trajectories decay. Continue all folds unchanged
to full50/audit; do not tune on fold2. Exact report:
vindr_a40_convnext_relational_cv5_first20_20260922.md.

A40 common CV5 first30 is again unchanged: mean .7174048669 passes, but SD
.1132044396 and minimum .5439920998 fail. Fold2 has not improved its epoch3
selection in 27 epochs. Fold0 remains strong even at epoch30 (.7864934019),
showing highly fold-specific dynamics. Continue unchanged to full50/audit.
Exact report: vindr_a40_convnext_relational_cv5_first30_20260922.md.

A40 common CV5 first40 incorporates fold3's epoch34 improvement and reaches
mean .7196907017, but SD .1124297521 and minimum .5439920998 still fail.
Fold2 has not improved for 37 epochs; replacing only the backbone is not
repairing stability. Finish50 and audit before formal rejection. Exact report:
vindr_a40_convnext_relational_cv5_first40_20260922.md.

A40 completed CV5 and all five audits PASS. Fold scores are .8212558177/
.8126870715/.5439920998/.6936746863/.7268438333; mean .7196907017 passes,
but sample SD .1124297521 and minimum .5439920998 fail. Reject A40 as the
stable solution. ConvNeXt raises mean/accuracy/QWK over A30 but exposes severe
fold-dependent optimization, especially fold2. Next test a major hybrid
representation/fusion change rather than another scalar tweak. Exact report:
vindr_a40_convnext_relational_cv5_results_20260922.md.

A41 hybrid relational-spatial fusion is preregistered conditionally, not
launched. It preserves A40's ConvNeXt global relational path and adds a
64-token regional cross-view Transformer as a learnable residual initialized
at weight .1. It has 32,367,980 parameters. Tests pass 37/37, strict checkpoint
roundtrip passes, and the unchanged A40 path is matched-seed bit-exact across
snapshots. Real RTX5090 cache preflight is required before folds1/3. Exact
report: vindr_a41_convnext_hybrid_spatial_preregistration_20260922.md.

A41's first preflight invocation stopped before loading a batch because the
copied snapshot contained local cache paths. The split directory was replaced
with the byte-identical frozen A40 cluster manifests and assignment SHA
43daa869... was restored. The actual real-cache preflight then PASSed on
master RTX5090: finite forward/loss/backward/clipping/update, two AMP skips,
and 2.647 GiB peak memory. A41 is cleared for folds1/3 only. Exact report:
vindr_a41_convnext_hybrid_spatial_preflight_20260922.md.

A41 launched as job1031 on fixed folds1/3 only. Both tasks run on master
RTX5090; worker2/Vesta is not used. W&B IDs are fold1 o1khepub and fold3
jms2mbgl. Do not expand before full50, both audits and both numerical gates.
Exact report: vindr_a41_convnext_hybrid_spatial_launch_20260922.md.

A41 common first10 selects fold1 .8213746277 at epoch9 and fold3 .7170961423
at epoch7, mean .7692353850, sample SD .0737360242 and minimum .7170961423.
Both early numerical gates pass, and A41 improves both folds over matched A40;
the gains include B/D rather than only rare class A. Epoch10 itself decays to
.540341/.555444, so continue unchanged to common20 and full50/audit; do not
expand yet. Exact report: vindr_a41_convnext_hybrid_spatial_first10_20260922.md.

A41 common first20 improves fold1 to .8321319993 at epoch16 while fold3 stays
.7170961423 at epoch7, giving mean .7746140708, sample SD .0813426346 and
minimum .7170961423. Both numerical gates remain met and fold1's gain includes
B/C/D plus accuracy/QWK. Epoch20 itself decays to .508200/.515502. Continue
unchanged to full50/audit; do not expand yet. Exact report:
vindr_a41_convnext_hybrid_spatial_first20_20260922.md.

A41 common first30 remains unchanged: fold1 .8321319993 at epoch16 and fold3
.7170961423 at epoch7, mean .7746140708, sample SD .0813426346 and minimum
.7170961423. Both screen gates pass, but epoch30 decays to .527979/.555369.
Continue unchanged to full50/audit; do not expand early. Exact report:
vindr_a41_convnext_hybrid_spatial_first30_20260922.md.

A41 completed50 and both audits PASS. Fold1 selects .8321319993 at epoch16
and fold3 .7170961423 at epoch7, mean .7746140708, sample SD .0813426346 and
minimum .7170961423. Both registered expansion gates pass. Preserve these
screen runs and launch only folds0/2/4 from the same immutable snapshot/config;
final CV5 stability remains unproven. Exact report:
vindr_a41_convnext_hybrid_spatial_twofold_final_20260922.md.

A41 expanded as job1033 on folds0/2/4 only, preserving job1031 folds1/3.
Folds0/2 run on master RTX5090 and fold4 on worker1 RTX5090; no task uses
worker2/Vesta. W&B IDs are twd1bi2e, f12x7ilg and ysfrdx6l. Final CV5 remains
pending full50 and all audits. Exact report:
vindr_a41_convnext_hybrid_spatial_cv5_expansion_launch_20260922.md.

A41 common CV5 first10 selects folds0--4 at .8280128668/.8213746277/
.5583275293/.7170961423/.7598495569. Mean .7369321446 passes, but sample SD
.1098231696 and minimum .5583275293 fail because fold2 remains the bottleneck.
Fold2 is slightly better than matched A40 and has higher D F1, but still
misses its single A case. Continue job1033 unchanged to common20/full50; do
not tune on fold2. Exact report:
vindr_a41_convnext_hybrid_spatial_cv5_first10_20260922.md.

A41 common CV5 first20 improves fold4 to .7897866700 at epoch19, raising mean
to .7450710415; SD .1141426504 and minimum .5583275293 still fail because
fold2 remains unchanged at epoch3. Continue full50/audit without fold-specific
tuning. Exact report: vindr_a41_convnext_hybrid_spatial_cv5_first20_20260922.md.

A41 common CV5 first30 improves fold4 to .8146311433 at epoch30 and reaches
mean .7500399362, but SD .1170788722 and minimum .5583275293 still fail.
Fold2 remains unchanged at epoch3. Finish50 and audit without fold-specific
tuning. Exact report: vindr_a41_convnext_hybrid_spatial_cv5_first30_20260922.md.

A41 completed CV5 and all five audits PASS. Fold scores are .8280128668/
.8321319993/.5583275293/.7170961423/.8259769927; mean .7523091061 exceeds
the stretch target, but SD .1187418588 and minimum .5583275293 fail. Reject
A41 as the stable solution. A40/A41 have zero fold2 A F1 in all 50 epochs,
whereas A30 has positive A F1 in 47/50; A41 fold2 B/C/D mean is already
.744437. Next isolate a hierarchical A-vs-rest primary head while retaining
A41 representation. Exact report:
vindr_a41_convnext_hybrid_spatial_cv5_results_20260922.md.

A42 hierarchical A-gate is preregistered conditionally, not launched. It
retains all A41 representation/training and factorizes only the primary head
into A-vs-rest plus conditional B/C/D, producing one normalized differentiable
four-class distribution. Parameter count stays 32,367,980. Tests pass 40/40,
strict roundtrip passes and the unchanged A41 flat path is bit-exact. Real
RTX5090 cache preflight is required before fixed folds1/3. Exact report:
vindr_a42_agate_head_preregistration_20260922.md.

A42 real-cache preflight PASS on master RTX5090 with batch shape
[2,4,3,512,512]. Forward/loss/backward/clipping/update were finite, AMP
recovered after two skipped updates, and peak memory was 2.647 GiB. The
pre-clipping gradient norm 39.79 was finite and handled by the registered
clip. A42 is cleared for folds1/3 only. Exact report:
vindr_a42_agate_head_preflight_20260922.md.

Goal scope revised again at the user's request: large changes to the complete
encoder--fusion--head architecture are now the default when justified, not a
fallback after more small repairs. The active scientific gates remain audited
CV5 mean >=.70, sample SD <=.05 and minimum >=.65, with a .75 stretch target,
single-model inference, frozen data protocol, seed42 and RTX5090-only compute.
A41 is the mean reference (.7523091) and A30 is the stability reference. Based
on the latest audited CV5, future major candidates after the already-running
A42 control screen on the current two weakest folds, fold2/fold3, before CV5
expansion. Full details and ordered architecture families are in
goal_major_architecture_search_revision_20260922.md.

A42 launched as job1037 on folds1/3 from its immutable snapshot. Both tasks
run on master RTX5090; W&B IDs are 5lsfvwi2 and jglym8l6. The first formal
comparison remains at common epoch10 or later. Exact report:
vindr_a42_agate_head_launch_20260922.md.

A43 is preregistered as the first full fusion-interface replacement under the
expanded goal. It removes PairFusion, product/difference relations and the
bilateral side gate, replacing them with a learned two-scale four-view token
Transformer with explicit view, laterality, scale and spatial embeddings. It
retains A42's normalized A-gate head to isolate the fusion redesign. The new
weak-fold protocol screens fold2/fold3 after RTX5090 real-cache preflight.
Remote unit tests pass 44/44; launch is not yet authorized. Exact report:
vindr_a43_multiscale_view_transformer_preregistration_20260922.md.

A43 real-cache preflight PASSed on worker1 RTX5090: architecture v10,
29,906,793 parameters, finite loss 1.676529, finite pre-clip gradient norm
20.974478, two AMP skips before recovery, 2.640089 GiB peak memory, strict
roundtrip error zero and 44/44 unit tests PASS. The initial job1039 failed
before model execution only because TORCH_HOME was absent; job1040 used the
registered launcher cache path and passed without a model/config change.
Exact report: vindr_a43_multiscale_view_transformer_preflight_20260922.md.

A43 launched as job1041 on current weak folds2/3 from the immutable v1
snapshot. Both run on worker1 RTX5090; worker2/Vesta is unused. W&B IDs are
hw6b2q8i and 0cojka4k. Do not expand before full50, both audits and the
two-fold mean/minimum gates. Exact report:
vindr_a43_multiscale_view_transformer_launch_20260922.md.

A42 common first10 selects fold1 .5803329 at epoch5 and fold3 .7385653 at
epoch7; mean .6594491, sample SD .1118872, minimum .5803329. It misses both
screen numerical gates and trails A41 at the same horizon, largely because
fold1 A F1 is zero. Continue the registered full50/audits; do not expand.
Exact report: vindr_a42_agate_head_first10_20260922.md.

A43 post-launch gradient audit confirms finite nonzero gradients through both
ConvNeXt scales, both projections, all semantic embeddings, the exam token and
both primary-head branches. The runtime model has no PairFusion, side gate or
bilateral module. This verifies the registered arm is a substantive active
architecture replacement, not a dormant auxiliary path.

Added `scripts/summarize_density_horizon.py` plus focused tests to make interim
two-fold comparisons reproducible. It accepts either training logs or final
history JSON, enforces complete common horizons, selects DEV Macro-F1 only
within that horizon, and computes mean/sample-SD/minimum plus the registered
screen gates. Focused tests pass 2/2. Future epoch20/50 reports must use this
tool rather than ad-hoc manual aggregation.

Rare-class sensitivity audit: frozen DEV folds contain A counts 1/1/1/2/1.
Holding all A41 outputs except fold2 A F1 fixed, A F1=.6667 would raise fold2
to .724994 and repair the minimum, but CV5 SD would still be .059077. Only
fold2 A F1=1.0 yields SD .048497 and passes the .05 gate. Keep the gate, but
always separate this one-case contribution from B/C/D, accuracy and QWK; a
gate pass alone is not evidence of robust A generalization. Exact report:
vindr_rare_a_stability_sensitivity_20260922.md.

A42 common first20 selects fold1 .7615292 at epoch19 and fold3 .7385653 at
epoch7; mean .7500472, sample SD .0162380, minimum .7385653. Both numerical
screen gates provisionally pass after first10 failed. However, the combined
selected B/C/D mean is .7222852 versus A41's matched .7550412; fold1 B/D and
QWK regress while its one A reaches F1=1.0. Continue full50/audit and do not
expand early. Exact report: vindr_a42_agate_head_first20_20260922.md.

A43 common first10 selects both fold2/fold3 at epoch7 with .7994428/.6785630;
mean .7390029, sample SD .0854750, minimum .6785630. The registered mean and
minimum screen gates pass provisionally, and this is the first ConvNeXt arm to
recover fold2 A. But combined B/C/D mean is .7075594 versus A41 .7391713 on
the same folds; fold3 D/QWK regress. Continue full50/audits and do not expand
early. Exact report: vindr_a43_multiscale_view_transformer_first10_20260922.md.

Primary-literature review supports a possible next family if A43 cannot
recover substantive B/C/D performance: hierarchical local attention within
each view followed by global attention over four view summaries, with small
view-specific adapters rather than fully unshared encoders. This is a major
inductive-bias change from A43's immediate 80-token global attention. It is an
evidence note only; do not implement or launch before A43 full50/audits. Exact
note and primary-source links: next_major_architecture_evidence_20260922.md.

The common-horizon summarizer now also computes aggregate accuracy, QWK,
per-class F1 means and B/C/D F1 mean. This makes the rare-A sensitivity check
part of every reproducible horizon result rather than a separate manual
calculation.

A42 common first30 is unchanged from first20: fold1/fold3 .7615292/.7385653,
mean .7500472, SD .0162380, minimum .7385653, B/C/D mean .7222852. Epoch30
itself falls to .5581752/.5452214 with A F1 zero in both folds. Continue50 and
audit; no early expansion. Exact report: vindr_a42_agate_head_first30_20260922.md.

A43 common first20 is unchanged from first10: fold2/fold3 .7994428/.6785630,
mean .7390029, SD .0854750, minimum .6785630, B/C/D mean .7075594. Epoch20
itself falls to .5243444/.5365968 with A F1 zero in both folds. The current
gain remains transient and A-driven; continue50/audit without expansion.
Exact report: vindr_a43_multiscale_view_transformer_first20_20260922.md.

Rare-A persistence across common horizons separates the two new arms. A42 has
positive A F1 in only 1/30 fold1 epochs and 4/30 fold3 epochs. A43 has positive
A F1 in 10/20 fold2 epochs and 4/20 fold3 epochs; A40/A41 fold2 had 0/50.
Therefore A43 genuinely repairs the fold2 A decision region, although maximum
streak is three epochs and B/C/D/QWK still regress. Exact report:
vindr_a42_a43_a_region_persistence_20260922.md.

A42 common first40 remains unchanged since first20: mean .7500472, SD
.0162380, minimum .7385653 and B/C/D mean .7222852. Epoch40 falls to
.5402210/.5000093 with A F1 zero in both folds. Finish50/audit; no early
expansion. Exact report: vindr_a42_agate_head_first40_20260922.md.

A43 common first30 improves fold3 at epoch30 to .7152517 while fold2 retains
.7994428 at epoch7. Mean .7573472, SD .0595321, minimum .7152517, QWK
.6614393 and B/C/D mean .7320185. It now preserves nearly all A41 B/C/D on
these folds while repairing fold2 A, so the gain is no longer merely A-only.
Finish50 and both audits before expansion. Exact report:
vindr_a43_multiscale_view_transformer_first30_20260922.md.

A42 completed50 on folds1/3 and both audits PASS. Selected scores
.7615292/.7385653 give mean .7500472, SD .0162380 and minimum .7385653; both
registered expansion gates pass despite weaker B/C/D mean .7222852. Preserve
these screen folds and expand only 0/2/4. Exact report:
vindr_a42_agate_head_twofold_final_20260922.md.

A42 expanded as job1043 on folds0/2/4 from the same immutable snapshot.
Folds0/2 run on master RTX5090 and fold4 on worker1 RTX5090; worker2/Vesta is
unused. W&B IDs are k5fx8np4, dla18fu9 and jnslnq8i. Final CV5 remains pending
full50 and all audits. Exact report:
vindr_a42_agate_head_cv5_expansion_launch_20260922.md.

A43 common first40 improves fold3 to .7199629 at epoch35; fold2 stays
.7994428. Mean .7597029, SD .0562008, minimum .7199629, QWK .6684805 and
B/C/D mean .7351594, now within .0040 of A41 on these folds while repairing
fold2 A. Finish50/audit before expansion. Exact report:
vindr_a43_multiscale_view_transformer_first40_20260922.md.

A43 completed50 on weak folds2/3 and both audits PASS. Selected scores are
.7994428/.7199629, mean .7597029, SD .0562008, minimum .7199629, QWK
.6684805 and B/C/D mean .7351594. Both registered expansion gates pass and
the gain combines fold2 A recovery with near-A41 B/C/D. Exact report:
vindr_a43_multiscale_view_transformer_twofold_final_20260922.md.

A43 expanded as job1046 on folds0/1/4 from the same immutable snapshot,
preserving job1041 folds2/3. All tasks run on worker1 RTX5090; worker2/Vesta is
unused. W&B IDs are dpwsopx7, gacylkw6 and as0dj0qb. Final CV5 remains pending
full50 and all audits. Exact report:
vindr_a43_multiscale_view_transformer_cv5_expansion_launch_20260922.md.

A42 common CV5 first10 selects folds0--4 at .8243696/.5803329/.6061748/
.7385653/.7945236. Mean .7087932 passes, but SD .1102572 and minimum
.5803329 fail. B/C/D mean remains strong at .7406132. Fold2 now has A F1=.4
but three A false positives; fold1 is horizon-limited and later improved in
its completed screen. Continue common20/full50 without tuning. Exact report:
vindr_a42_agate_head_cv5_first10_20260922.md.

A42 common CV5 first20 reaches mean .7450325 after fold1's epoch19 gain, but
SD .0841712 and minimum .6061748 still fail; fold2 remains unchanged at
epoch8. B/C/D mean is .7222656. Continue full50/audit without tuning. Exact
report: vindr_a42_agate_head_cv5_first20_20260922.md.

A43 common CV5 first10 selects folds0--4 at .8160008/.5850244/.7994428/
.6785630/.5835890. Mean .6925240, SD .1121339 and minimum .5835890 all fail;
folds1/4 are the early bottlenecks and B/C/D mean is .7100320. The preserved
fold3 improved only at epoch35, so continue common20/full50 unchanged. Exact
report: vindr_a43_multiscale_view_transformer_cv5_first10_20260922.md.

A42 common CV5 first30 improves fold2 to .6773145 at epoch25. Aggregate mean
.7592604 and minimum .6773145 pass; SD .0561945 is only .0061945 above the
final gate. B/C/D mean is .7234584. This is the closest arm to all final CV5
criteria, but remains unaccepted pending full50/five audits. Exact report:
vindr_a42_agate_head_cv5_first30_20260922.md.

A43 common CV5 first20 is unchanged from first10: mean .6925240, SD .1121339,
minimum .5835890 and B/C/D mean .7100320. Folds1/4 remain the bottlenecks.
Continue full50 unchanged because the completed screen improved late. Exact
report: vindr_a43_multiscale_view_transformer_cv5_first20_20260922.md.

A43 common CV5 first30 improves folds3/4 to .7152517/.7188252 while fold1
remains .5850244. Aggregate mean .7269090 passes, but SD .0915573 and minimum
.5850244 fail; B/C/D mean is .7336564. Continue full50/audit without tuning.
Exact report:
vindr_a43_multiscale_view_transformer_cv5_first30_20260922.md.

A42 common CV5 first40 is unchanged from first30: mean .7592604, SD .0561945,
minimum .6773145 and B/C/D mean .7234584. Mean/minimum pass, but SD remains
.0061945 above the final gate. Finish epoch50 and audit all folds before any
claim. Exact report: vindr_a42_agate_head_cv5_first40_20260922.md.

A42 expansion folds0/2 completed50 and audit PASS including finished W&B.
Selected scores .8243696/.6773145 fall to .5035518/.5331754 at epoch50,
with A F1 zero. Fold4 remains RUNNING at43; A43 folds0/1/4 RUNNING at35.
CV5 audit allowlist now recognizes v7--v10; full verification is pending.
Exact report: vindr_a42_expansion_partial_audit_20260922.md.

A42 now provably cannot meet the SD gate: folds0--3 are final, and fold4's
existing best .7945236 exceeds the fixed-four mean .7504447. Its best-DEV
score cannot decrease; feasible minimum final sample SD is .0561945. Finish
and audit fold4, but reject A42 for final stability. Updated CV5 auditor
also passed end-to-end on completed A41 and reproduced its existing metrics.
Exact report: vindr_a42_final_sd_lower_bound_20260922.md.

Late-A history diagnostic: A42 folds0--3 have zero A-positive epochs in
31--50. A43 improves persistence on some folds but fold1 remains positive
only once through40. This is case-level sensitivity with six A exams, not
proof of a causal loss/backbone defect. Exact snapshot:
vindr_a42_a43_late_a_persistence_20260922.md.

A43 common40: mean .7392163, sample SD .0935366, min .5850244, B/C/D
.7278439. Fold4 improves to .7756505 at35 through A recovery while its
accuracy/QWK decline. Fold1 remains weak. Continue registered50/audit.
Exact report: vindr_a43_multiscale_view_transformer_cv5_first40_20260922.md.

A42 full50 CV5 audit PASS. Final selected-DEV mean .7592604, sample SD
.0561945, min .6773145; stability gate FAIL. Epoch50 mean .5202418.
Raw audit saved as vindr_a42_cv5_audit_20260922.json; W&B audited summary
8niae7gz published and synced with target_met_single_seed=false.
Final report: vindr_a42_agate_head_cv5_final_20260922.md.

Active goal tightened to mean>=.72 and sample SD<=.03, preserving the
minimum .65 and user's major-architecture authorization. New candidates
screen one fold first per latest goal. A43 completed50; CV5 audit PASS,
mean .7392163, SD .0935366, minimum .5850244: rejected. W&B summary
bfcspx52 published with new thresholds. A44 local-global fusion registered
before implementation, screening weakest A43 fold1. Exact reports:
vindr_a43_multiscale_view_transformer_cv5_final_20260922.md and
vindr_a44_local_global_fusion_preregistration_20260922.md.

A44 v11 implemented: local/global four-view Transformer with view/side
adapters.50 local CPU tests PASS, synthetic512 forward PASS,31,553,769
parameters. Configuration isolation verified. Remote source transfer rejected
by automatic approval review; no A44 GPU preflight or training submitted.
Await explicit approval for source transfer to Atlas. Exact report:
vindr_a44_implementation_validation_20260922.md.

User approved exact Atlas deployment; source transfer succeeded and hashes
match. Four A44 tests PASS remotely. Real-cache RTX5090 AMP preflight1049
PASS (loss1.22838, grad12.0919, zero skipped updates,2.652GiB). Fold1
screen1050_1 RUNNING on master RTX5090, seed42/full50, W&B2031sdoy.
Vesta excluded. Exact report: vindr_a44_local_global_launch_20260922.md.

A44 fold1 first10: best epoch4 Macro-F1 .5418260 vs matched A43 .5850244;
B/C/D mean .7224347 vs .7133659, but QWK .6321601 vs .6936710 and A F1
zero for10/10 epochs. Screen gates not met; keep registered50 unchanged,
no expansion. Exact report: vindr_a44_local_global_first10_20260922.md.

A44 fold1 first20: epoch19 reaches Macro-F1 .7641792 through its sole
A-positive epoch, but B/C/D mean .6855723 and QWK .5916055 both regress
against A43 and fail registered secondary gates. Epoch20 falls to .4949260
with A F1 zero. No CV5 expansion; finish50/audit unchanged. Exact report:
vindr_a44_local_global_first20_20260922.md.

A44 first40 remains selected epoch19 at .7641792; B/C/D .6855723 and
QWK .5916055 still fail preservation gates. A positive only1/40 epochs;
epoch40 Macro-F1 .5219888, A F1 zero. Finish50/audit; no expansion.
Exact report: vindr_a44_local_global_first40_20260922.md.

A44 fold1 completed50 and audit PASS. Selected epoch19 Macro-F1 .7641792,
but B/C/D .6855723 and QWK .5916055 fail preregistered preservation gates;
only1/50 epochs has positive A F1. Epoch50 Macro-F1 .5256756. Reject A44
and do not expand. Exact report: vindr_a44_local_global_final_20260922.md.

A45 v12 implemented locally per preregistration: one shared training-only
four-class head supervises each local view summary at focal-loss weight .25;
the single exam head remains the sole inference output. All59 repository
tests PASS, focused A44/A45 tests10/10 PASS, and production-shape512 forward
PASS. A seed-controlled test proves every parameter shared with A44 starts
bit-identically, avoiding an initialization confound. Deployment to the new
immutable Atlas destination was rejected pending explicit
destination-specific approval; no A45 code, preflight, or training job was
submitted. Exact report:
vindr_a45_implementation_validation_20260922.md.

User explicitly authorized the new Atlas destination. A45 was deployed to an
immutable snapshot; source hashes and ten focused tests match remotely.
Preflight1051 failed only in the new shell launcher before model/data access;
the corrected launcher passed syntax checks and replacement real-cache AMP
preflight1052 PASS on RTX5090. Fold1 job1053_1 was observed RUNNING on the
master RTX5090 with fixed split/seed42/full50, worker2/Vesta excluded, and
W&B run1k59zmph. No quality claim or fold expansion before the registered
10--20 epoch milestone and completed50 audit. Exact report:
vindr_a45_per_view_auxiliary_launch_20260922.md.

A45 fold1 matched first10 selects epoch4 at Macro-F1 .5472873, accuracy
.8089330, QWK .6438009 and B/C/D mean .7297163, with zero A-positive epochs.
It modestly improves A44's matched Macro-F1/QWK/B-C-D values but remains
below A43 Macro-F1 .5850244 and fails the Macro-F1/QWK screen gates. View
auxiliary loss decreases from .0671709 to .0104573; this confirms the added
head is optimized, not that exam-level generalization is improved. Job1053_1
continues unchanged to50; no fold expansion. Exact report:
vindr_a45_per_view_auxiliary_first10_20260922.md.

A45 fold1 matched first20 selects boundary epoch20 at Macro-F1 .5572461,
accuracy .8486352, QWK .6671180 and B/C/D mean .7429949, with zero positive-A
epochs. Common-class performance and QWK materially exceed A44's matched
selected checkpoint, but A45 fails Macro-F1/QWK gates and remains below A43
on both metrics because it never recovers the single A case. Continue
unchanged to40/50; no tuning or fold expansion. Exact report:
vindr_a45_per_view_auxiliary_first20_20260922.md.

A45 first40 remains selected epoch20 at Macro-F1 .5572461, accuracy .8486352,
QWK .6671180 and B/C/D mean .7429949. There are zero positive-A epochs and
zero epochs at Macro-F1>=.72. Training/view auxiliary losses continue to fall
but DEV selection plateaus, so A45 passes only the B/C/D gate. Finish50 and
audit; no tuning or fold expansion. Exact report:
vindr_a45_per_view_auxiliary_first40_20260922.md.

A45 fold1 completed50 and audit PASS. Selected epoch20 Macro-F1 .5572461,
accuracy .8486352, QWK .6671180 and B/C/D mean .7429949. Zero of50 epochs
has positive A F1 or Macro-F1>=.72. A45 passes only the B/C/D gate and fails
Macro-F1/QWK gates; reject without CV5 expansion. Exact report:
vindr_a45_per_view_auxiliary_final_20260922.md.

Post-A45 gate diagnostic: A43/A44/A45 each classify all5 FIT A cases correctly;
A44/A45 also classify all157 FIT B as B. A45 is most saturated on FIT
(P(A)>=.999999 for every A) but maps the sole DEV A to B with P(A)=.000170.
This is rare-case memorization/generalization failure, not insufficient A
gradient. Mask/intensity statistics place the DEV A farther from the FIT-A
centroid than FIT-B and outside FIT-A ranges for several brightness measures,
so a raw radiomics branch is rejected before training. Exact report:
vindr_a45_rare_a_generalization_diagnostic_20260922.md.

A46 preregistered from A45 with one treatment group: training-only,
exam-consistent feature MixStyle after the ConvNeXt fine stage (probability
.5, Beta alpha .1, non-identity exam pairing). It targets the observed
style/generalization failure while leaving inference single-path and
parameter count unchanged. Fixed fold1/full50/seed42/cache and
Macro/B-C-D/QWK expansion gates remain unchanged. Implementation pending.
Exact report: vindr_a46_exam_mixstyle_preregistration_20260922.md.

A46 v13 implemented locally per preregistration. The parameter-free
exam-consistent MixStyle layer is inserted after ConvNeXt's fine stage and is
disabled exactly for evaluation/inference. All65 repository tests and 16/16
focused A44--A46 tests PASS; synthetic production-shape512 inference PASS;
parameter count remains31,554,797. A46 differs from A45 only in arm name,
MixStyle probability.5 and Beta alpha.1. Deployment and real-cache RTX5090
AMP preflight pending. Exact report:
vindr_a46_implementation_validation_20260922.md.

A46 deployed to immutable Atlas snapshot
hcmus-density-localglobal-perviewaux-mixstyle-20260922-v1 with matching hashes
and 16/16 focused tests PASS. Real-cache AMP preflight job1056 PASS on RTX5090
(batch2x4x3x512x512, peak2.6990GiB, two normal scaler recovery skips).
Fold1-only full50 job1057_1 launched on slurm-b20a-master-0/RTX5090, no Vesta;
W&B run2rzbst10. No other fold is running and expansion remains gate-locked.
Exact report: vindr_a46_exam_mixstyle_launch_20260922.md.

A46 fold1 matched first10 selects epoch8 at Macro-F1 .5321024, accuracy
.8387097, QWK .6145924, B/C/D mean .7094699 and F1
[0,.6849315,.9,.5434783]. There are zero positive-A epochs and zero epochs at
Macro-F1>=.72. A46 trails A45 first10 Macro by .0151848 and A43 by .0529220;
all three expansion gates currently fail. Continue the preregistered full50
unchanged and do not expand or retune from this interim DEV result. Exact
report: vindr_a46_exam_mixstyle_first10_20260922.md.

A46 fold1 matched first20 selects epoch15 at Macro-F1 .5464094, accuracy
.8312655, QWK .6426932, B/C/D mean .7285459 and F1
[0,.7058824,.8935484,.5862069]. There are zero positive-A epochs and zero
epochs at Macro-F1>=.72. A46 trails A45 first20 Macro by .0108367 and passes
only the B/C/D preservation gate; Macro/QWK gates fail. Continue full50
unchanged, no expansion or interim retuning. Exact report:
vindr_a46_exam_mixstyle_first20_20260922.md.

A46 fold1 matched first40 selects epoch25 at Macro-F1 .5475739, accuracy
.8610422, QWK .6585366, B/C/D mean .7300985 and F1
[0,.6764706,.9185868,.5952381]. No epoch has positive-A F1 or
Macro-F1>=.72. The selected Macro improves only .0011645 beyond first20 and
trails A45 first40 by .0096723; A46 still passes only the B/C/D gate. Finish
full50 unchanged, then audit; no expansion or interim retuning. Exact report:
vindr_a46_exam_mixstyle_first40_20260922.md.

A46 fold1 completed50 and read-only audit PASS, including all frozen manifests,
assignment SHA, v13 provenance, predictions, probability normalization and
finished W&B run. Selected epoch25 Macro-F1 .5475739, accuracy .8610422, QWK
.6585366, B/C/D mean .7300985, F1 [0,.6764706,.9185868,.5952381]. Zero/50
epochs have positive A F1 or Macro-F1>=.72. A46 passes only the B/C/D gate and
fails Macro/QWK; reject without CV5 expansion. MixStyle improves accuracy but
does not solve rare-A generalization. Exact report:
vindr_a46_exam_mixstyle_final_20260922.md.

A47 preregistered from A42, the closest audited CV5 candidate, rather than
continuing the rejected A43--A46 branch. It keeps A42's ConvNeXt hybrid
relational/spatial representation and successful A gate, but replaces the
conditional B/C/D head with a D-vs-(B/C) endpoint gate plus a conditional B/C
head. Parameter count and single-path inference remain unchanged. Screen the
two lowest A42 folds2/3 only; require each Macro>=.72, two-fold sampleSD<=.03,
and preservation of registered B/C/D and QWK mean/min before folds0/1/4.
Exact report: vindr_a47_dual_endpoint_gate_preregistration_20260922.md.

A47 v14 implemented locally per preregistration. It reinterprets A42's
existing three B/C/D projection outputs as D gate plus B/C conditional logits,
so A42/A47 state keys, seed42 initialization and parameter count32,367,980 are
identical. All70 repository tests and 10/10 focused A41/A42/A47 tests PASS;
production-shape512 inference and normalized probabilities PASS. Config differs
from A42 only in arm and primary-head name. Deployment/preflight pending.
Exact report: vindr_a47_implementation_validation_20260922.md.

A47 deployed to immutable Atlas snapshot hcmus-density-dual-endpoint-gate-
20260922-v1 with matching hashes and 10/10 focused tests PASS. Real-cache AMP
preflight job1060 PASS on RTX5090 (batch2x4x3x512x512, peak2.6942GiB, finite
grad norm10.54596, one scaler recovery skip). Preregistered fold2/3 full50
array1061_2--3 launched on master RTX5090, no Vesta. W&B runs109017w9 and
zja66x7p. Folds0/1/4 remain gate-locked. Exact report:
vindr_a47_dual_endpoint_gate_launch_20260922.md.

A47 matched first10 on folds2/3: selected Macro .6535918/.7029314 versus A42
.6061748/.7385653. Two-fold mean improves .0058916, sampleSD drops .0587258 to
.0348884 and minimum improves .0474170, but B/C/D mean declines .0088112 and
QWK mean declines .0133324. Both Macro scores remain below.72 and SD remains
above.03, so expansion gates fail at this horizon. Continue unchanged to
20/40/50; folds0/1/4 remain locked. Exact report:
vindr_a47_dual_endpoint_gate_first10_20260922.md.

A47 matched first20 is unchanged from first10: folds2/3 select epoch3/5 at
Macro .6535918/.7029314, two-fold mean .6782616, sampleSD .0348884 and minimum
.6535918. Fold3 has one additional positive-A epoch13 but no selected-score
gain. Both Macro scores, SD, B/C/D mean and QWK mean gates still fail. Continue
unchanged to40/50; folds0/1/4 remain locked. Exact report:
vindr_a47_dual_endpoint_gate_first20_20260922.md.

A47 matched first40 remains selected at fold2 epoch3 .6535918 and fold3
epoch5 .7029314; mean .6782616, sampleSD .0348884, min .6535918. A42 matched
first40 is .6773145/.7385653, mean .7079399, SD .0433108. A47 narrows spread
but loses mean/min and B/C/D/QWK means; no selected improvement after epoch5
and both epoch40 A F1 are zero. All expansion gates fail. Finish50/audit; keep
folds0/1/4 locked. Exact report:
vindr_a47_dual_endpoint_gate_first40_20260922.md.

A47 folds2/3 completed50 and both local read-only audits PASS for split SHA,
v14 provenance, histories, checkpoints, predictions, probability normalization
and recomputed metrics. Training logs show both W&B runs finished syncing;
external W&B API was not called by the safer local audit. Final selected Macro
.6535918/.7029314 gives mean .6782616, sampleSD .0348884, min .6535918;
B/C/D mean .7099044 and QWK mean .6444421. Both per-fold Macro gates, SD,
B/C/D-mean and QWK-mean gates fail. Reject A47; do not launch folds0/1/4.
Exact report: vindr_a47_dual_endpoint_gate_twofold_final_20260922.md.

A48 preregistered from A42 after A47 showed that output-only D factorization
trades fold2 D improvement for fold3 B/D regression. A48 restores A42's exact
A-gate plus conditional B/C/D head and adds a dedicated fine-scale 384-channel
four-view spatial-attention expert whose zero-initialized scalar adjusts only
the D logit. Shared A42 initialization and initial output must be bit-exact;
single-model inference only. Screen fixed folds2/3 with the same Macro/SD,
B/C/D and QWK gates before any expansion. Exact report:
vindr_a48_fine_d_expert_preregistration_20260922.md.

A48 implementation validation passes locally: 76/76 complete tests, 14/14
focused A42/A47/A48 tests, clean diff check and finite production-shape 512x512
inference. A42/A48 shared state and complete initial outputs are bit-exact;
the treatment adds 1,784,321 parameters and its upstream fine branch receives
gradient after the zero-initialized D projection's first update. Atlas snapshot
hashes match and focused tests pass 14/14 with the registered `.deps` path.
Real-cache RTX5090 preflight remains required before training. Exact report:
vindr_a48_implementation_validation_20260922.md.

A48 real-cache preflight job1065 passes on NVIDIA RTX5090 with production
batch `[2,4,3,512,512]`: finite forward/loss, backward, clipped gradients and
optimizer update under AMP; peak allocation 2.719 GiB. Two-fold training is
ready but not yet submitted because aggregate-only W&B upload requires
explicit payload-and-destination approval. No training result exists yet.

A48 two-fold screen launched as Slurm array job1066 tasks2-3 after creating an
immutable offline-only receipt snapshot. Both tasks run on RTX5090 and exclude
Vesta. Treatment/protocol are unchanged; W&B mode alone is offline, with local
run IDs qai5n15b/3ppb7vks, so no payload is uploaded. Folds0/1/4 remain locked
until final local audits and every preregistered gate pass. Exact receipt:
vindr_a48_fine_d_expert_launch_20260922.md.

A48 matched first10 selects fold2 epoch3 Macro .5400831 and fold3 epoch6
.7383681. Against A42's matched first10, B/C/D mean improves .0224741 to
.7411897 and QWK mean improves .0065967 to .6643712; fold2 D F1 improves
.0484848 and fold3 is essentially preserved. But fold2 has zero A-positive
epochs, causing Macro mean to fall .0331444 to .6392256 and sampleSD to rise
.0465945 to .1402087. Continue unchanged to20/40/50; no tuning and folds0/1/4
remain locked. Exact report: vindr_a48_fine_d_expert_first10_20260922.md.

A48 matched first20 is unchanged from first10: selected epochs3/6 yield Macro
.5400831/.7383681, mean .6392256, sampleSD .1402087 and minimum .5400831.
B/C/D and QWK gates pass, but fold2 has zero A-positive epochs out of20 and
therefore fails the per-fold Macro gate; SD also fails by .1102087. Continue
unchanged to40/50 with folds0/1/4 locked. Exact report:
vindr_a48_fine_d_expert_first20_20260922.md.

A48 matched first40 remains selected at epochs3/6 with Macro
.5400831/.7383681, mean .6392256, sampleSD .1402087 and minimum .5400831.
Against A42 first40, fold2 D F1 improves .0877005 and all B/C/D/QWK gates
pass, but fold2 has zero A-positive epochs out of40 versus A42 recovery at
epoch25. Macro mean is .0687143 lower and sampleSD .0968978 higher than A42.
Finish50/audit; folds0/1/4 remain locked. Exact report:
vindr_a48_fine_d_expert_first40_20260923.md.

A48 folds2/3 completed50 and both local audits PASS. Final selected epochs3/6
remain Macro .5400831/.7383681, mean .6392256, sampleSD .1402087 and minimum
.5400831. B/C/D and QWK gates pass, but fold2 Macro and SD fail; reject without
folds0/1/4. A post-run diagnostic proves construction and fine-branch forward
advance the global RNG relative to A42 despite exact shared weights/initial
outputs, confounding later dropout trajectories. Exact report:
vindr_a48_fine_d_expert_twofold_final_20260923.md.

A49 preregistered as an exact A48 repeat with CPU RNG restoration around
treatment construction and CPU/CUDA RNG forking around the fine-D forward.
It must prove construction/forward RNG parity with A42 before the same fixed
fold2/3 50-epoch screen and unchanged expansion gates. Architecture v16;
single model, no ensemble or calibration. Exact report:
vindr_a49_rng_isolated_fine_d_preregistration_20260923.md.

A49 local implementation validation passes: 77/77 complete tests and 15/15
focused tests. At production 512x512, shared A42/A49 state, initial train-mode
outputs, construction RNG and post-forward RNG are all bit-exact; outputs are
finite and normalized. The treatment still receives gradient. Config differs
from A48 only by arm name and RNG-isolation flag. Atlas deployment/preflight
remain pending. Exact report:
vindr_a49_implementation_validation_20260923.md.

A49 Atlas hashes match local, focused tests pass 15/15, and immutable snapshot
`hcmus-density-rngisolated-fine-d-20260923-v1` is read-only. Real-cache
preflight job1068 passes on RTX5090 at production shape with finite loss,
backward and optimizer update. Two-fold screen job1069 tasks2-3 then launched
for 50 epochs each on RTX5090 with Vesta excluded and W&B offline IDs
7msbizh4/7mch95l6. Folds0/1/4 stay locked. Exact launch report:
vindr_a49_rng_isolated_fine_d_launch_20260923.md.

A49 CUDA parity audit job1072 passes on RTX5090: shared state, construction CPU
RNG, post-forward CPU/CUDA RNG and every initial output tensor are bit-exact
against A42 under matched seeds; the fine-D head gradient is finite/non-zero.
Diagnostic job1071 had first stopped only because its loss weights were on CPU;
the corrected audit moved that diagnostic object to CUDA, with no model or
training change. Evidence is recorded in the A49 implementation report.

A49 matched first10 selects fold2 epoch5 Macro .6062836 and fold3 epoch7
.7112440, mean .6587638, sampleSD .0742182, minimum .6062836. Relative to A48,
fold2 recovers .0662005 and SD falls .0659904; rare-A positive-epoch counts
return exactly to A42's 1/10 and 4/10. Relative to A42, mean is still .0136062
lower and B/C/D mean .0070309 lower because fold3 regresses. No final gate is
claimed; continue unchanged to20/40/50 with folds0/1/4 locked. Exact report:
vindr_a49_rng_isolated_fine_d_first10_20260923.md.

A49 matched first20 is unchanged from first10: selected epochs5/7 give Macro
.6062836/.7112440, mean .6587638, sampleSD .0742182 and minimum .6062836.
Neither fold has any epoch >=.72. RNG isolation preserves A42-like A-positive
counts (1/20 and 4/20) and improves A48's SD, but fold3 B/C/D regression leaves
mean, B/C/D and QWK below A42. Finish40/50 and audit; folds0/1/4 remain locked.
Exact report: vindr_a49_rng_isolated_fine_d_first20_20260923.md.

A50 preregistered before A49 final inspection as A42 plus zero-initialized
projection-specific 384-channel CC/MLO residual adapters before the shared
upper ConvNeXt stage. It targets encoder negative transfer after A43--A49
exhausted token fusion, per-view supervision, MixStyle and D-specific heads.
A50 is locked until A49 finishes/audits; then it must prove bit-exact A42
initialization/RNG and pass the unchanged folds2/3 gates before expansion.
Architecture v17; single model, no ensemble. Exact report:
vindr_a50_projection_adapters_preregistration_20260923.md.

A49 matched first40 remains selected at epochs5/7: Macro .6062836/.7112440,
mean .6587638, sampleSD .0742182 and minimum .6062836. Neither fold has any
epoch >=.72. Against matched A42, mean is .0491761 lower, minimum .0710309
lower, B/C/D mean .0100126 lower and QWK mean .0118243 lower; only B/C/D and
QWK minima improve. Finish50 and queued audits1073/1074; folds0/1/4 remain
locked. Exact report: vindr_a49_rng_isolated_fine_d_first40_20260923.md.

A49 folds2/3 complete50 and audit jobs1073/1074 both PASS with empty errors.
Final selected epochs5/7 remain Macro .6062836/.7112440, mean .6587638,
sampleSD .0742182 and minimum .6062836. Both Macro gates, SD, B/C/D mean and
QWK mean fail; B/C/D and QWK minima pass. Reject A49 without folds0/1/4.
RNG control is validated but the learned fine-D treatment is not beneficial.
A50 implementation is now unlocked, with training still locked pending its
registered validation/preflight. Exact report:
vindr_a49_rng_isolated_fine_d_twofold_final_20260923.md.

A50 projection-adapter implementation validation passes: local complete tests
82/82, focused tests 20/20 locally and on Atlas, production 512 outputs finite,
and A42/A50 shared state, initial outputs and CPU/CUDA RNG streams bit-exact.
CUDA parity job1076 passes on RTX5090; real-cache preflight job1077 passes with
finite loss/gradient and 2.7185 GiB peak allocation. A50 adds 149,952 parameters
over A42. The folds2/3 screen is unlocked; folds0/1/4 remain locked. Exact
report: vindr_a50_implementation_validation_20260923.md.

A50 matched first10 selects fold2 epoch4 Macro .5391099 and fold3 epoch3 Macro
.6981955: mean .6186527, sampleSD .1124905 and minimum .5391099. Neither fold
reaches .72. Fold2 has zero A-positive epochs; fold3 has 4/10, but the signal
vanishes after epoch7. Non-zero CC/MLO adapter projection norms confirm that
the new path is learning, while the current generalization is worse than the
matched A42/A49 control. Continue unchanged to20/40/50; folds0/1/4 remain
locked. Exact report: vindr_a50_projection_adapters_first10_20260923.md.

A51 is preregistered after A50 first10 but before first20/final inspection. It
retains A42 and adds a zero-initialized orientation-aligned bilateral spatial
relation residual: right maps are flipped, CC/MLO pairs use symmetric mean,
absolute-difference and product maps, and one shared spatial block feeds the
exam feature. A 100-exam label-free cache audit confirms opposing L/R CC
orientation. A51 is a single model and remains locked until A50 completes and
audits. Exact report:
vindr_a51_bilateral_spatial_relation_preregistration_20260923.md.

A50 matched first20 is unchanged from first10: selected epochs4/3 give Macro
.5391099/.6981955, mean .6186527, sampleSD .1124905 and minimum .5391099.
Fold2 remains 0/20 A-positive; fold3 is 5/20 with longest streak three. Neither
fold has an epoch >=.72, while epoch20 itself is .5032574/.6734800. Continue
unchanged to40/50 and audits; folds0/1/4 remain locked. A51 was preregistered
before this inspection. Exact report:
vindr_a50_projection_adapters_first20_20260923.md.

A50 matched first40 moves fold3 to epoch40 Macro .7268970, the first A50 epoch
above .72, with B/C/D .7469738 and QWK .6814056. Fold2 remains selected at
epoch4 Macro .5391099 with zero A-positive epochs. Aggregate mean is .6330034,
sampleSD .1327855 and minimum .5391099; fold2 Macro, SD and QWK mean gates
fail despite passing B/C/D gates. Continue unchanged to50 and queued audits;
folds0/1/4 remain locked. Exact report:
vindr_a50_projection_adapters_first40_20260923.md.

A50 folds2/3 complete50 and read-only audits1080/1081 both PASS. Selected
epochs4/40 give Macro .5391099/.7268970, mean .6330034, sampleSD .1327855 and
minimum .5391099. Fold2 Macro, SD and QWK mean gates fail; B/C/D mean/minimum
and QWK minimum pass. Reject A50 without folds0/1/4. Projection adapters help
fold3 late but worsen fold sensitivity and never recover fold2 A. A51
implementation is now unlocked, with training locked pending validation and
real-cache preflight. Exact report:
vindr_a50_projection_adapters_twofold_final_20260923.md.

A51 local implementation validation passes: syntax, focused tests 25/25,
complete tests 87/87, bit-exact A42 state/initial output/RNG, staged gradients,
side symmetry, strict roundtrip and finite production 512 forward. It adds
987,648 parameters to A42. Atlas payload transfer is awaiting explicit user
authorization; no remote validation or training has been claimed. Exact
report: vindr_a51_local_implementation_validation_20260923.md.

A51 Atlas deployment is now authorized and validated. Registered hashes match,
remote focused tests pass 25/25, CUDA parity job1082 and real-cache preflight
job1083 both PASS on RTX5090 with worker2/Vesta excluded. The read-only
snapshot then launched the fixed fold2/3 full50 screen as array job1084, W&B
offline IDs 5hzj03pt/oeauqr5m. Audits1086/1087 wait on afterok:1084;
folds0/1/4 stay locked until all registered two-fold gates pass. Exact receipt:
vindr_a51_bilateral_spatial_relation_launch_20260923.md.

A51 matched first10 selects epoch7 on both folds: Macro .6155977/.7281705,
mean .6718841, sampleSD .0796010 and minimum .6155977. Versus matched A42 it
slightly raises fold2 and lowers fold3, leaving mean effectively unchanged but
narrowing spread. Fold2/fold3 have 1/10 and 5/10 positive-A epochs; the
zero-initialized bilateral output projection is non-zero in both checkpoints.
Fold2 Macro, SD, B/C/D mean and QWK mean gates currently fail. Continue
unchanged to20/40/50; folds0/1/4 remain locked. Exact report:
vindr_a51_bilateral_spatial_relation_first10_20260923.md.

A51 matched first20 remains selected at epoch7 on both folds with Macro
.6155977/.7281705, mean .6718841, sampleSD .0796010 and minimum .6155977.
Fold3 accumulates 8/20 positive-A and 3/20 Macro>=.72 epochs, but fold2 remains
at one isolated positive-A epoch and no epoch>=.72. Fold2 Macro, SD, B/C/D mean
and QWK mean gates still fail. Continue unchanged to40/50; folds0/1/4 remain
locked. Exact report:
vindr_a51_bilateral_spatial_relation_first20_20260923.md.

A52 is conditionally preregistered after A51 first20 and before its
first40/final inspection. It is a major single-model change that preserves the
complete A42 hybrid path and adds A43's multi-scale four-view Transformer only
as a zero-initialized residual expert for the A-vs-rest logit. B/C/D, ordinal
and binary predictions stay on A42. Construction/forward RNG must remain
bit-exact and the fixed folds2/3 gates are unchanged. Training stays locked
behind completed audited A51 rejection. Exact report:
vindr_a52_multiscale_a_expert_preregistration_20260923.md.

A52 local implementation is validation-complete: syntax, focused tests30/30,
full tests92/92, bit-exact A42 shared state/initial output/CPU RNG, staged
expert gradients, strict roundtrip and finite production512 forward all PASS.
The expert changes only the A gate and adds2,082,049 parameters. Config delta
is arm, treatment flag and offline W&B only. Atlas/CUDA/preflight/training stay
locked behind completed audited A51 rejection. Exact report:
vindr_a52_local_implementation_validation_20260923.md.

A51 matched first40 improves fold3 at epoch40 to .7404835, while fold2 remains
epoch7 .6155977 with only one isolated positive-A epoch. Aggregate mean is
.6780406, sampleSD .0883076 and minimum .6155977. B/C/D and QWK mean/minimum
gates now pass, but fold2 Macro and SD fail decisively; the bilateral branch
helps the stronger fold more. Finish50 and queued audits1086/1087, with
folds0/1/4 locked. A52 was preregistered before this inspection. Exact report:
vindr_a51_bilateral_spatial_relation_first40_20260923.md.

A51 folds2/3 complete50 and audit jobs1086/1087 both PASS. Final selected
epochs7/40 give Macro .6155977/.7404835, mean .6780406, sampleSD .0883076 and
minimum .6155977. B/C/D and QWK mean/minimum pass, but fold2 Macro and SD fail.
Reject A51 without folds0/1/4: its learned bilateral branch amplifies the
stronger fold and leaves only one isolated positive-A epoch on fold2. Audited
rejection unlocks A52 Atlas/CUDA/preflight validation, not training. Exact
report: vindr_a51_bilateral_spatial_relation_twofold_final_20260923.md.

A52 Atlas hashes match, remote focused tests pass30/30, CUDA parity job1088
and real-cache preflight job1089 PASS on RTX5090 with worker2/Vesta excluded.
The read-only snapshot launched fixed folds2/3 as full50 array job1090, W&B
offline IDs o8i8cjx5/q6zqr8i4; first updates are finite. Audits1092/1093 wait
on afterok:1090. Folds0/1/4 remain gate-locked. Exact receipt:
vindr_a52_multiscale_a_expert_launch_20260923.md.

A52 matched first10 selects epoch7 on both folds at Macro .6034620/.7180493,
mean .6607556, sampleSD .0810255 and minimum .6034620. The expert output head
is non-zero, but fold2 still has one isolated positive-A epoch and neither fold
reaches .72. Both scores trail matched A42; Macro, SD, B/C/D mean/min and QWK
mean gates currently fail. Continue unchanged to20/40/50; folds0/1/4 remain
locked. Exact report: vindr_a52_multiscale_a_expert_first10_20260923.md.

A52 matched first20 improves fold3 at epoch19 to .7305408, while fold2 stays
epoch7 .6034620 with one isolated positive-A epoch. Mean is .6670014,
sampleSD .0898583 and minimum .6034620; the mean gain and expert-norm growth
occur only on the stronger fold. Fold2 Macro, SD, B/C/D mean/min and QWK mean
gates fail. Continue unchanged to40/50 and audits; folds0/1/4 remain locked.
Exact report: vindr_a52_multiscale_a_expert_first20_20260923.md.

A53 is conditionally preregistered after A52 first20 and before first40/final.
It replaces, rather than residually adjusts, the A-gate input with A43's
multi-scale four-view representation, while A42 remains the sole source for
B/C/D, ordinal and binary heads. One shared backbone and one normalized output
keep it a single model. Training is locked behind audited A52 rejection; fixed
fold2/3 gates are unchanged. Exact report:
vindr_a53_multiscale_a_replacement_preregistration_20260923.md.

A53 local implementation passes syntax, focused tests34/34, full tests96/96,
bit-exact A42 shared state/construction and post-forward RNG, exact initial
ordinal/binary and conditional B/C/D outputs, intentional A-output change,
first-step gradients through A gate/multi-scale Transformer, strict roundtrip
and production512 forward. It adds2,081,280 parameters. Atlas/CUDA/preflight
and training remain locked behind audited A52 rejection. Exact report:
vindr_a53_local_implementation_validation_20260923.md.

A52 matched first40 remains epoch7/19 at Macro .6034620/.7305408, mean
.6670014, sampleSD .0898583 and minimum .6034620. Fold2 stays at one isolated
positive-A epoch and zero epochs>=.72; fold3 adds only one positive-A epoch
after first20. The learned residual expert does not repair the weak fold.
Finish50 and audits1092/1093; folds0/1/4 remain locked. A53 was preregistered
before this inspection. Exact report:
vindr_a52_multiscale_a_expert_first40_20260923.md.
