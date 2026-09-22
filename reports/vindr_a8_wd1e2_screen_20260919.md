# A8 completed fold-0 screen

A8 changes only AdamW weight decay from the numerically ineffective A5 value
1e-4 to 1e-2. Shared DenseNet121, hierarchical fusion, augmentation, dropout
0.3, losses, LR5e-5, natural sampling, split and seed remain fixed. Inference
uses one flat-head checkpoint; no ensemble.

Job785_0 completed50 with Slurm COMPLETED ExitCode=0:0 on master; worker2 was
excluded, requeue disabled, and RTX5090 startup verified. Full read-only audit
PASS: architecture/config/provenance, checkpoint selection, all five frozen
manifests/hash, exact DEV membership and labels, finite normalized
probabilities/argmax, independently recomputed metrics and finished W&B all
agree.

Selected epoch29 DEV Macro-F1 **0.8050193050**, accuracy 0.8514851485,
QWK 0.6726801340. Class F1 A/B/C/D =
[1.0, 0.6486486486, 0.9047619048, 0.6666666667]. Confusion matrix:
`[[1,0,0,0],[0,24,16,0],[0,10,285,16],[0,0,18,34]]`; no severe errors.
Twelve of 50 epochs reached .75. Epoch50 Macro-F1 was 0.5284265251.

A8 is 1.5369 percentage points above A5 fold0 and passes the preregistered
numeric expansion gate. This is not a success claim: fold0 contains one A
case, CV5/multiseed remain unverified, and DEV is not an independent test.
Proceed with fresh folds1--4 from the identical snapshot and retain this fold0.

[W&B run](https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/s9v0d7rc)

