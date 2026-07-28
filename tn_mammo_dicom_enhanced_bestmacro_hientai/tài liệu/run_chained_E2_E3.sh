#!/usr/bin/env bash
# Chained pipeline: Wait for E2 preprocessed to finish, then run E3 enhanced
# Usage: nohup bash run_chained_E2_E3.sh &

set -euo pipefail

cd /mnt/hcmus/breast_vn/code/phase2.2/antigavity_dicom_create

source /mnt/hcmus/breast_vn/miniconda3/etc/profile.d/conda.sh
conda activate tnmammo

export CUDA_VISIBLE_DEVICES=0

CHAIN_LOG="outputs/chained_E2_E3.log"

echo "=============================================" | tee -a "${CHAIN_LOG}"
echo " Chained Pipeline: Wait for E2, then run E3" | tee -a "${CHAIN_LOG}"
echo " Started: $(date)" | tee -a "${CHAIN_LOG}"
echo "=============================================" | tee -a "${CHAIN_LOG}"

# Wait for E2 training to finish (check for best_checkpoint.pt and training.log completion)
E2_DIR="outputs/DICOM_E2_512_preprocessed"
echo "[CHAIN] Waiting for E2 training to complete..." | tee -a "${CHAIN_LOG}"

while true; do
    # Check if training.log contains "DONE" or the summary has been generated
    if [ -f "${E2_DIR}/training_summary.png" ]; then
        echo "[CHAIN] E2 summary detected - E2 is complete!" | tee -a "${CHAIN_LOG}"
        break
    fi
    # Also check if the log file stopped updating (training finished but evaluate/summary may have failed)
    if [ -f "${E2_DIR}/best_checkpoint.pt" ]; then
        # Check if any python train.py process is still running
        if ! pgrep -f "train.py.*DICOM_E2" > /dev/null 2>&1; then
            echo "[CHAIN] E2 train process no longer running - proceeding" | tee -a "${CHAIN_LOG}"
            break
        fi
    fi
    sleep 30
done

echo "[CHAIN] E2 finished at $(date). Starting E3..." | tee -a "${CHAIN_LOG}"

# Run E3
bash run_E3_enhanced.sh 2>&1 | tee -a "${CHAIN_LOG}"

echo "" | tee -a "${CHAIN_LOG}"
echo "=============================================" | tee -a "${CHAIN_LOG}"
echo " FULL CHAIN COMPLETE at $(date)" | tee -a "${CHAIN_LOG}"
echo "=============================================" | tee -a "${CHAIN_LOG}"
