# A42 CV5 expansion launch

A42 expanded as Slurm array job `1043` on folds 0, 2 and 4 only, preserving
completed job-1037 folds 1 and 3. Folds 0/2 run on master RTX 5090 and fold 4
runs on worker1 RTX 5090. Worker2/Vesta is excluded and unused.

| Fold | W&B ID | W&B URL |
|---:|---|---|
| 0 | `k5fx8np4` | https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/k5fx8np4 |
| 2 | `dla18fu9` | https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/dla18fu9 |
| 4 | `jnslnq8i` | https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/jnslnq8i |

All tasks use the same immutable snapshot, config, seed 42 and assignment
SHA256 as the screen. Final acceptance still requires all five audits PASS,
CV5 mean >= `0.70`, sample SD <= `0.05` and minimum fold >= `0.65`. Report
only at common 10--20 epoch horizons or completion.
