# Thí nghiệm 1 sau best Macro-F1

Package phân loại mật độ mô vú BI-RADS A/B/C/D từ bốn view:
`L_CC`, `L_MLO`, `R_CC`, `R_MLO`.

Đây là phiên bản thí nghiệm preprocessing/augmentation phát triển sau model
E1 best Macro-F1. Package có checkpoint baseline đã chọn, code train/evaluate,
ba config độ phân giải và pipeline sinh báo cáo.

## Cấu trúc

```text
thunghiem1_saubestmacro/
├── checkpoint/
│   └── best_model.pt
├── configs/
│   ├── v2_224.yaml
│   ├── v2_384.yaml
│   └── v2_512.yaml
├── docs/
│   ├── README.md
│   ├── 01_PREPROCESSING.md
│   ├── 02_DATASET_MANIFEST.md
│   ├── 03_MODEL_LOSS_TRAINING.md
│   ├── 04_CONFIGS_AND_RUNS.md
│   ├── 05_METRICS_EVALUATION.md
│   ├── 06_REPORT_GRADCAM.md
│   ├── 07_OUTPUT_INVENTORY.md
│   └── 08_QUEUE_OPERATIONS.md
├── scripts/
│   ├── generate_report.py
│   └── run_queue.sh
├── src/tn_mammo/
│   ├── data/
│   ├── losses/
│   ├── metrics/
│   ├── models/
│   ├── training/
│   ├── utils/
│   ├── constants.py
│   └── inference.py
├── config.yaml
├── evaluate.py
├── requirements.txt
└── train.py
```

Checkpoint được quản lý bằng Git LFS.

## Những thay đổi chính

- Đọc được cả schema `L_CC/...` và schema Phase-G `left_cc_path/...`.
- Crop bounding box vùng khác nền đen.
- Chuẩn hóa orientation bằng cách lật cố định hai view bên phải.
- Pad vuông rồi resize, không kéo méo tỷ lệ giải phẫu.
- Không dùng random horizontal flip độc lập.
- Rotation, translation, gamma và contrast dùng chung tham số cho bốn view.
- Gaussian noise nhẹ khi train.
- Chạy độc lập ở resolution 224, 384 và 512.
- Lưu probability, prediction theo `case_id`, metric và history từng epoch.
- Sinh ROC/AUC, confusion matrix, heatmap, training curve và Grad-CAM.

Chi tiết từng nhóm code nằm trong [docs/README.md](docs/README.md).

## Cài đặt

Khuyến nghị Python 3.10 và PyTorch/CUDA phù hợp GPU:

```bash
python -m pip install -r requirements.txt
```

## Manifest

Các cột bắt buộc:

```text
case_id,label,L_CC,L_MLO,R_CC,R_MLO
```

Hoặc schema Phase-G:

```text
case_id,label,left_cc_path,left_mlo_path,right_cc_path,right_mlo_path
```

Đường dẫn ảnh có thể tuyệt đối hoặc tương đối so với manifest.

## Train một cấu hình

```bash
python -u train.py \
  --config configs/v2_384.yaml \
  --output-dir outputs/v2_384
```

Các YAML hiện giữ đường dẫn tuyệt đối của môi trường nghiên cứu HCMUS. Khi chạy
trên máy khác, sửa ba manifest và `initialization_checkpoint` trong config.

## Evaluate

```bash
python -u evaluate.py \
  --checkpoint outputs/v2_384/best_checkpoint.pt \
  --manifest /path/to/validation.csv \
  --output-dir outputs/v2_384_eval
```

## Queue 224 → 384 → 512 → PDF

```bash
CUDA_VISIBLE_DEVICES=1 bash scripts/run_queue.sh
```

Queue ghi:

- `best_checkpoint.pt`
- `best_metrics.json`
- `best_predictions.csv`
- `history.jsonl`
- `tonghop.pdf`

## Kết quả validation đã chạy

| Run | Accuracy | BalAcc | Macro-F1 | Macro AUC | QWK | Severe |
|---|---:|---:|---:|---:|---:|---:|
| baseline selected | 0.6917 | 0.7160 | **0.7349** | **0.8972** | **0.7613** | 0 |
| v2 224 | 0.6692 | 0.7442 | 0.7023 | 0.8879 | 0.7340 | 0 |
| v2 384 | 0.6767 | **0.7528** | 0.7079 | 0.8871 | 0.7394 | 0 |
| v2 512 | 0.5639 | 0.5744 | 0.4954 | 0.8339 | 0.5863 | 2 |

Primary metric đã khóa là validation Macro-F1, nên baseline checkpoint vẫn là
model thắng chung. Trong nhóm preprocessing mới, v2 384 là cấu hình tốt nhất.

## Locked test

Checkpoint `checkpoint/best_model.pt` có SHA256:

```text
7b80c4cd36f4377f87f0dbfbc337ba0d0f58fa8ac60cca9043790ddd5b43b22b
```

Checkpoint này đã được đánh giá one-time trên TN locked test 132 ca:

- Accuracy: 0.6818
- Balanced accuracy: 0.7454
- Macro-F1: 0.7022
- QWK: 0.7643
- Within-one: 1.0000
- Severe errors: 0

Không dùng locked test để chọn resolution, augmentation hoặc hyperparameter.
