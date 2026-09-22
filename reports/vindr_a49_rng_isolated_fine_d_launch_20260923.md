# A49 RNG-isolated fine-D launch receipt

A49 passed local and Atlas implementation validation plus real-cache RTX5090
preflight job 1068. The registered two-fold screen was submitted as Slurm array
job 1069, tasks 2 and 3, for exactly 50 epochs each. Both tasks started on
`slurm-b20a-master-0` and explicitly reported `NVIDIA GeForce RTX 5090`; the
launcher excludes `slurm-b40a-worker-2` (Vesta).

Immutable execution snapshot:
`/slurmshared/Ngoc/code/hcmus-density-rngisolated-fine-d-20260923-v1`.
Training outputs:

- fold2: `/slurmshared/Ngoc/runs/hcmus-density-cv5-v1-1069-fold2`
- fold3: `/slurmshared/Ngoc/runs/hcmus-density-cv5-v1-1069-fold3`

The model topology, split, cache, seed42, optimizer, losses, sampling and every
registered gate are unchanged from A48. The sole treatment change is RNG
isolation around construction and forward of the fine-D expert. W&B remains
offline; local run IDs are `7msbizh4` (fold2) and `7mch95l6` (fold3). No
medical image, case identifier, per-patient prediction or checkpoint has been
uploaded externally.

This is a selected-DEV screen, not an independent test. Folds0/1/4 remain
locked unless every preregistered two-fold expansion gate passes after both
50-epoch runs and local audits complete.
