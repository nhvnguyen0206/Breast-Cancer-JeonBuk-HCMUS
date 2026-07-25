# Model, loss và training engine

## File code

```text
filecode1/src/tn_mammo/models/density_model.py
filecode1/src/tn_mammo/losses/multitask.py
filecode1/src/tn_mammo/training/engine.py
filecode1/src/tn_mammo/utils/seeding.py
filecode1/train.py
```

## Model

`FourViewDensityModel` dùng DenseNet121 chia sẻ trọng số cho bốn ảnh.

Luồng feature:

```text
4 views
  -> shared DenseNet121 features
  -> feature từng view [1024]
  -> mean hai view bên trái
  -> mean hai view bên phải
  -> mean hai bên
  -> exam feature [1024]
```

Hai head:

- Flat head: 4 logits A/B/C/D, dùng `argmax` làm prediction cuối.
- CORAL ordinal head: 3 ngưỡng, chỉ hỗ trợ loss lúc train.

## Khởi tạo

Mỗi run v2 khởi tạo từ checkpoint E0:

```text
/mnt/hcmus/breast_vn/code/new_implement/outputs/
E0_phaseg_reproduction_seed42_20260718_163950/best_checkpoint.pt
```

Hai key của ordinal head được phép thiếu vì E0 chưa có head này.

## Loss

```text
total_loss =
class_balanced_focal(flat_logits)
+ 0.5 * coral_loss(ordinal_logits)
```

- Focal gamma: 2.0.
- Effective-number beta: 0.99.
- TN class counts: `[12, 81, 178, 140]`.

## Training

- Optimizer: AdamW.
- Learning rate: `1e-4`.
- Weight decay: `1e-4`.
- Scheduler: StepLR, step size 5, gamma 0.5.
- AMP: bật trên CUDA.
- Gradient clipping: norm 5.0.
- Seed: 42.
- Primary selection metric: validation Macro-F1.
- Early stopping patience: 10.
- Tối đa: 50 epoch.

Mỗi epoch ghi một dòng vào `history.jsonl`. Khi Macro-F1 tốt hơn, engine ghi:

```text
best_checkpoint.pt
best_metrics.json
best_predictions.csv
```
