#!/usr/bin/env bash
# Run E3 Enhanced experiment: Bilateral Fusion + Neighbor Penalty + ImageNet Init
# This script should be run AFTER the E2 preprocessed training finishes.
# Usage: bash run_E3_enhanced.sh

set -euo pipefail

cd /mnt/hcmus/breast_vn/code/phase2.2/antigavity_dicom_create

source /mnt/hcmus/breast_vn/miniconda3/etc/profile.d/conda.sh
conda activate tnmammo

export CUDA_VISIBLE_DEVICES=0

OUTPUT_DIR="outputs/DICOM_E3_enhanced_run"
CONFIG="config_E3_enhanced.yaml"
LOG="${OUTPUT_DIR}.log"

echo "=============================================="
echo " E3 Enhanced: Bilateral + NeighborPenalty"
echo " Config: ${CONFIG}"
echo " Output: ${OUTPUT_DIR}"
echo " Started: $(date)"
echo "=============================================="

# 1. Train
echo "[STEP 1/3] Training..."
python3 train.py --config "${CONFIG}" --output-dir "${OUTPUT_DIR}" 2>&1 | tee -a "${LOG}"

# 2. Evaluate on test set
echo "[STEP 2/3] Evaluating on test set..."
python3 evaluate.py \
    --checkpoint "${OUTPUT_DIR}/best_checkpoint.pt" \
    --test-manifest manifests/dicom_tn_test132.csv \
    --dicom-root /mnt/hcmus/breast_vn/data/TNMammo/data_tn_mammo_dicom \
    --output-dir "${OUTPUT_DIR}" \
    --image-size 512 \
    --batch-size 2 \
    2>&1 | tee -a "${LOG}"

# 3. Generate summary
echo "[STEP 3/3] Generating summary..."
python3 generate_summary.py --output-dir "${OUTPUT_DIR}" 2>&1 | tee -a "${LOG}"

echo ""
echo "=============================================="
echo " E3 Enhanced COMPLETE at $(date)"
echo "=============================================="
