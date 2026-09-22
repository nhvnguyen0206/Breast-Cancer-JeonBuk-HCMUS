# A18 fixed-BatchNorm screen — numerical failure

A18 was preregistered as A5 plus fixed DenseNet BatchNorm running statistics,
with the A5 mixed-precision training contract otherwise unchanged. Fold0 job
932 started on master with an RTX 5090, worker2/Vesta excluded, Requeue0 and
Restarts0, but failed before completing epoch1 with a non-finite loss. The
failed W&B run is `zdit2tcj`.

Three no-W&B diagnostic reproductions used the same seed42 data order,
augmentation, model initialization, optimizer, loss and AMP path. Every run
reproduced the failure at batch150. Before that forward pass:

- The input tensor was finite, range `[-2.1179039478, 2.2351434231]`.
- All model parameters were finite.
- Initial AMP gradient overflows were correctly skipped while GradScaler
  reduced its scale from 65536 to 2048.
- The last sampled checkpoint at batch100 had finite loss 0.6119199395 and
  finite logits.

At batch150, all three head outputs and all four loss components became NaN
under autocast. Re-running the same finite input and same finite model state
with autocast disabled produced finite outputs and total loss 1.7531044483.
This identifies mixed-precision activation overflow under fixed BatchNorm
statistics, rather than corrupt input, non-finite parameters or scheduler
failure.

A18 is rejected as numerically incompatible with the fixed A5 AMP contract.
It has no valid DEV score and folds1--4 must not be launched. Disabling AMP or
forcing the backbone to FP32 would introduce a second treatment and confound
the intended one-factor comparison; that variant is not silently substituted.
The temporary diagnostic script was removed after collecting this evidence.

W&B failed run:
https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/zdit2tcj
