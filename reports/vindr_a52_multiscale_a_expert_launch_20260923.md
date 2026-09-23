# A52 multiscale A expert: two-fold launch

A52 passed every preregistered implementation and execution check before
training. The snapshot
`/slurmshared/Ngoc/code/hcmus-density-multiscale-a-expert-20260923-v1` is
read-only, registered hashes match local, and focused remote tests pass 30/30.
CUDA parity job `1088` and real-cache preflight job `1089` both completed with
exit `0:0` on `NVIDIA GeForce RTX 5090`, with worker2/Vesta excluded.

The fixed fold2/3 full50 screen was launched as Slurm array job `1090`:

- tasks `1090_2` and `1090_3` run on the Atlas master RTX5090;
- outputs are `/slurmshared/Ngoc/runs/hcmus-density-cv5-v1-1090-fold2`
  and `/slurmshared/Ngoc/runs/hcmus-density-cv5-v1-1090-fold3`;
- frozen split seed is 42 and assignment SHA256 is
  `43daa86936ee7b1bae1b200836fb1afdfe0c8294c7c865d8f5758bf989f12a9a`;
- architecture is
  `convnext_tiny_hybrid_spatial_a_gate_multiscale_a_expert_v19`;
- W&B remains offline in `TN_Mammo_BreastDensity/HCMUS-paper1`, with local
  run IDs `o8i8cjx5` (fold2) and `q6zqr8i4` (fold3); no cloud URL or upload is
  claimed;
- the first update is finite on both folds and records the intended config.

Read-only audits `1092` (fold2) and `1093` (fold3) are queued with
`afterok:1090`. Folds0/1/4 remain locked. Interim inspection is restricted to
epoch10/20/40/50, and the running configuration cannot be retuned.
