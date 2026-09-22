# A6 completed fold-0 screen

A6 changes only FIT sampling power from 0 to 0.25 relative to A5. Shared
DenseNet121, hierarchical fusion, augmentation, dropout 0.3, loss, learning
rate, split and seed remain fixed. Inference uses one flat-head checkpoint;
no ensemble.

Job 775_0 completed 50 epochs with ExitCode 0 on slurm-b20a-master-0;
slurm-b40a-worker-2 was excluded. RTX 5090 startup was verified. Full
read-only screen audit PASS: architecture/config/provenance, checkpoint
selection, all five frozen manifests and assignment hash, exact unique DEV
membership and labels, finite normalized probabilities/argmax, independently
recomputed metrics and finished W&B metadata all agree.

Selected epoch 4 DEV Macro-F1 **0.7829792575**, accuracy 0.8143564356,
QWK 0.6444663475. Class F1 A/B/C/D =
[1.0, 0.5957446809, 0.8756218905, 0.6605504587]. Confusion matrix:
`[[1,0,0,0],[0,28,12,0],[0,26,264,21],[0,0,16,36]]`.
Only one of 50 epochs reached .75. Epoch50 Macro-F1 was 0.5547746827.
AMP skipped-update total was 16; all logged scalar losses were finite.

This passes the preregistered numerical expansion gate but is slightly below
A5 fold0 (0.7896498562). Fold0 contains only one A case, so it is not a
success claim. Proceed with fresh folds1--4 using the identical snapshot;
retain this completed fold0. CV5 mean and multi-seed stability remain
unverified; DEV is not an independent test.

[W&B run](https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/qla23v5w)

