# A48 fine-scale D expert launch receipt

A48 passed implementation validation and real-cache RTX5090 preflight job
1065. The registered two-fold screen was submitted as Slurm array job 1066,
tasks 2 and 3, for exactly 50 epochs each. Both tasks started on
`slurm-b20a-master-0` and explicitly reported `NVIDIA GeForce RTX 5090`; the
launcher excludes `slurm-b40a-worker-2` (Vesta).

Immutable execution snapshot:
`/slurmshared/Ngoc/code/hcmus-density-fine-d-expert-offline-20260922-v1`.
Training outputs:

- fold2: `/slurmshared/Ngoc/runs/hcmus-density-cv5-v1-1066-fold2`
- fold3: `/slurmshared/Ngoc/runs/hcmus-density-cv5-v1-1066-fold3`

The model, split, cache, seed42, optimizer, losses, sampling and all registered
gates are unchanged from the preregistration. The only difference from the
online receipt config is `wandb.mode: offline`. W&B data remains local on Atlas
until explicit upload approval; no medical image, case identifier,
per-patient prediction or checkpoint is queued for upload. Local offline run
IDs are `qai5n15b` (fold2) and `3ppb7vks` (fold3).

This is a selected-DEV screen, not an independent test. Folds0/1/4 remain
locked unless every preregistered two-fold expansion gate passes after both
50-epoch runs and local audits complete.
