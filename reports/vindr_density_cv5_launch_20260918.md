# Density-CV5 full-50 campaign — 2026-09-18

**Completed:** all five active runs finished 50/50 epochs. Checkpoints,
prediction membership and W&B summaries were verified. See the
[final aggregate results](vindr_density_cv5_results_20260918.md).

User requested rerunning all five folds on the new density-balanced split.
Slurm array **712**, tasks 0–4, one RTX 5090 per fold, at most five concurrent.
All five tasks verified RTX 5090 at startup. **Worker recovery:** original tasks
712_2/3/4 subsequently failed after epoch 1 when W&B tried to stage confusion
matrix artifacts under a non-writable worker home directory. Tasks 712_0/1
continue unchanged. Failed runs/artifacts were preserved.

Only folds 2–4 were relaunched as array **717**, with fresh ImageNet initialization
and the same training/split settings. The retry script sets per-task
`WANDB_DATA_DIR` and `WANDB_CACHE_DIR` under `/slurmshared/Ngoc/runs/runtime/`.
No HOME override, model change, loss change or data change was needed.
The original failed W&B runs in the initial-launch table below must not be
included in CV results.

Active runs after recovery:

| Fold | Slurm task | W&B run |
|---|---|---|
| 0 | 712_0 | https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/phfsagbm |
| 1 | 712_1 | https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/ecgddcce |
| 2 | 717_2 | https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/m7d1pybx |
| 3 | 717_3 | https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/z2c15901 |
| 4 | 717_4 | https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/ps6qqkst |

Retry output paths use `hcmus-density-cv5-v1-717-fold{i}` and logs use
`hcmus-density-cv5-717_{i}.log`. The group contains both failed initial attempts
and active retries; use the active run IDs above when aggregating results.

Post-recovery W&B API verification: all five active runs report `running`;
folds 0/1 reached epoch 4, folds 2/3/4 reached epoch 1, and all five have logged
confusion matrices successfully. Fold IDs, group name and DEV class counts
match the registered new split. All five Slurm tasks remain RUNNING.

Initial launch (including the three failed worker attempts):

| Fold | W&B run | Observed node |
|---|---|---|
| 0 | https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/phfsagbm | slurm-b20a-master-0 |
| 1 | https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/ecgddcce | slurm-b20a-master-0 |
| 2 | https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/bg2s5q5c | slurm-b40a-worker-1 |
| 3 | https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/jhve2hqx | slurm-b40a-worker-1 |
| 4 | https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/9159ncra | slurm-b40a-worker-1 |

W&B group: `vindr-densityCV5-v1-seed42-full50`, project `HCMUS-paper1`.
Each run records fold, split schema/hash and fresh-ImageNet initialization in
`config.experiment`, plus train/validation class counts in its summary.

## Configuration

- Split: `data/vindr_density_cv5_seed42_v1/fold_i/{fit,dev}.csv`.
- Each fold uses 4/5 of the population for FIT and the remaining fold for DEV.
- Full **50 epochs**, `min_epochs=50`; no early stopping before epoch 50.
- Fresh ImageNet weights for every fold; old density/BIRADS-split checkpoints
  are not loaded. Seed 42, 512px, batch 2, four loader workers, original losses,
  AdamW LR 5e-5, cosine decay over 50 epochs, FP16 AMP.
- Model architecture and image preprocessing unchanged, including direct square
  resize (no new padding or orientation transformations).
- Source config: `configs/vindr_cache_5090_full50.yaml`, with fold-specific W&B
  naming/provenance applied by `scripts/train_density_fold.py`.
- The launcher checks assignment SHA256 and exact FIT/DEV rows against the
  registered assignment before starting W&B/training. All five passed locally
  and on the cluster. Nine tests pass, including rejection of altered manifests.

## Remote artifacts

Deployment: `/slurmshared/Ngoc/code/hcmus-paper1-vindr-20260918-e50`.
Output per fold:
`/slurmshared/Ngoc/runs/hcmus-density-cv5-v1-712-fold{i}`.
Logs: `/slurmshared/Ngoc/logs/hcmus-density-cv5-712_{i}.log`.
Each output contains epoch history, selected `best.pt`, and selected DEV predictions.

Submission (already executed; do not rerun just to monitor):

```bash
sbatch --chdir=/slurmshared/Ngoc/code/hcmus-paper1-vindr-20260918-e50 scripts/train_density_cv5_5090.sbatch /slurmshared/Ngoc/code/hcmus-paper1-vindr-20260918-e50
```

These are DEV-selected cross-validation experiments, not independent final-test
estimates. Each DEV fold has only 1–2 class-A studies. Old runs and splits are
preserved; their results must not be mixed with this protocol. This note records
the launch, not completed training results.
