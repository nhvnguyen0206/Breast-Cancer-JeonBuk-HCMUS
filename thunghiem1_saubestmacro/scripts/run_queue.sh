#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON="/mnt/hcmus/miniconda3/envs/tnmammo_v2/bin/python"
MANIFEST="/mnt/hcmus/breast_vn/code/new_implement/manifests/phaseg_tn_valid133.csv"
STATUS="${ROOT}/queue_status.txt"

cd "${ROOT}"
export CUDA_VISIBLE_DEVICES="${CUDA_VISIBLE_DEVICES:-0}"
export MPLCONFIGDIR="${ROOT}/.matplotlib"
mkdir -p outputs logs "${MPLCONFIGDIR}"

trap 'code=$?; printf "FAILED exit=%s time=%s\n" "$code" "$(date -Iseconds)" > "${STATUS}"; exit "$code"' ERR

WAIT_FOR_PID="${WAIT_FOR_PID:-}"
if [[ -n "${WAIT_FOR_PID}" ]]; then
  while kill -0 "${WAIT_FOR_PID}" 2>/dev/null; do
    command_line="$(tr '\0' ' ' < "/proc/${WAIT_FOR_PID}/cmdline" 2>/dev/null || true)"
    if [[ "${command_line}" != *"baseline_ngoc_e1_seed42_20260724"* ]]; then
      break
    fi
    printf "WAITING baseline_pid=%s time=%s\n" "${WAIT_FOR_PID}" "$(date -Iseconds)" > "${STATUS}"
    sleep 60
  done
fi

printf "RUNNING baseline_eval time=%s\n" "$(date -Iseconds)" > "${STATUS}"

"${PYTHON}" -u evaluate.py \
  --checkpoint checkpoint/best_model.pt \
  --manifest "${MANIFEST}" \
  --output-dir outputs/baseline_selected \
  > logs/baseline_selected_eval.log 2>&1

for resolution in 224 384 512; do
  printf "RUNNING v2_%s time=%s\n" "${resolution}" "$(date -Iseconds)" > "${STATUS}"
  "${PYTHON}" -u train.py \
    --config "configs/v2_${resolution}.yaml" \
    --output-dir "outputs/v2_${resolution}" \
    > "logs/v2_${resolution}.log" 2>&1
done

printf "RUNNING report time=%s\n" "$(date -Iseconds)" > "${STATUS}"
"${PYTHON}" -u scripts/generate_report.py \
  --manifest "${MANIFEST}" \
  --output "${ROOT}/tonghop.pdf" \
  --run baseline_selected outputs/baseline_selected checkpoint/best_model.pt - \
  --run v2_224 outputs/v2_224 outputs/v2_224/best_checkpoint.pt configs/v2_224.yaml \
  --run v2_384 outputs/v2_384 outputs/v2_384/best_checkpoint.pt configs/v2_384.yaml \
  --run v2_512 outputs/v2_512 outputs/v2_512/best_checkpoint.pt configs/v2_512.yaml \
  > logs/report.log 2>&1

printf "COMPLETED report=%s time=%s\n" "${ROOT}/tonghop.pdf" "$(date -Iseconds)" > "${STATUS}"
