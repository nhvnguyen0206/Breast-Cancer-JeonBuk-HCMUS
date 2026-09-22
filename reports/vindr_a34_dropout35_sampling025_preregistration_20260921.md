# A34 preregistration: interpolate dropout between A6 and A30

Parent A6. Change only model dropout from 0.30 to 0.35 and arm metadata.
Retain sampling power 0.25, augmentation, optimizer, all losses, cache, seed
42, frozen grouped split, DenseNet121/hierarchical fusion, and single
flat-head inference. No ensemble.

Rationale: A6 is the strongest completed stability reference (mean 0.676551,
SD 0.064446, minimum 0.619496). Raising dropout to 0.40 in A30 raised the
mean to 0.709931 while narrowly missing the SD and minimum gates. Dropout
0.45 in A32 was too strong and degraded mean and dispersion. A34 tests the
unmeasured midpoint 0.35 as a bounded interpolation; it does not assume a
monotonic response and it introduces no structural change.

Clone immutable A6 and verify exact semantic delta, source/script/split byte
parity, assignment digest, and snapshot tests. Run fixed fold 0 for all 50
epochs on RTX 5090, excluding worker2/Vesta. Expand folds 1–4 only after a
completed screen audit PASS with selected DEV Macro-F1 >=0.70, preserving
fold 0. Final acceptance remains mean >=0.70, sample SD <=0.05, and minimum
fold >=0.65. Selected DEV is not independent-test evidence; six total
class-A studies limit inference.

## Deployment preflight

Immutable A6 was cloned to
`/slurmshared/Ngoc/code/hcmus-density-auggeo-dropout35-sampling025-20260921-v1`.
The parsed configuration delta contains exactly arm metadata and dropout
0.30 -> 0.35. `src/`, `scripts/`, and the frozen split are byte-identical to
A6; assignment SHA256 remains
`43daa86936ee7b1bae1b200836fb1afdfe0c8294c7c865d8f5758bf989f12a9a`;
16/16 snapshot tests passed. Config SHA256:
`b28bc4cc4d34017ba0f26f85478a637a27eb92ff353147bc95d33a5ddddfd9e7`.

Submitted fold 0 only as job `997_0`. Startup verification: RUNNING on
`slurm-b20a-master-0`, allocated GPU `NVIDIA GeForce RTX 5090`, no
restart/requeue, and worker2/Vesta excluded. W&B:
https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/6bhg258e
