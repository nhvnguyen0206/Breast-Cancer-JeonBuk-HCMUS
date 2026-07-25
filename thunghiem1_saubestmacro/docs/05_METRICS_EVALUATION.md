# Evaluation, prediction và metrics

## File code

```text
filecode1/evaluate.py
filecode1/src/tn_mammo/inference.py
filecode1/src/tn_mammo/metrics/classification.py
```

## Prediction

Prediction cuối dùng:

```python
softmax(flat_logits).argmax(dim=1)
```

CORAL head không được dùng để decode.

`best_predictions.csv` chứa:

```text
case_id, y_true, y_pred, prob_A, prob_B, prob_C, prob_D
```

## Metric được tính

- Accuracy.
- Balanced accuracy.
- Macro-F1.
- Weighted-F1.
- Precision/recall/F1/support từng lớp.
- Quadratic weighted kappa (QWK).
- Within-one accuracy.
- Ordinal MAE.
- Severe error count, với lỗi cách từ hai bậc trở lên.
- Confusion matrix 4×4.
- One-vs-rest AUC từng lớp.
- Macro và weighted multiclass AUC.
- FPR, TPR và threshold để vẽ ROC từng lớp.

## Lệnh đánh giá

```bash
cd /mnt/hcmus/breast_vn/code/new_implement_v2
CUDA_VISIBLE_DEVICES=1 \
/mnt/hcmus/miniconda3/envs/tnmammo_v2/bin/python -u evaluate.py \
  --checkpoint outputs/v2_384/best_checkpoint.pt \
  --manifest /mnt/hcmus/breast_vn/code/new_implement/manifests/phaseg_tn_valid133.csv \
  --output-dir outputs/v2_384_recheck
```

Không dùng locked test để chọn resolution, augmentation hoặc hyperparameter.
