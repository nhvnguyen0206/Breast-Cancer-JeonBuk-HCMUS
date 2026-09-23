# A53 multiscale A-gate replacement: two-fold launch

A53 passed every preregistered implementation and execution check before
training. The read-only snapshot is
`/slurmshared/Ngoc/code/hcmus-density-multiscale-a-replacement-20260923-v1`;
registered hashes match and focused remote tests pass 34/34. CUDA parity job
`1094` and real-cache preflight job `1095` completed with exit `0:0` on
RTX5090 with worker2/Vesta excluded.

The fixed fold2/3 full50 screen was launched as Slurm array job `1096`:

- tasks `1096_2` and `1096_3` run on the Atlas master RTX5090;
- outputs are `/slurmshared/Ngoc/runs/hcmus-density-cv5-v1-1096-fold2`
  and `/slurmshared/Ngoc/runs/hcmus-density-cv5-v1-1096-fold3`;
- split seed42 and assignment SHA256
  `43daa86936ee7b1bae1b200836fb1afdfe0c8294c7c865d8f5758bf989f12a9a`
  remain frozen;
- architecture is `convnext_tiny_hybrid_bcd_multiscale_a_gate_v20`;
- W&B remains offline in `TN_Mammo_BreastDensity/HCMUS-paper1`, local IDs
  `6irwuqqa` (fold2) and `82som6u1` (fold3); no cloud URL/upload is claimed;
- the first update is finite on both folds and records the intended config.

Read-only audits `1098`/`1099` wait on `afterok:1096`. Folds0/1/4 remain
locked. Interim inspection is limited to epoch10/20/40/50 and cannot retune the
running experiment.
