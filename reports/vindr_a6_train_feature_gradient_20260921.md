# FIT train-mode feature-gradient diagnostic

Ran scripts/audit_loss_feature_gradients.py --train-batches64 on A6
775-fold0 best checkpoint and original fold0 FIT manifest, RTX5090 asserted.
64 batches of2 from the seeded power.25 sampler, with configured augmentation,
dropout and train-mode BN. FP32 diagnostic, not an exact AMP training replay.
No optimizer step or checkpoint write; BN buffers change only in memory.
FIT counts [5,156,1245,207]. Initial diagnostic attempt failed on optional
attributes absent from immutable A6; corrected to validate config defaults.

Gradients measured at detached exam representation, not shared parameters.
Example C/C batch: focal norm .0129322, ordinal .1138014,
binary .0001930, neighbor .0186774. Example B/A batch: focal .9663268,
ordinal .1498866. Many confident batches have near-zero focal gradients.
Ordinal/focal directions in displayed records are often close to orthogonal,
not evidence of large systematic opposing gradients. Cosines involving tiny
norms are epsilon-sensitive and must not be interpreted as reliable angles.

This supports a loss-scale disparity at this representation/checkpoint,
but not a causal explanation of CV5 failures. It does not establish that
reducing ordinal weight improves generalization. Next use a matched control
and shared-parameter gradients before choosing an intervention; check existing
ordinal-weight arms to avoid repeating tested configurations.
