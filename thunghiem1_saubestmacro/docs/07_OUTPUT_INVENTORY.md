# Danh mục output của filecode1

## Baseline validation

```text
outputs/baseline_selected/best_metrics.json
outputs/baseline_selected/best_predictions.csv
```

## V2 224

```text
outputs/v2_224/best_checkpoint.pt
outputs/v2_224/best_metrics.json
outputs/v2_224/best_predictions.csv
outputs/v2_224/history.jsonl
logs/v2_224.log
```

## V2 384

```text
outputs/v2_384/best_checkpoint.pt
outputs/v2_384/best_metrics.json
outputs/v2_384/best_predictions.csv
outputs/v2_384/history.jsonl
logs/v2_384.log
```

## V2 512

```text
outputs/v2_512/best_checkpoint.pt
outputs/v2_512/best_metrics.json
outputs/v2_512/best_predictions.csv
outputs/v2_512/history.jsonl
logs/v2_512.log
```

## Locked test authoritative

```text
outputs/locked_test_baseline_selected_authoritative/
├── FILECODE1_PROVENANCE.txt
├── LOCKED_CONFIG.json
├── PIPELINE_DONE.txt
├── data_audit.json
├── test_c_to_d_errors.csv
├── test_confusion_matrix.csv
├── test_d_to_c_errors.csv
├── test_metrics.json
├── test_predictions.csv
├── test_severe_errors.csv
└── validation_reproduction.json
```

## Report

```text
tonghop.pdf
logs/report.log
queue_status.txt
```

## Artifact khác đang có trong filecode1

Filecode1 hiện còn có các folder `outputs/R2_*`, `outputs/E1_vs_R2_*` và
`experiments/R3_R6_*`. Đây là các artifact hậu xử lý/ensemble xuất hiện sau
pipeline preprocessing 224/384/512. Chúng không thuộc queue preprocessing cốt
lõi được mô tả trong bộ README này và không được dùng để chọn kết quả ở bảng
validation phía trên.
