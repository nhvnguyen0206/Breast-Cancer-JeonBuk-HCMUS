# Preprocessing và augmentation bốn view

## Code chính

```text
filecode1/src/tn_mammo/data/transforms.py
```

Class chính: `SynchronizedFourViewTransform`.

## Pipeline validation/inference

Mỗi ca gồm đúng bốn ảnh theo thứ tự:

```text
L_CC, L_MLO, R_CC, R_MLO
```

Mỗi ảnh đi qua:

1. Chuyển sang RGB.
2. Tìm bounding box pixel grayscale lớn hơn ngưỡng nền đen.
3. Crop vùng giải phẫu, giữ margin 1% hoặc tối thiểu 4 pixel.
4. Lật cố định `R_CC` và `R_MLO` để chuẩn hóa orientation.
5. Pad ảnh thành hình vuông, không kéo méo tỷ lệ.
6. Resize về 224, 384 hoặc 512.
7. Chuyển tensor và normalize theo ImageNet mean/std.

Validation không có augmentation ngẫu nhiên.

## Pipeline training

Sau preprocessing, một bộ tham số ngẫu nhiên được sample một lần cho cả ca:

- Rotation: `[-5°, +5°]`.
- Translation: tối đa 3% kích thước ảnh theo mỗi trục.
- Gamma: `[0.9, 1.1]`.
- Contrast: `[0.9, 1.1]`.
- Gaussian noise: standard deviation `0.01`.

Rotation, translation, gamma và contrast dùng cùng giá trị cho cả bốn view.
Không có `RandomHorizontalFlip` ngẫu nhiên độc lập. Noise được tạo riêng trên
từng tensor nhưng cùng mức cường độ.

## Ý nghĩa

- Crop làm giảm vùng nền đen không mang thông tin.
- Pad trước resize giữ tỷ lệ giải phẫu.
- Orientation cố định tránh cùng cấu trúc trái/phải xuất hiện theo hai hướng.
- Đồng bộ geometric augmentation tránh phá quan hệ không gian giữa bốn view.

## Giới hạn cần ghi rõ

- Crop hiện dùng threshold nền, không phải segmentation model.
- Lật phải là quy tắc cố định dựa trên vị trí view, không tự phát hiện chest wall.
- Transform không dùng mask vùng vú.
- Chưa có ablation tách riêng đóng góp của crop, orientation và từng augmentation.
