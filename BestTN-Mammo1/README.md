# BestTN-Mammo1 (REGION1_ENSEMBLE)

> **6-Model Multi-Seed Ensemble (3x DenseNet-121 @ 512 + 3x ConvNeXt-Tiny @ 1024)**

---

### 📊 Test Set Performance (Test-132, N = 132)

| Metric | Score | Note |
| :--- | :---: | :--- |
| **Macro-F1** | **`0.7496`** (~75.0%) | Primary Ranking Metric |
| **BCD-F1** | **`0.7478`** | Dense Classes (B, C, D) |
| **Quadratic Weighted Kappa (QWK)** | **`0.7749`** | Ordinal Agreement |
| **Accuracy** | **`71.21%`** | Exact 4-Class Match |

#### 📈 Per-Class F1-Score Breakdown:
* **Class A (Almost Entirely Fatty):** `0.8571`
* **Class B (Scattered Fibroglandular):** `0.7273`
* **Class C (Heterogeneously Dense):** `0.6783`
* **Class D (Extremely Dense):** `0.7356`

---

### 💡 Architecture & Ensembling
* **E3 Group (10% weight):** 3 seeds (42, 43, 44) of DenseNet-121 @ 512x512 with Bilateral Contralateral Region Attention.
* **E7 Group (90% weight):** 3 seeds (42, 43, 44) of ConvNeXt-Tiny @ 1024x1024 with Bilateral Fusion.
* **Formula:** `P_final = 0.10 * mean(P_E3_seeds) + 0.90 * mean(P_E7_seeds)`

---

### 🚀 Quickstart (Inference)
```bash
python3 inference.py --config config/config.yaml --output-dir outputs/inference_results
```

---

### 🔍 Preprocessing Modules (`src/tn_mammo/data/`)

Tất cả các module tiền xử lý ảnh mammo hoàn chỉnh được đóng gói độc lập trong từng package:

1. **`dicom_dataset.py` (DICOM-Native Pipeline):**
   * Đọc trực tiếp DICOM raw 12-bit / 16-bit qua `pydicom`.
   * Áp dụng chuyển đổi cửa sổ VOI LUT (`apply_voi_lut`).
   * Tự động phát hiện và đảo cực tính ảnh âm bản (`MONOCHROME1` → `MONOCHROME2`).
   * Phân đoạn vùng nhu mô vú tự động bằng phân ngưỡng Otsu (`cv2.threshold`).
   * Cắt bounding box bám sát vùng tuyến vú với padding biên thích ứng.
   * Cân bằng độ tương phản thích ứng cục bộ CLAHE (`clipLimit=2.0, tileGridSize=(8, 8)`).
   * Resize song tuyến tính khử răng cưa (`TF.InterpolationMode.BILINEAR`, `antialias=True`).
   * Chuẩn hóa thống kê ImageNet (`mean=[0.485, 0.456, 0.406]`, `std=[0.229, 0.224, 0.225]`).

2. **`preprocessing.py` (P2 Aspect-Preserving CLAHE):**
   * Thuật toán `preprocess_P2`: Scale đồng tỉ lệ bảo toàn hình học tuyến vú (không méo ảnh).
   * Padding viền nền có kiểm soát canvas và sinh mặt nạ hợp lệ `valid_mask`.
   * Tăng cường tương phản cục bộ CLAHE.

3. **`pectoral_removal.py` (Pectoral Muscle Segmentation):**
   * Bóc tách cơ ngực lớn trên góc phần tư trên của view MLO bằng biến đổi Hough (`skimage.transform.hough_line`).
   * Bộ lọc kiểm tra tính hợp lý giải phẫu (`_pectoral_plausible`) tránh cắt lẹm vào nhu mô tuyến vú.

4. **`contracts.py` & `jpeg_dataset.py`:**
   * Quy chuẩn cấu trúc dữ liệu 4 view chuẩn lâm sàng (`L_CC`, `L_MLO`, `R_CC`, `R_MLO`).
   * Adapter xử lý tương thích cho cả dữ liệu ảnh xuất định dạng JPEG/PNG.
