# A43 CV5 expansion launch

A43 expanded as Slurm array job `1046` on folds 0, 1 and 4 only, preserving
completed job-1041 folds 2 and 3. All three tasks run on worker1 RTX 5090.
Worker2/Vesta is excluded and unused.

| Fold | W&B ID | W&B URL |
|---:|---|---|
| 0 | `dpwsopx7` | https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/dpwsopx7 |
| 1 | `gacylkw6` | https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/gacylkw6 |
| 4 | `as0dj0qb` | https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/as0dj0qb |

All tasks use the same immutable v1 snapshot, config, seed 42 and frozen
assignment SHA256 as the weak-fold screen. Final acceptance requires all five
audits PASS, CV5 mean >= `0.70`, sample SD <= `0.05` and minimum fold >=
`0.65`. Report at common 10--20 epoch horizons or completion only.
