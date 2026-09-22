# A36 view-token attention two-fold launch

A36 launched only the fixed stress-screen folds 1 and 3 as Slurm array job
1007 after its preregistration, 17/17 tests, strict checkpoint roundtrip, and
real cached-batch RTX 5090 preflight passed.

- Fold 1: W&B run `v4vdj0ig`
- Fold 3: W&B run `7be8i6ku`
- Node: `slurm-b20a-master-0`, NVIDIA GeForce RTX 5090
- Vesta/worker2: excluded
- Requeue/restarts: disabled / zero at launch
- Epochs: 50; seed: 42
- Frozen assignment SHA256:
  `43daa86936ee7b1bae1b200836fb1afdfe0c8294c7c865d8f5758bf989f12a9a`

Do not launch folds 0/2/4 unless both completed screen audits PASS, the mean
of folds 1/3 is >=0.70, and neither fold is below 0.65. Report at common
10- or 20-epoch checkpoints rather than every epoch.

