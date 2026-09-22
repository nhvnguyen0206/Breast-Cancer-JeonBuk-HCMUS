# A47 two-fold launch after real-cache preflight

The exact locally tested files were deployed to the new snapshot
`/slurmshared/Ngoc/code/hcmus-density-dual-endpoint-gate-20260922-v1`.
Remote hashes match the implementation report and all 10 focused A41/A42/A47
tests PASS in the deployed environment. The tested snapshot was made read-only.

RTX5090 preflight job 1060 PASSed with architecture
`convnext_tiny_hybrid_spatial_dual_endpoint_gate_multitask_v14`. One real
cached batch `[2,4,3,512,512]` completed AMP forward, backward and optimizer
update after one normal GradScaler recovery skip. Peak allocated GPU memory
was 2.6942 GiB and the finite pre-clipping gradient norm was 10.54596.

The preregistered two-lowest-fold screen was submitted as job array 1061_2--3.
Both tasks were observed RUNNING on `slurm-b20a-master-0`, each reporting an
NVIDIA GeForce RTX 5090. Worker2/Vesta is excluded. They use seed42, the
window16 cache, frozen assignment SHA256
`43daa86936ee7b1bae1b200836fb1afdfe0c8294c7c865d8f5758bf989f12a9a`
and 50/min50 epochs. Output directories are
`/slurmshared/Ngoc/runs/hcmus-density-cv5-v1-1061-fold2` and `...-fold3`.

W&B:

- fold2: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/109017w9
- fold3: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/zja66x7p

Folds 0/1/4 remain unlaunched and are gate-locked pending both completed
screen audits and every preregistered Macro-F1/SD/B-C-D/QWK gate.
