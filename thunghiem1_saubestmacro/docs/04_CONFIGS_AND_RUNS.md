# Config và các run đã thực hiện

## Config

```text
filecode1/configs/v2_224.yaml
filecode1/configs/v2_384.yaml
filecode1/configs/v2_512.yaml
```

Ba config giữ nguyên model, data, seed, loss và training protocol; yếu tố chính
được thay đổi là resolution.

| Run | Resolution | Batch size | Epoch thực chạy |
|---|---:|---:|---:|
| v2_224 | 224 | 2 | 25 |
| v2_384 | 384 | 2 | 21 |
| v2_512 | 512 | 1 | 11 |

Số epoch trên được lấy từ số dòng `history.jsonl`; run có thể kết thúc do early
stopping.

## Lệnh chạy một run

```bash
cd /mnt/hcmus/breast_vn/code/new_implement_v2
CUDA_VISIBLE_DEVICES=1 \
/mnt/hcmus/miniconda3/envs/tnmammo_v2/bin/python -u train.py \
  --config configs/v2_224.yaml \
  --output-dir outputs/v2_224
```

Thay `224` bằng `384` hoặc `512` cho run tương ứng.

## Baseline

`baseline_selected` được đánh giá từ:

```text
filecode1/checkpoint/best_model.pt
```

Đây là checkpoint package đã chọn, dùng preprocessing validation kiểu cũ để
đảm bảo đánh giá tương thích ngược.

## Kết luận validation

- Model thắng chung: `baseline_selected`, Macro-F1 0.7349.
- Model preprocessing mới tốt nhất: `v2_384`, Macro-F1 0.7079.
- 512 giảm rõ rệt và có hai severe errors; không được chọn.
