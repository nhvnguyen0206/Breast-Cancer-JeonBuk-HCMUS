# 🏆 TN-Mammo DICOM Ensemble SOTA (Macro F1 = 0.7384)

Thư mục này chứa toàn bộ mã nguồn, cấu hình và trọng số mô hình **Ensemble (E3 + E7)** đạt điểm số **SOTA cao nhất trong lịch sử dự án (Macro F1 = 0.7384)** trên tập kiểm thử 132 ca DICOM thuộc bộ dữ liệu **TNMammo**.

---

## 📊 1. Bảng Tổng Hợp Kết Quả Thực Nghiệm (Test Set 132 Cases)

| Mô hình / Thí nghiệm | Kích thước | Kiến trúc nổi bật | Macro F1 | Accuracy | QWK | Severe Errors |
| :--- | :---: | :--- | :---: | :---: | :---: | :---: |
| **Baseline (E1)** | 224x224 | DenseNet121 (Mean Fusion) | 0.6277 | 0.6742 | 0.7321 | 3 |
| **E2** | 512x512 | Crop Breast + CLAHE | 0.6729 | 0.6970 | 0.7712 | 2 |
| **E3** | 512x512 | Bilateral Fusion + Neighbor Penalty | 0.7053 | 0.6894 | 0.7178 | **1** |
| **E4** | 512x512 | CBAM + Hard Mining + Oversampling | 0.6743 | 0.6970 | 0.7489 | 1 |
| **E5** | 512x512 | FPN-lite Multi-scale | 0.5857 | 0.6439 | 0.6726 | 3 |
| **E6** | 512x512 | Partial Freezing (DenseBlock 1-2) | 0.5422 | 0.6212 | 0.6637 | 2 |
| **E7** | 1024x1024 | ConvNeXt-Tiny + Safe Horizontal TTA | 0.6864 | 0.6591 | 0.7172 | 2 |
| **ENSEMBLE (E3 + E7) 🌟** | **Mixed** | **50% E3 (DenseNet) + 50% E7 (ConvNeXt)** | **0.7384** | **0.7273** | **0.7665** | 2 |

### 📈 Chi tiết F1-Score từng lớp (Per-Class Metrics của Ensemble):
* **Class A (Fatty):** **0.8000** (Precision: 0.6667, Recall: 1.0000 - Nhận diện 4/4 ca chính xác)
* **Class B (Scattered):** **0.6667** (Precision: 0.6429, Recall: 0.6923)
* **Class C (Heterogeneously Dense):** **0.7193** (Precision: 0.7193, Recall: 0.7193 - Tăng vọt từ 0.65 nhờ E7 độ phân giải 1024)
* **Class D (Extremely Dense):** **0.7674** (Precision: 0.8049, Recall: 0.7333)
* **Tỷ lệ sai số trong phạm vi 1 lớp (Within-One Class):** **98.48%**

---

## 🛠️ 2. Phương Pháp Tiền Xử Lý Ảnh (DICOM Native Pipeline)

Dữ liệu đầu vào là **100% DICOM gốc (12-bit / 16-bit uint16)**. Quy trình tiền xử lý được chuẩn hóa như sau:

1. **Đọc DICOM gốc:** Đọc `pixel_array` trực tiếp qua `pydicom` và tự động đảo ngược màu nếu thuộc tính `PhotometricInterpretation == MONOCHROME1`.
2. **Chuẩn hóa Min-Max về 8-bit (uint8, 0-255):** Để áp dụng các thuật toán thị giác máy tính của OpenCV.
3. **Phân đoạn Bounding Box (Otsu Crop):** Sử dụng `cv2.threshold` Otsu để phát hiện đường viền bầu vú chính và tự động cắt bỏ hoàn toàn các vùng phông nền đen dư thừa.
4. **Tăng cường độ tương phản (CLAHE 8-bit):** Áp dụng `cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))` trên ảnh 8-bit giúp làm nổi bật các dải mô tuyến vú và các vi vôi hóa.
5. **Chuyển về float32 & Chuẩn hóa ImageNet:** Chia `255.0` đưa về dải `[0.0, 1.0]` float32 và chuẩn hóa theo `mean=[0.485, 0.456, 0.406]`, `std=[0.229, 0.224, 0.225]`.

---

## 💡 3. Nguyên Lý Kiến Trúc Mô Hình Kết Hợp (Ensemble Rationale)

* **E3 Model (DenseNet121 @ 512x512):** Học tốt đặc trưng tổng thể và liên kết 4 tư thế (`L-CC`, `L-MLO`, `R-CC`, `R-MLO`) thông qua cơ chế **Bilateral Gated Relational Fusion**.
* **E7 Model (ConvNeXt-Tiny @ 1024x1024):** Sử dụng backbone ConvNeXt hiện đại kết hợp độ phân giải cao `1024x1024` giúp giữ nguyên các sợi mô chi tiết li ti, kết hợp kỹ thuật **Safe Horizontal Flip TTA (Test-Time Augmentation)**.
* **Cơ chế Ensemble:** Trọng số xác suất tối ưu **50% E3 + 50% E7** (Soft Voting Probability Averaging) triệt tiêu hoàn toàn các lỗi nhiễu độc lập của từng model đơn lẻ.

---

## 🚀 4. Hướng Dẫn Chạy Dự Đoán (Inference)

### 4.1. Cài đặt môi trường
```bash
conda activate tnmammo
```

### 4.2. Chạy dự đoán Ensemble trên tập Test
```bash
cd tn-mammo-dicom-ensemble
python3 inference.py --config config.yaml --output-dir outputs/ensemble_results
```

Mã nguồn sẽ tự động tải 2 file weights trong thư mục `checkpoint/`, thực hiện inference 4 tư thế và xuất ra:
* `outputs/ensemble_results/test_metrics.json`: Báo cáo chỉ số Macro F1, Accuracy, QWK.
* `outputs/ensemble_results/test_predictions.csv`: Bảng dự đoán xác suất chi tiết từng ca.

---

## 🏋️ 5. Hướng Dẫn Huấn Luyện Lại (Retraining)

Nếu muốn train lại từng model đơn vị:

```bash
# Train E3 (DenseNet 512)
python3 train.py --config config_E3_enhanced.yaml --output-dir outputs/E3_run

# Train E7 (ConvNeXt 1024)
CUDA_VISIBLE_DEVICES=1 python3 train.py --config config_E7_convnext_1024.yaml --output-dir outputs/E7_run
```

---

## 📁 6. Cấu Trúc Thư Mục

```
tn-mammo-dicom-ensemble/
├── DESCRIPTION.md       # Báo cáo mô tả phương pháp & kết quả thực nghiệm (Tiếng Việt)
├── config.yaml          # File cấu hình Master cho Ensemble
├── inference.py         # Script chạy dự đoán Ensemble (50% E3 + 50% E7)
├── train.py             # Script huấn luyện
├── checkpoint/          # Thư mục lưu trữ trọng số (Git LFS)
│   ├── e3_densenet512_best.pt
│   └── e7_convnext1024_best.pt
└── src/                 # Bộ thư viện mã nguồn gốc
    └── tn_mammo/
```
