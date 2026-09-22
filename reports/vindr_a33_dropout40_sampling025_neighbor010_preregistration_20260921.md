# A33 preregistration: lower neighbor penalty on A30

Parent A30. Change only `loss.neighbor` from 0.20 to 0.10 and arm metadata.
Retain dropout 0.40, sampling power 0.25, augmentation, optimizer, all other
losses, cache, seed 42, frozen grouped split, DenseNet121/hierarchical fusion,
and single flat-head inference. No ensemble.

Rationale: A30 is the closest completed arm to acceptance (mean 0.709931,
SD 0.051267, minimum 0.640275), while its mean D F1 is only 0.561837. A25
tested neighbor 0.10 on A5 and obtained fold-0 D F1 0.693069 and QWK
0.663698, but did not test the A30 sampling/dropout interaction. A33 tests
whether less adjacent-class penalty improves D separation without removing
the head. This prior is limited to one DEV fold and is not a guarantee.

Clone immutable A30 and verify exact semantic delta, source/script/split byte
parity, assignment digest, and snapshot tests. Run fixed fold 0 for all 50
epochs on RTX 5090, excluding worker2/Vesta. Expand folds 1–4 only after a
completed screen audit PASS with selected DEV Macro-F1 >=0.70, preserving
the original fold 0. Final acceptance remains mean >=0.70, sample SD <=0.05,
and minimum >=0.65. Selected DEV is not independent-test evidence; six total
class-A cases limit inference.

## Deployment preflight

Immutable A30 was cloned to
`/slurmshared/Ngoc/code/hcmus-density-auggeo-dropout40-sampling025-neighbor010-20260921-v1`.
The parsed config delta contains exactly arm metadata and neighbor loss
0.20 -> 0.10. `src/` and `scripts/` are byte-identical to A30; assignment
SHA256 remains
`43daa86936ee7b1bae1b200836fb1afdfe0c8294c7c865d8f5758bf989f12a9a`;
16/16 snapshot tests passed. Config SHA256:
`58f741e825a652106285a459c526605a99dc935fb6531ab4dc03341188b47be8`.

Submitted fold 0 only as job `992_0`. Startup verification: RUNNING on
`slurm-b20a-master-0`, allocated GPU `NVIDIA GeForce RTX 5090`, no
restart/requeue, and worker2/Vesta excluded. W&B:
https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/x6422mve
