#!/bin/bash
#SBATCH --job-name=hcmus-paper1-vindr
#SBATCH --partition=batch
#SBATCH --exclude=slurm-b40a-worker-2
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=48G
#SBATCH --time=06:00:00
#SBATCH --no-requeue
#SBATCH --output=/slurmshared/Ngoc/logs/hcmus-paper1-vindr-%j.log
#SBATCH --error=/slurmshared/Ngoc/logs/hcmus-paper1-vindr-%j.log
set -euo pipefail
umask 077

repo=${1:?Pass the deployed repository directory}
config=${2:-configs/vindr_cache_5090.yaml}
cd "$repo"
export PYTHONPATH="$repo/.deps${PYTHONPATH:+:$PYTHONPATH}"
export NETRC=/slurmshared/Ngoc/.netrc
export TORCH_HOME=/slurmshared/Ngoc/datasets/torch
export WANDB_MODE=online
export PYTHONUNBUFFERED=1 PYTHONHASHSEED=42
export OMP_NUM_THREADS=4 MKL_NUM_THREADS=4 OPENBLAS_NUM_THREADS=1
export CUBLAS_WORKSPACE_CONFIG=:4096:8
unset WANDB_SERVICE _WANDB_SERVICE
python_bin=/slurmshared/Ngoc/envs/paper_1/bin/python
"$python_bin" -c 'import torch; name=torch.cuda.get_device_name(0); print("Allocated GPU:",name, "torch:",torch.__version__,flush=True); assert "5090" in name; x=torch.randn(64,64,device="cuda"); assert torch.isfinite(x@x).all()'
exec "$python_bin" train.py --config "$config" \
  --train-manifest data/vindr_cache_fold0/fit.csv \
  --valid-manifest data/vindr_cache_fold0/dev.csv \
  --output-dir "/slurmshared/Ngoc/runs/hcmus-paper1-vindr-f0-e50-${SLURM_JOB_ID}" \
  --device cuda
