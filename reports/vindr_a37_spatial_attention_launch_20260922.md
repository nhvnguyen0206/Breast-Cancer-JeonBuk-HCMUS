# A37 spatial-token attention two-fold launch

A37 launched only the fixed stress folds 1 and 3 as Slurm array job 1011
after A36 completed/audited and the A37 real-cache preflight passed.

- Fold 1: W&B run `jr97gvza`
- Fold 3: W&B run `q6fj2umt`
- Node/GPU: `slurm-b20a-master-0`, NVIDIA GeForce RTX 5090
- Vesta/worker2: excluded
- Requeue/restarts: disabled / zero at launch
- Epochs/seed: 50 / 42
- Frozen assignment SHA256:
  `43daa86936ee7b1bae1b200836fb1afdfe0c8294c7c865d8f5758bf989f12a9a`

Do not launch folds 0/2/4 unless both screen audits PASS, the two-fold mean
Macro-F1 is >=0.70 and neither fold is below 0.65. Report only at common
10–20 epoch checkpoints.
