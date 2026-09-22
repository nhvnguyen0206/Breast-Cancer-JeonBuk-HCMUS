# A39 corrected ordinal-primary two-fold launch

A39 launched only fixed stress folds 1 and 3 as Slurm array job 1018 after
A38 completed/audited and A39's real-cache preflight passed.

- Fold 1: W&B `fzts4z74`
- Fold 3: W&B `1qqpu7sq`
- Node/GPU: `slurm-b20a-master-0`, NVIDIA GeForce RTX 5090
- Vesta/worker2: excluded
- Requeue/restarts: disabled / zero at launch
- Epochs/seed: 50 / 42
- Frozen assignment SHA256:
  `43daa86936ee7b1bae1b200836fb1afdfe0c8294c7c865d8f5758bf989f12a9a`

Do not launch folds 0/2/4 unless both screen audits PASS, mean Macro-F1 is
>=0.70 and neither fold is below 0.65. Compare A39 directly with A38 at common
10–20 epoch horizons to test the threshold-initialization correction.

