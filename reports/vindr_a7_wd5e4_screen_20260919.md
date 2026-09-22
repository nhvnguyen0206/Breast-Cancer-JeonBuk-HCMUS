# A7 completed fold-0 screen

A7 changes only AdamW weight decay from 1e-4 to 5e-4 relative to A5. Shared
DenseNet121, hierarchical fusion, augmentation, dropout 0.3, loss, learning
rate, natural sampling, split and seed remain fixed. Inference uses one
flat-head checkpoint; no ensemble.

Job 780_0 completed 50 epochs with ExitCode 0 on slurm-b20a-master-0;
slurm-b40a-worker-2 was excluded and requeue was disabled. RTX 5090 startup
was verified. Full read-only screen audit PASS: architecture/config/provenance,
checkpoint selection, all five frozen manifests and assignment hash, exact
unique DEV membership and labels, finite normalized probabilities/argmax,
independently recomputed metrics and finished W&B metadata all agree.

Selected epoch 30 DEV Macro-F1 **0.7896498562**, accuracy 0.8267326733,
QWK 0.6486083499. Class F1 A/B/C/D =
[1.0, 0.6419753086, 0.8859934853, 0.6306306306]. Confusion matrix:
`[[1,0,0,0],[0,26,14,0],[0,15,272,24],[0,0,17,35]]`.
Five of 50 epochs reached .75. Epoch50 Macro-F1 was 0.5147925058.
AMP skipped-update total was 16; all logged scalar losses were finite.

This result is numerically identical to A5 fold0, despite the weight-decay
change. It passes the preregistered expansion gate but does not show a fold0
improvement. Fold0 contains only one A case, so it is not a success claim.
Proceed with fresh folds1--4 using the identical A7 snapshot and retain this
completed fold0. CV5 mean and multi-seed stability remain unverified; DEV is
not an independent test.

[W&B run](https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/k0rg6gfh)

