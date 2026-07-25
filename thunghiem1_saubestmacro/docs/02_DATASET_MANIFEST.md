# Dataset loader và manifest

## Code chính

```text
filecode1/src/tn_mammo/data/dataset.py
filecode1/src/tn_mammo/data/sampler.py
filecode1/src/tn_mammo/data/contracts.py
```

## `FourViewManifestDataset`

Loader kiểm tra:

- Manifest tồn tại và không rỗng.
- Có `case_id` và `label`.
- `case_id` không thiếu và không trùng.
- Label thuộc A/B/C/D.
- Đủ bốn đường dẫn ảnh.
- Tất cả file ảnh tồn tại trước khi train.

Loader nhận được cả hai schema:

| Schema package | Schema Phase-G |
|---|---|
| `L_CC` | `left_cc_path` |
| `L_MLO` | `left_mlo_path` |
| `R_CC` | `right_cc_path` |
| `R_MLO` | `right_mlo_path` |

Đường dẫn tương đối được resolve theo folder chứa manifest. Đường dẫn tuyệt đối
được giữ nguyên sau khi resolve.

Mỗi sample trả về:

```python
{
    "views": Tensor[4, 3, H, W],
    "label": int,
    "case_id": str,
    "source": str,
}
```

## Manifest đã dùng

```text
/mnt/hcmus/breast_vn/code/new_implement/manifests/phaseg_tn_train411.csv
/mnt/hcmus/breast_vn/code/new_implement/manifests/phaseg_vindr_train3975.csv
/mnt/hcmus/breast_vn/code/new_implement/manifests/phaseg_tn_valid133.csv
```

Quy mô:

- TN train: 411 ca.
- VinDr train: 3,975 ca.
- TN validation: 133 ca.

## Domain sampler

`build_domain_sampler` tạo `WeightedRandomSampler` sao cho tổng sampling mass:

- TN: 60%.
- Ngoài TN/VinDr: 40%.

Mỗi epoch sample 4,386 ca có replacement.
