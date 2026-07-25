# TN-Mammo — Phân loại mật độ mô vú 4 lớp A/B/C/D (BI-RADS density)

Model E1 tốt nhất hiện tại: **Macro-F1 = 0.7022** trên tập test khóa TN-Mammo 132 ca.

## 1. Bài toán

Cho MỘT ca chụp nhũ ảnh gồm đủ 4 view: L-CC, L-MLO, R-CC, R-MLO (vú trái/phải,
mỗi bên 2 góc chụp), phân loại mật độ mô vú của bệnh nhân vào đúng một trong
4 mức BI-RADS:

    A — gần như toàn mỡ            C — mô dày không đồng nhất
    B — mô sợi-tuyến rải rác       D — mô cực kỳ dày

Điểm khó:

1. **Mất cân bằng lớp** (A rất hiếm) → chỉ số chính là Macro-F1, loss dùng
   class-balanced focal.
2. **Nhãn có thứ tự** A < B < C < D → thêm loss ordinal CORAL phụ trợ
   (chỉ dùng lúc train).
3. **Dữ liệu TN-Mammo ít** (411 ca train) → train trộn thêm VinDr (3975 ca),
   sampler giữ 60% mass cho domain TN.

## 2. Kiến trúc (E1)

```text
L-CC ─┐
L-MLO ┤   DenseNet121 (chia sẻ trọng số)      mean fusion
R-CC  ┼──> encode từng view ──> [B,4,1024] ──> trái=(v1+v2)/2 ──┐
R-MLO ┘        224x224                         phải=(v3+v4)/2   │
                                               exam=(trái+phải)/2
                                                    [B,1024]
                                      ┌─────────────┴─────────────┐
                                      ▼                           ▼
                             Flat head Linear(1024,4)    CORAL head (3 ngưỡng)
                             => argmax => A/B/C/D        chỉ tính loss lúc train
                             (DỰ ĐOÁN CUỐI CÙNG)         (KHÔNG dùng để decode)

Loss = ClassBalancedFocal(flat) + 0.5 * coral_loss(ordinal)
```

Kết quả test khóa TN-Mammo (132 ca — đã "đốt", không dùng lại để chọn model):

    Macro-F1 0.7022 | Acc 0.6818 | BalAcc 0.7454 | QWK 0.7643
    Within-one 1.0000 | Lỗi nghiêm trọng (lệch >= 2 bậc): 0
    Confusion: [[4,0,0,0],[2,15,9,0],[0,8,37,12],[0,0,11,34]]

## 3. Cấu trúc thư mục

```text
.
├── train.py                    # CLI train
├── evaluate.py                 # CLI đánh giá checkpoint
├── config.yaml                 # config của run E1 đã chọn
├── checkpoint/best_model.pt    # checkpoint E1 (Macro-F1 0.7022)
├── fusion_experiment_plan.md   # kế hoạch thí nghiệm fusion (đọc mục 6)
├── fusion_config_snippet.yaml  # snippet config cho các fusion mới
└── src/tn_mammo/
    ├── constants.py            # VIEW_ORDER, nhãn, kích thước feature
    ├── data/
    │   ├── contracts.py        # nhãn ordinal CORAL, nhãn binary, decode
    │   ├── transforms.py       # SquarePad + pipeline biến đổi ảnh
    │   ├── dataset.py          # FourViewManifestDataset (đọc manifest CSV)
    │   └── sampler.py          # sampler trộn domain TN/VinDr
    ├── models/density_model.py # FourViewDensityModel (DenseNet121 + 2 head)
    ├── losses/multitask.py     # class-balanced focal + CORAL (λ=0.5)
    ├── metrics/classification.py  # Macro-F1, QWK, within-one, severe...
    ├── training/engine.py      # vòng lặp train/validate, early stopping
    ├── utils/seeding.py        # seed_everything, seed_worker
    └── inference.py            # run_eval: đánh giá checkpoint
```

## 4. Cài đặt và chạy

Yêu cầu: Python ≥ 3.10, PyTorch + torchvision (bản CUDA phù hợp GPU),
và các gói:

```bash
pip install coral-pytorch pandas scikit-learn pyyaml pillow
```

### Manifest CSV

Mỗi dòng là một ca chụp, cần cột:

```text
case_id, label, L_CC, L_MLO, R_CC, R_MLO, [source]
```

- `label`: A/B/C/D; `source`: TN hoặc VinDr (mặc định TN nếu thiếu).
- Đường dẫn ảnh tuyệt đối, hoặc tương đối so với vị trí file manifest.
- Dataset sẽ tự kiểm tra: đủ cột, không trùng `case_id`, label hợp lệ,
  file ảnh tồn tại — lỗi sẽ báo ngay trước khi train.

### Train

```bash
python train.py --config config.yaml --output-dir outputs/run1
```

Config cần các khối `experiment` (seed), `data` (manifest + `tn_domain_ratio`),
`model`, `loss`, `training` — xem `config.yaml` làm mẫu. Checkpoint tốt nhất
theo **validation Macro-F1** được lưu tại `outputs/run1/best_checkpoint.pt`
(kèm optimizer/scheduler/scaler state để resume).

### Đánh giá

```bash
python evaluate.py --checkpoint checkpoint/best_model.pt --manifest valid.csv
```

In JSON gồm: accuracy, balanced accuracy, Macro-F1, QWK, within-one,
severe-error count, confusion matrix và per-class P/R/F1.

## 5. Nguyên tắc đánh giá — ĐỌC TRƯỚC KHI CHẠY THÍ NGHIỆM

- Tập test khóa TN-Mammo 132 ca **đã được đánh giá đúng một lần** (kết quả ở
  mục 2) và được coi là "đã đốt": **không dùng lại** để chọn model, chọn
  hyperparameter, calibrate hay tune threshold dưới bất kỳ hình thức nào.
- Mọi lựa chọn (fusion, resolution, data strategy, seed) chỉ dựa trên
  **validation Macro-F1**.
- Metric phụ để theo dõi: balanced accuracy, QWK, per-class F1, within-one,
  severe-error count.

## 6. Làm thí nghiệm fusion theo kế hoạch

Kế hoạch đầy đủ ở [`fusion_experiment_plan.md`](fusion_experiment_plan.md).
Tóm tắt lộ trình và cách bám theo:

| Phase | Việc cần làm | Điều kiện chuyển phase |
|---|---|---|
| **A — Sanity** | Chạy mỗi fusion 1 epoch, dữ liệu nhỏ, seed 42 | Không lỗi shape, loss hữu hạn, `flat_logits [B,4]`, `ordinal_logits [B,3]`, checkpoint load/eval được |
| **B — Screening** | 4 fusion (`mean`, `concat_mlp`, `attention`, `hierarchical_gated`) tại 224, seeds 42/52/62 | Shortlist fusion có Macro-F1 trung bình > baseline, không giảm QWK, không tăng severe, cải thiện ở ≥ 2/3 seed |
| **C — Resolution** | Top-2 fusion (gồm `mean`) tại 224/384/512, giữ effective batch tương đương | Chọn resolution theo Macro-F1/QWK, độ ổn định giữa seed, VRAM và thời gian |
| **D — Ablation** | Nếu `hierarchical_gated` thắng: tách vai trò CC-MLO (ipsilateral) và trái-phải (bilateral) | Hiểu được thành phần nào đóng góp |
| **E — Data strategy** | TN-only vs TN+VinDr tự nhiên vs target-aware 0.6 (thử 0.5/0.7 nếu cần) | Chốt chiến lược dữ liệu |

Quy trình cho MỖI run:

1. Copy `config.yaml`, chỉ đổi đúng nhóm yếu tố của phase đó (ví dụ Phase B
   chỉ đổi `model.fusion` — thêm các trường từ `fusion_config_snippet.yaml`).
2. Đặt tên output dir có ý nghĩa: `outputs/F3_hierarchical_seed42/`...
3. Chạy đủ seed quy định (baseline và model cuối: ≥ 3 seed).
4. Lưu prediction validation theo `case_id` để paired bootstrap về sau.
5. Báo cáo `mean ± std` Macro-F1/QWK/BalAcc, kèm số tham số, thời gian
   epoch và peak VRAM (bảng mẫu ở mục 10 của plan).

**Lưu ý hiện trạng code**: `src/tn_mammo/models/density_model.py` hiện chỉ có
`mean` fusion. Trước khi vào Phase A cần thêm `models/fusion.py` cài
`concat_mlp`, `attention`, `hierarchical_gated` theo interface của
`fusion_config_snippet.yaml` (`fusion`, `fusion_hidden_dim`, `fusion_dropout`)
và cho `FourViewDensityModel` nhận tham số này từ config. Các bản cài đặt
tham khảo của phiên bản trước (parameter-matched MLP, ipsilateral, bilateral
gated) xem trong git history: `git show f9fa7e1:tn-mammo-bestmacro-hientai/src/tn_mammo/models/fusion.py`.

Chỉ sau khi fusion + resolution + protocol chọn model **đã khóa hoàn toàn**
từ validation mới được nghĩ đến việc chạy test cuối (một lần duy nhất).

## 7. Ghi chú lịch sử

- Package `src/tn_mammo/` hiện tại là bản module hóa từ
  `tn_mammo_onepage_fixed.py`, đã kiểm chứng tương thích ngược: checkpoint E1
  load `strict=True`, logits bit-exact, hai chiều load checkpoint cũ/mới.
- Bản code gốc phong cách server (kèm audit test khóa SHA256, marker một lần)
  nằm ở các commit trước — xem `git log` với các file `train.py`,
  `inference.py`, `src/tn_mammo/` cũ.
- `DESCRIPTION.md` giữ mô tả gói E1 và kết quả test khóa lịch sử.

<- Seed: POST_E1_R1_R6_PACKAGE -->

## Post-E1 research package: R1-R6

| Branch | Method | Strict OOF Macro-F1 | Exploratory test Macro-F1 | Decision |
|---|---|---:|---:|---|
| E1 | Shared DenseNet121, four-view mean fusion, flat + CORAL heads | 0.563267 | **0.702155** | Official model |
| R1 | OOF logit calibration | 0.569545 | Not promoted | Rejected |
| R2 | Fold-specific C/D logistic specialist | 0.574876 | 0.669728 | Rejected |
| R3 | Mixture of Experts | 0.572962 | 0.702155 | No gain |
| R4 | Dynamic Ensemble Selection | 0.567641 | 0.687899 | Rejected |
| R5 | Stacking | **0.580841** | 0.702155 | No gain |
| R6 | Selective Classification | 0.571333 | 0.669728 | Rejected |

### Packaged trained artifacts

- E1 official PyTorch checkpoint: `checkpoint/E1/best_checkpoint.pt`.
- Fifteen R2 C/D specialists: `checkpoint/R2_cd_specialists/seedXX_foldY/`.
- R3 Mixture-of-Experts gate: `checkpoint/R3_R6/R3_final_gate.joblib`.
- R5 stacking classifier: `checkpoint/R3_R6/R5_final_stacking.joblib`.
- Frozen R3-R6 parameters and report are stored in `checkpoint/R3_R6/`.

### Research implementation files

| File | Responsibility |
|---|---|
| `research/R1_calibration/r1_strict_oof5x3_20260724_181205__run_r1_strict_oof.py` | Runs strict five-fold × three-seed R1 calibration experiments. |
| `research/R1_calibration/r1_strict_oof5x3_20260724_181205__finalize_existing_oof.py` | Aggregates OOF predictions, computes bootstrap stability and applies the promotion gate. |
| `research/R2_cd_specialist/run_r2_strict_specialist.py` | Trains and evaluates fifteen fold-specific C/D logistic specialists. |
| `research/R3_R6_ensemble_management/run_r3_r6.py` | Implements Mixture of Experts, Dynamic Ensemble Selection, Stacking and Selective Classification. |

The R2-R6 locked-test comparisons are exploratory. E1 remains the authoritative model.
