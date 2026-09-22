# A51 bilateral spatial relation: two-fold launch

A51 passed every preregistered implementation and execution check before
training. The source/config snapshot
`/slurmshared/Ngoc/code/hcmus-density-bilateral-relation-20260923-v1` is
read-only, its registered file hashes match local, and its focused remote tests
pass 25/25. CUDA parity job `1082` and real-cache preflight job `1083` both
completed with exit `0:0` on `NVIDIA GeForce RTX 5090`, with worker2/Vesta
excluded.

The fixed fold2/3 screen was launched as Slurm array job `1084` for 50 epochs:

- tasks `1084_2` and `1084_3` run on the Atlas master RTX5090;
- outputs are `/slurmshared/Ngoc/runs/hcmus-density-cv5-v1-1084-fold2`
  and `/slurmshared/Ngoc/runs/hcmus-density-cv5-v1-1084-fold3`;
- frozen split seed is 42 and assignment SHA256 is
  `43daa86936ee7b1bae1b200836fb1afdfe0c8294c7c865d8f5758bf989f12a9a`;
- architecture is
  `convnext_tiny_hybrid_spatial_a_gate_bilateral_relation_v18`;
- W&B remains offline in project `TN_Mammo_BreastDensity/HCMUS-paper1`, with
  local run IDs `5hzj03pt` (fold2) and `oeauqr5m` (fold3); no cloud URL or
  external metric upload is claimed;
- first completed updates report the intended configuration and finite metrics
  on both folds.

Read-only audits `1086` (fold2) and `1087` (fold3) are queued with
`afterok:1084`. Folds0/1/4 remain locked. They may be opened only if both
audits PASS and every preregistered Macro-F1, sample-SD, B/C/D and QWK gate
passes. Interim inspection is limited to the registered epoch10/20/40/50
milestones and cannot change this run.
