# A35 preregistration: stronger neighbor-cost loss on A30

Parent A30. Change only `loss.neighbor` from 0.20 to 0.30 and arm metadata.
Retain dropout 0.40, sampling power 0.25, augmentation, optimizer, all other
losses, cache, seed 42, frozen grouped split, DenseNet121/hierarchical fusion,
and single flat-head inference. No ensemble.

Rationale: A30 remains closest to final acceptance (mean 0.709931, SD
0.051267, minimum 0.640275), but D recognition is weak, especially D->C
errors. The neighbor cost assigns a cost of 3 to D->C, so a modest increase
directly tests stronger ordinal-distance pressure without changing the model.
A33's decrease to 0.10 worsened mean and dispersion; this supports testing the
opposite direction but does not guarantee improvement.

Apply the revised fixed two-fold stress screen: run folds 1 and 3, historically
the two lowest folds across completed arms, for all 50 epochs from one
immutable snapshot/config on RTX 5090 with worker2/Vesta excluded. Expand to
folds 0, 2 and 4 only if both audits PASS, their two-fold mean Macro-F1 is
>=0.70, and neither fold is below 0.65. Retain screen runs during expansion.
Final acceptance remains audited CV5 mean >=0.70, sample SD <=0.05 and minimum
>=0.65. Selected DEV is not independent-test evidence.

## Deployment preflight

Immutable A30 was cloned to
`/slurmshared/Ngoc/code/hcmus-density-auggeo-dropout40-sampling025-neighbor030-20260921-v1`.
The parsed configuration delta contains exactly arm metadata and neighbor
loss 0.20 -> 0.30. `src/`, `scripts/`, and the frozen split are byte-identical
to A30; assignment SHA256 remains
`43daa86936ee7b1bae1b200836fb1afdfe0c8294c7c865d8f5758bf989f12a9a`;
16/16 snapshot tests passed. Config SHA256:
`9b1f671b63dab1840ea44d2ed87547e74e12006517f2c5245725b32b61699147`.

Submitted only folds 1 and 3 as array job `1002_[1,3]`. Both tasks started on
`slurm-b20a-master-0`, allocated `NVIDIA GeForce RTX 5090`, with no
restart/requeue and worker2/Vesta excluded. W&B:

- fold 1: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/ksdm0x9c
- fold 3: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/jytyd5ja
