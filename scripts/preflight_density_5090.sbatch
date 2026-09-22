#!/bin/bash
#SBATCH --job-name=hcmus-density-preflight
#SBATCH --partition=batch
#SBATCH --exclude=slurm-b40a-worker-2
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=4
#SBATCH --mem=24G
#SBATCH --time=00:20:00
#SBATCH --no-requeue
#SBATCH --output=/slurmshared/Ngoc/logs/hcmus-density-preflight-%j.log
#SBATCH --error=/slurmshared/Ngoc/logs/hcmus-density-preflight-%j.log
set -euo pipefail
umask 077

repo=${1:?Pass deployed repository}
config=${2:?Pass registered config}
manifest=${3:?Pass registered FIT manifest}
cd "$repo"

export PYTHONPATH="$repo/.deps${PYTHONPATH:+:$PYTHONPATH}"
export PYTHONUNBUFFERED=1 PYTHONHASHSEED=42
export OMP_NUM_THREADS=4 MKL_NUM_THREADS=4 OPENBLAS_NUM_THREADS=1
export CUBLAS_WORKSPACE_CONFIG=:4096:8

python_bin=/slurmshared/Ngoc/envs/paper_1/bin/python
"$python_bin" -c 'import torch; n=torch.cuda.get_device_name(0); print("Allocated GPU:",n,flush=True); assert "5090" in n'
exec "$python_bin" scripts/preflight_density_batch.py \
  --config "$config" \
  --manifest "$manifest"
