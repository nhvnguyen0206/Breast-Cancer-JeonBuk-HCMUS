#!/bin/bash
#SBATCH --job-name=hcmus-density-cv5
#SBATCH --partition=batch
#SBATCH --exclude=slurm-b40a-worker-2
#SBATCH --array=0
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=48G
#SBATCH --time=06:00:00
#SBATCH --no-requeue
#SBATCH --output=/slurmshared/Ngoc/logs/hcmus-density-cv5-%A_%a.log
#SBATCH --error=/slurmshared/Ngoc/logs/hcmus-density-cv5-%A_%a.log
set -euo pipefail
# Screening defaults to fixed fold 0. After all 50 epochs and a passing audit
# with selected DEV Macro-F1 >= 0.75, use sbatch --array=1-4 for confirmation;
# retain the original screened fold 0 rather than rerunning or replacing it.
umask 077
repo=${1:?Pass deployed repository}
config=${2:-configs/vindr_cache_5090_full50.yaml}
cd "$repo"
export PYTHONPATH="$repo/.deps${PYTHONPATH:+:$PYTHONPATH}"
export NETRC=/slurmshared/Ngoc/.netrc
export TORCH_HOME=/slurmshared/Ngoc/datasets/torch
export WANDB_MODE=online PYTHONUNBUFFERED=1 PYTHONHASHSEED=42
export OMP_NUM_THREADS=4 MKL_NUM_THREADS=4 OPENBLAS_NUM_THREADS=1
export CUBLAS_WORKSPACE_CONFIG=:4096:8
runtime_dir="/slurmshared/Ngoc/runs/runtime/hcmus-density-${SLURM_ARRAY_JOB_ID}-${SLURM_ARRAY_TASK_ID}"
export WANDB_DATA_DIR="$runtime_dir/data"
export WANDB_CACHE_DIR="$runtime_dir/cache"
mkdir -p "$WANDB_DATA_DIR" "$WANDB_CACHE_DIR"
unset WANDB_SERVICE _WANDB_SERVICE
python_bin=/slurmshared/Ngoc/envs/paper_1/bin/python
"$python_bin" -c 'import torch; n=torch.cuda.get_device_name(0); print("Allocated GPU:",n,flush=True); assert "5090" in n; x=torch.randn(64,64,device="cuda"); assert torch.isfinite(x@x).all()'
exec "$python_bin" scripts/train_density_fold.py \
  --config "$config" \
  --fold "$SLURM_ARRAY_TASK_ID" \
  --output-dir "/slurmshared/Ngoc/runs/hcmus-density-cv5-v1-${SLURM_ARRAY_JOB_ID}-fold${SLURM_ARRAY_TASK_ID}" \
  --device cuda
