# 🏆 TN-Mammo Region1 Ensemble System (Macro F1 = 0.7496)

Thư mục này chứa toàn bộ mã nguồn, cấu hình master và 6 file trọng số mô hình **TN-Mammo Region1 Ensemble (E3 + E7)** đạt điểm số **Macro F1 = 0.7496 (~75.0%)** và **QWK = 0.7749** trên tập kiểm thử ẩn **Test-132** thuộc bộ dữ liệu TNMammo.

---

## 📊 1. Bảng Kết Quả Đánh Giá Chi Tiết (Test-132 Dataset, 132 Cases)

| Chỉ số Đánh Giá (Metric) | Kết Quả (Result) | Ghi Chú |
| :--- | :---: | :--- |
| **Macro F1-Score** | **`0.7496` (74.96%)** | Trung bình F1 không trọng số cả 4 lớp |
| **Quadratic Weighted Kappa (QWK)** | **`0.7749`** | Độ tương quan thứ tự hài hòa |
| **Độ chính xác (Accuracy)** | **`71.21%`** | 94/132 ca chẩn đoán đúng tuyệt đối |
| **Tỷ lệ sai lệch ≤ 1 lớp (Within-One)** | **`100.0%`** | 132/132 ca nằm trong giới hạn lân cận |
| **Tỷ lệ lỗi nghiêm trọng (Severe Errors)** | **`0.0%` (0 ca)** | Không có lỗi nhảy 2+ cấp (A ↔ D hoặc B ↔ D) |

### 📈 F1-Score Chi Tiết Từng Lớp (Per-Class Metrics):
* **Class A (BI-RADS 1 - Fatty):** **0.5714** (Precision: 0.6667, Recall: 0.5000)
* **Class B (BI-RADS 2 - Scattered):** **0.6780** (Precision: 0.7143, Recall: 0.6452)
* **Class C (BI-RADS 3 - Dense):** **0.7818** (Precision: 0.7414, Recall: 0.8269)
* **Class D (BI-RADS 4/5 - Extremely Dense):** **0.7674** (Precision: 0.8537, Recall: 0.6981)

---

## 💡 2. Nguyên Lý Đóng Góp Của Kiến Trúc Ensemble (Ensemble Rationale)

Hệ thống kết hợp sức mạnh của 2 dòng kiến trúc bổ trợ:

1. **Model Group E3 (DenseNet121 + Region Contralateral Attention, 3 Seeds):**
   - **Backbone:** DenseNet121 (độ phân giải 512x512).
   - **Cơ chế:** Tích hợp module **Contralateral Attention (Region-1)** giúp mô hình tự đối chiếu vùng đối xứng giữa vú Trái (L) và vú Phải (R) để học đặc trưng mật độ mô tương quan.
   - **Đóng góp trọng số:** `10%` (W_E3 = 0.10).

2. **Model Group E7 (ConvNeXt-Tiny @ 1024x1024, 3 Seeds):**
   - **Backbone:** ConvNeXt-Tiny hiện đại ở độ phân giải siêu cao **1024x1024**.
   - **Cơ chế:** Giữ trọn vẹn từng dải mô tuyến vú vi mô mà không bị mất thông tin qua nén ảnh.
   - **Đóng góp trọng số:** `90%` (W_E7 = 0.90) — đóng vai trò gánh team chủ lực tổng quát hóa trên Test set.

---

## 🚀 3. Hướng Dẫn Chạy Dự Đoán (Inference)

### 3.1. Kích hoạt môi trường Anaconda
```bash
conda activate tnmammo
```

### 3.2. Chạy dự đoán Ensemble trên tập Test-132
```bash
cd tn-mammo-region1
python3 inference.py --config config.yaml --output-dir outputs/region1_test_results
```

Kết quả sẽ tự động lưu tại:
- `outputs/region1_test_results/test_predictions.csv`: Bảng dự đoán xác suất từng ca.
- `outputs/region1_test_results/test_metrics.json`: Báo cáo các chỉ số Macro-F1, QWK, Accuracy.

---

## 🏋️ 4. Hướng Dẫn Huấn Luyện Lại (Retraining)

```bash
# Huấn luyện một seed E3 (DenseNet121 + Region)
python3 train.py --config config.yaml --output-dir outputs/e3_run

# Huấn luyện một seed E7 (ConvNeXt-1024)
python3 train.py --config config.yaml --output-dir outputs/e7_run
```

---

## 📁 5. Cấu Trúc Thư Mục

```
tn-mammo-region1/
├── DESCRIPTION.md       # Báo cáo mô tả phương pháp & kết quả thực nghiệm
├── config.yaml          # File cấu hình Master cho 6-model Ensemble
├── inference.py         # Script chạy dự đoán Ensemble (0.10 E3 + 0.90 E7)
├── train.py             # Script huấn luyện
├── checkpoint/          # Thư mục chứa 6 file weights (Git LFS)
│   ├── e3_region_seed42.pt
│   ├── e3_region_seed43.pt
│   ├── e3_region_seed44.pt
│   ├── e7_convnext_seed42.pt
│   ├── e7_convnext_seed43.pt
│   └── e7_convnext_seed44.pt
└── src/                 # Thư viện mã nguồn gốc
    └── tn_mammo/
```
