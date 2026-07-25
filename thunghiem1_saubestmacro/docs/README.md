# Tài liệu filecode1 — preprocessing và thí nghiệm đa độ phân giải

## 1. Quy ước và vị trí

`filecode1` là:

```text
/mnt/hcmus/breast_vn/code/new_implement_v2
```

Đây là phiên bản phát triển từ package `tn-mammo-bestmacro-hientai`, với mục
tiêu kiểm tra các góp ý về preprocessing/augmentation bốn view và so sánh ba
độ phân giải 224, 384 và 512.

Folder `xuly_phanpreprocessing` chỉ chứa tài liệu. Code và artifact thật vẫn
nằm trong `filecode1` để tránh tạo thêm bản sao dễ lệch phiên bản.

## 2. Filecode1 đã làm được gì?

1. Hỗ trợ trực tiếp manifest Phase-G có các cột:
   `left_cc_path`, `left_mlo_path`, `right_cc_path`, `right_mlo_path`.
2. Crop bounding box vùng ảnh khác nền đen và giữ một margin nhỏ.
3. Chuẩn hóa orientation bằng cách lật cố định hai view bên phải.
4. Không dùng `RandomHorizontalFlip` độc lập.
5. Áp dụng chung tham số rotation, translation, gamma và contrast cho cả bốn
   view của cùng một ca.
6. Thêm Gaussian noise nhẹ khi train.
7. Giữ tỷ lệ ảnh, pad thành hình vuông rồi mới resize.
8. Train riêng ở 224, 384 và 512.
9. Lưu checkpoint tốt nhất theo validation Macro-F1.
10. Lưu prediction, probability, `case_id`, metric và history từng epoch.
11. Sinh ROC/AUC, confusion matrix, heatmap, training curve và Grad-CAM.
12. Tổng hợp báo cáo thành `filecode1/tonghop.pdf`.
13. Đối chiếu locked-test bằng SHA256 và reuse kết quả one-time authoritative
    khi checkpoint thắng trùng tuyệt đối checkpoint đã được đánh giá.

## 3. Kết quả validation

| Run | Acc | BalAcc | Macro-F1 | Weighted-F1 | Macro AUC | QWK | Within-1 | MAE | Severe |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| baseline_selected | 0.6917 | 0.7160 | **0.7349** | 0.6923 | **0.8972** | **0.7613** | 1.0000 | **0.3083** | 0 |
| v2_224 | 0.6692 | 0.7442 | 0.7023 | 0.6611 | 0.8879 | 0.7340 | 1.0000 | 0.3308 | 0 |
| v2_384 | 0.6767 | **0.7528** | 0.7079 | 0.6660 | 0.8871 | 0.7394 | 1.0000 | 0.3233 | 0 |
| v2_512 | 0.5639 | 0.5744 | 0.4954 | 0.5112 | 0.8339 | 0.5863 | 0.9850 | 0.4511 | 2 |

Theo primary metric đã định trước là validation Macro-F1,
`baseline_selected` là model thắng. Trong riêng nhóm preprocessing mới,
`v2_384` tốt hơn `v2_224` và `v2_512`.

## 4. Locked test của model thắng

Checkpoint thắng có SHA256:

```text
7b80c4cd36f4377f87f0dbfbc337ba0d0f58fa8ac60cca9043790ddd5b43b22b
```

Checkpoint này trùng checkpoint đã được đánh giá one-time trên TN locked test
132 ca. Kết quả authoritative:

| Metric | Giá trị |
|---|---:|
| Accuracy | 0.6818 |
| Balanced accuracy | 0.7454 |
| Macro-F1 | 0.7022 |
| Weighted-F1 | 0.6799 |
| QWK | 0.7643 |
| Within-one | 1.0000 |
| Severe errors | 0 |

Artifact nằm tại:

```text
filecode1/outputs/locked_test_baseline_selected_authoritative/
```

## 5. Mục lục tài liệu

- [01_PREPROCESSING.md](01_PREPROCESSING.md): crop, orientation, resize và augmentation đồng bộ.
- [02_DATASET_MANIFEST.md](02_DATASET_MANIFEST.md): schema manifest và dataset loader.
- [03_MODEL_LOSS_TRAINING.md](03_MODEL_LOSS_TRAINING.md): model, loss và training engine.
- [04_CONFIGS_AND_RUNS.md](04_CONFIGS_AND_RUNS.md): config 224/384/512 và lệnh chạy.
- [05_METRICS_EVALUATION.md](05_METRICS_EVALUATION.md): prediction, ROC/AUC và metric.
- [06_REPORT_GRADCAM.md](06_REPORT_GRADCAM.md): PDF, plot và Grad-CAM.
- [07_OUTPUT_INVENTORY.md](07_OUTPUT_INVENTORY.md): toàn bộ output chính đã sinh.
- [08_QUEUE_OPERATIONS.md](08_QUEUE_OPERATIONS.md): queue, nohup, status và log.
