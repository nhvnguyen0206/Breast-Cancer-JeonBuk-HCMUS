"""JPEG four-view mammography dataset.

Reads pre-converted JPEG images from paths stored in the manifest CSV.
Same output API as DicomFourViewDataset: returns {views, label, case_id, source}.

Manifest columns:
    case_id, split, domain, source, label, label_idx,
    left_cc_path, left_mlo_path, right_cc_path, right_mlo_path
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np
import torch
from PIL import Image
from torch.utils.data import Dataset
from torchvision import transforms
from torchvision.transforms import functional as TF

import pandas as pd

from tn_mammo.constants import (
    LABEL_TO_INDEX,
    VIEW_ORDER,
)


# JPEG column names mapping to VIEW_ORDER
JPEG_VIEW_COLUMNS: dict[str, str] = {
    "L_CC": "left_cc_path",
    "L_MLO": "left_mlo_path",
    "R_CC": "right_cc_path",
    "R_MLO": "right_mlo_path",
}

# ImageNet normalization statistics
IMAGENET_MEAN = [0.485, 0.456, 0.406]
IMAGENET_STD = [0.229, 0.224, 0.225]


def read_jpeg_as_tensor(
    jpeg_path: str | Path,
    image_size: int,
) -> torch.Tensor:
    """Read a JPEG file and return a [3, H, W] float32 tensor.

    Steps:
        1. Open JPEG with PIL (RGB)
        2. Resize to image_size x image_size
        3. Convert to float32 tensor [0, 1]
    """
    try:
        image = Image.open(str(jpeg_path)).convert("RGB")

        tensor = TF.to_tensor(image)  # [3, H, W] float32 [0,1]

        tensor = TF.resize(
            tensor,
            [image_size, image_size],
            interpolation=TF.InterpolationMode.BILINEAR,
            antialias=True,
        )

    except Exception as e:
        print(
            f"[WARNING] Corrupted JPEG skipped "
            f"({jpeg_path}): {e}"
        )
        tensor = torch.zeros(
            (3, image_size, image_size),
            dtype=torch.float32,
        )

    return tensor


def build_jpeg_train_augmentation(
    image_size: int,
) -> transforms.Compose:
    """Training augmentation pipeline."""
    return transforms.Compose([
        transforms.RandomHorizontalFlip(p=0.5),
        transforms.RandomVerticalFlip(p=0.5),
        transforms.RandomAffine(
            degrees=10,
            translate=(0.05, 0.05),
            scale=(0.9, 1.1),
        ),
        transforms.ColorJitter(
            brightness=0.1,
            contrast=0.1,
        ),
        transforms.Normalize(
            mean=IMAGENET_MEAN,
            std=IMAGENET_STD,
        ),
    ])


def build_jpeg_eval_augmentation() -> transforms.Compose:
    """Evaluation-time normalization only."""
    return transforms.Compose([
        transforms.Normalize(
            mean=IMAGENET_MEAN,
            std=IMAGENET_STD,
        ),
    ])


class JpegFourViewDataset(Dataset):
    """JPEG four-view mammography dataset.

    Each sample is a dict with:
        - "views": [4, 3, H, W] float32 tensor
        - "label": scalar int64 tensor
        - "case_id": string
        - "source": string (domain)
    """

    def __init__(
        self,
        manifest_path: str | Path,
        *,
        image_size: int,
        training: bool,
    ) -> None:
        self.manifest_path = Path(
            manifest_path
        )
        self.image_size = int(image_size)
        self.training = bool(training)

        # For compatibility with engine.dataset_summary
        self.dicom_root = Path("N/A_JPEG_MODE")

        if not self.manifest_path.exists():
            raise FileNotFoundError(
                f"Manifest not found: "
                f"{self.manifest_path}"
            )

        self.dataframe = pd.read_csv(
            self.manifest_path
        )

        # Validate required columns
        required_cols = list(
            JPEG_VIEW_COLUMNS.values()
        )
        missing_cols = [
            col
            for col in required_cols
            if col not in self.dataframe.columns
        ]
        if missing_cols:
            raise ValueError(
                f"Manifest missing columns: "
                f"{missing_cols}"
            )

        if self.training:
            self.transform = (
                build_jpeg_train_augmentation(
                    self.image_size
                )
            )
        else:
            self.transform = (
                build_jpeg_eval_augmentation()
            )

        # Validate all JPEG files exist
        self._validate_jpeg_availability()

    def _validate_jpeg_availability(
        self,
    ) -> None:
        """Check that all cases have JPEG files."""
        missing = []

        for idx in range(len(self.dataframe)):
            row = self.dataframe.iloc[idx]
            for view_name in VIEW_ORDER:
                col = JPEG_VIEW_COLUMNS[view_name]
                jpeg_path = str(row[col])
                if not Path(jpeg_path).exists():
                    missing.append(
                        f"{row['case_id']}/{view_name}: "
                        f"{jpeg_path}"
                    )

        if missing:
            raise FileNotFoundError(
                f"Missing JPEG files for "
                f"{len(missing)} entries: "
                f"{missing[:10]}"
            )

    def __len__(self) -> int:
        return len(self.dataframe)

    def __getitem__(
        self,
        index: int,
    ) -> dict[str, Any]:
        row = self.dataframe.iloc[index]
        case_id = str(row["case_id"])

        # Read four JPEG views
        view_tensors = []

        for view_name in VIEW_ORDER:
            col = JPEG_VIEW_COLUMNS[view_name]
            jpeg_path = str(row[col])

            tensor = read_jpeg_as_tensor(
                jpeg_path,
                self.image_size,
            )

            # Apply augmentation/normalization
            tensor = self.transform(tensor)
            view_tensors.append(tensor)

        # Stack to [4, 3, H, W]
        views = torch.stack(
            view_tensors,
            dim=0,
        )

        # Get label
        label_raw = row.get(
            "label",
            row.get("label_idx", None),
        )

        if isinstance(label_raw, str):
            label_raw = label_raw.strip()

        if label_raw in LABEL_TO_INDEX:
            label_idx = LABEL_TO_INDEX[
                label_raw
            ]
        else:
            label_idx = int(label_raw)

        label = torch.tensor(
            label_idx,
            dtype=torch.long,
        )

        # Get source/domain
        source = str(
            row.get(
                "domain",
                row.get("source", "TN"),
            )
        )

        return {
            "views": views,
            "label": label,
            "case_id": case_id,
            "source": source,
        }
