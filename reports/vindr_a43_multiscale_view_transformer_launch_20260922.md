# A43 multi-scale four-view Transformer launch

A43 launched as Slurm array job `1041` on the newly registered current weak
folds 2 and 3. Both tasks are running on `slurm-b40a-worker-1`; both logs
identify `NVIDIA GeForce RTX 5090`. Worker2/Vesta is excluded and unused.

| Fold | W&B ID | W&B URL |
|---:|---|---|
| 2 | `hw6b2q8i` | https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/hw6b2q8i |
| 3 | `0cojka4k` | https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/0cojka4k |

Immutable snapshot:
`/slurmshared/Ngoc/code/hcmus-density-multiscale-view-transformer-20260922-v1`.

Critical SHA256 values:

- config: `e7f14915078d31a72634197e1569ecf64617d0124f1c893d408fd34b027d63d2`
- model: `c133c7f81664bfaacc1c2068ab5d0e249ce407cb488d2d659dc15e89b95322e5`
- engine: `8ae35d1d46582a43116c7867a983b7676a4f0d33a0b1509d554a7c0aefd50524`
- audit: `8b3a14afe4c999c6785ee7c84e371a89871d1397a8419fa9877854a9d786e309`
- launcher: `01e5c7689f4ba0fed29ca0ebfffee6b47f7619c394d8f80dea8d81212107ea06`
- assignments: `43daa86936ee7b1bae1b200836fb1afdfe0c8294c7c865d8f5758bf989f12a9a`

Both folds must run the registered 50 epochs and pass reconstruction audits.
Expansion to folds 0/1/4 requires two-fold mean Macro-F1 >= `0.70` and minimum
>= `0.65`. Early results cannot authorize expansion.
