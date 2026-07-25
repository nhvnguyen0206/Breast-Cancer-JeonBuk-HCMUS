# Report, biểu đồ và Grad-CAM

## File code

```text
filecode1/scripts/generate_report.py
```

## File PDF

```text
filecode1/tonghop.pdf
```

PDF gồm:

1. Bảng so sánh metric giữa baseline, 224, 384 và 512.
2. Training loss và validation curves.
3. Confusion matrix theo số lượng.
4. Confusion matrix normalized theo hàng.
5. ROC one-vs-rest và AUC từng lớp.
6. Heatmap precision/recall/F1 từng lớp.
7. Grad-CAM các ca đúng đại diện cho A/B/C/D.
8. Grad-CAM các ca sai, ưu tiên lỗi có khoảng cách thứ tự lớn.

## Grad-CAM

Grad-CAM dùng feature từ DenseNet `denseblock4`. Gradient được lấy theo logit
của lớp dự đoán. Mỗi trang hiển thị đủ bốn view với heatmap chồng lên ảnh đã
qua preprocessing validation.

Grad-CAM là công cụ giải thích định tính, không phải bằng chứng model đã học
đúng vùng giải phẫu. Cần kiểm tra bằng chuyên gia hoặc mask nếu muốn đánh giá
định lượng localization.

## Lệnh sinh lại PDF

Lệnh đầy đủ đã được khai báo ở cuối:

```text
filecode1/scripts/run_queue.sh
```

Script truyền bốn run vào `generate_report.py` và ghi log tại:

```text
filecode1/logs/report.log
```
