# A17: mild weighted sampling on A5

Only training change from A5: use weighted case sampling with power 0.10
instead of natural sampling. Architecture, preprocessing, augmentation,
dropout, optimizer, losses, split and seed remain unchanged.

A6 showed that sampling power 0.25 reduced the five-fold Macro-F1 sample SD
from 0.11729 to 0.06445, but also reduced mean Macro-F1 from 0.70283 to
0.67655. A17 tests a smaller, preregistered interpolation intended to retain
more of A5's mean while applying a weaker stability pressure. This outcome is
uncertain and is not assumed.

Same stretch512 cache input, fixed grouped split and seed42 as A5. Fixed fold0
only, fresh ImageNet initialization, full50. Only a completed audited selected
DEV Macro-F1 >=.75 permits fresh folds1--4 while retaining fold0. No ensemble,
resplit or independent-test claim. RTX5090 only; worker2/Vesta excluded. Final
joint criteria remain mean>=.70, sample SD<=.05 and minimum fold>=.65.

Immutable deployment target:
`/slurmshared/Ngoc/code/hcmus-density-auggeo-dropout30-sampling010-20260920-v1`.
Config SHA256:
`2740940652db1870ac9aa5570916561b163ceb6ab7bedd6d9e4870f7e5a688dd`.
Cluster preflight passes 22/22 tests, validates all five frozen fold manifests,
and reads a finite real FIT tensor with shape `[4,3,512,512]`. Parsed config
differs from A5 only by arm identity and `sampling_power: 0.10`. For fold0 FIT
counts `[5,156,1245,207]`, the registered sampler's expected class draw
probabilities are `[0.0051266920,0.1133904192,0.7352188594,0.1462640294]`
across exactly 1613 replacement draws per epoch.

Submitted fixed fold0 only as job907_0. Startup is verified RUNNING on
`slurm-b20a-master-0` with `NVIDIA GeForce RTX 5090`; worker2/Vesta is
excluded and no-requeue is active. Output is
`/slurmshared/Ngoc/runs/hcmus-density-cv5-v1-907-fold0`.
W&B source run: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/djz4e32c
