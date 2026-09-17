"""DICOM-native four-view mammography dataset.

Replaces the original PhaseGDatasetAdapter by reading DICOM files
directly via pydicom, instead of relying on pre-converted JPG/PNG
images and the legacy phaseG_rerun code.

Pipeline per image:
    1. Read DICOM pixel_array (uint16, 12-bit stored)
    2. Apply MONOCHROME1 inversion if needed
    3. Normalize to float32 [0, 1]
    4. Resize to (image_size, image_size)
    5. Replicate grayscale → 3-channel RGB
    6. Apply optional augmentation (train only)
    7. Normalize with ImageNet statistics
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

import cv2
import numpy as np
import pandas as pd
import pydicom
import torch
from torch.utils.data import Dataset
from torchvision import transforms
from torchvision.transforms import functional as TF

from tn_mammo.constants import (
    LABEL_TO_INDEX,
    VIEW_ORDER,
)


# DICOM view filenames inside each case directory
VIEW_FILES_LEGACY: dict[str, str] = {
    "L_CC": "Left - CC.dcm",
    "L_MLO": "Left - MLO.dcm",
    "R_CC": "Right - CC.dcm",
    "R_MLO": "Right - MLO.dcm",
}

VIEW_FILES_BREAST_ONLY: dict[str, str] = {
    "L_CC": "L_CC.dcm",
    "L_MLO": "L_MLO.dcm",
    "R_CC": "R_CC.dcm",
    "R_MLO": "R_MLO.dcm",
}

# ImageNet normalization statistics
IMAGENET_MEAN = [0.485, 0.456, 0.406]
IMAGENET_STD = [0.229, 0.224, 0.225]


def read_dicom_as_tensor(
    dicom_path: str | Path,
    image_size: int,
) -> torch.Tensor:
    """Read a DICOM file and return a [3, H, W] float32 tensor.

    Steps:
        1. Read pixel_array from DICOM
        2. Handle MONOCHROME1 (invert)
        3. Normalize to [0, 1] float32
        4. Resize to image_size x image_size
        5. Replicate to 3 channels
    """
    try:
        dcm = pydicom.dcmread(
            str(dicom_path),
            force=True,
        )
        if not hasattr(dcm, "file_meta"):
            dcm.file_meta = pydicom.dataset.FileMetaDataset()
        if not hasattr(dcm.file_meta, "TransferSyntaxUID") or not dcm.file_meta.TransferSyntaxUID:
            dcm.file_meta.TransferSyntaxUID = pydicom.uid.ImplicitVRLittleEndian

        from pydicom.pixel_data_handlers.util import apply_voi_lut
        arr = apply_voi_lut(dcm.pixel_array, dcm)
        pixel_array = arr.astype(
            np.float32
        )

        # Handle MONOCHROME1 (white = low value)
        photometric = getattr(
            dcm,
            "PhotometricInterpretation",
            "MONOCHROME2",
        )

        if photometric == "MONOCHROME1":
            pixel_array = pixel_array.max() - pixel_array

        # 1. Normalize to uint8 for cv2 processing
        pmin = pixel_array.min()
        pmax = pixel_array.max()
        if pmax > pmin:
            img_8u = ((pixel_array - pmin) / (pmax - pmin) * 255).astype(np.uint8)
        else:
            img_8u = np.zeros_like(pixel_array, dtype=np.uint8)
        
        # 2. Otsu Threshold to find mask
        _, thresh = cv2.threshold(img_8u, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # 3. Find largest contour (breast)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(largest_contour)
            
            # Optional: add a small padding
            pad = 10
            x_start = max(0, x - pad)
            y_start = max(0, y - pad)
            x_end = min(img_8u.shape[1], x + w + pad)
            y_end = min(img_8u.shape[0], y + h + pad)
            
            cropped = img_8u[y_start:y_end, x_start:x_end]
        else:
            cropped = img_8u
            
        # 4. CLAHE for contrast enhancement
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(cropped)
        
        # 5. Normalize back to [0, 1] float32
        pixel_array = enhanced.astype(np.float32) / 255.0

        # Convert to torch tensor [1, H, W]
        tensor = torch.from_numpy(
            pixel_array
        ).unsqueeze(0)

    except Exception as e:
        import logging
        logging.getLogger(__name__).error(
            f"Failed to decode DICOM ({dicom_path}): {e}"
        )
        raise e

    # Resize to target size
    tensor = TF.resize(
        tensor,
        [image_size, image_size],
        interpolation=TF.InterpolationMode.BILINEAR,
        antialias=True,
    )

    # Replicate grayscale → 3-channel
    tensor = tensor.expand(3, -1, -1).clone()

    return tensor



def build_train_augmentation(
    image_size: int,
) -> transforms.Compose:
    """Training augmentation pipeline matching the original Phase-G setup."""
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


def build_eval_augmentation() -> transforms.Compose:
    """Evaluation-time normalization only."""
    return transforms.Compose([
        transforms.Normalize(
            mean=IMAGENET_MEAN,
            std=IMAGENET_STD,
        ),
    ])


class DicomFourViewDataset(Dataset):
    """DICOM-native four-view mammography dataset.

    Each sample is a dict with:
        - "views": [4, 3, H, W] float32 tensor
        - "label": scalar int64 tensor
        - "case_id": string
        - "source": string (domain)
    """

    def __init__(
        self,
        manifest_path: str | Path,
        dicom_root: str | Path,
        *,
        image_size: int,
        training: bool,
        source_representation: str = "legacy",
    ) -> None:
        self.manifest_path = Path(
            manifest_path
        )
        self.dicom_root = Path(dicom_root)
        self.image_size = int(image_size)
        self.training = bool(training)
        self.source_representation = source_representation

        if self.source_representation == "breast_only_dicom":
            self.view_filenames = VIEW_FILES_BREAST_ONLY
        else:
            self.view_filenames = VIEW_FILES_LEGACY

        if not self.manifest_path.exists():
            raise FileNotFoundError(
                f"Manifest not found: "
                f"{self.manifest_path}"
            )

        if not self.dicom_root.exists():
            raise FileNotFoundError(
                f"DICOM root not found: "
                f"{self.dicom_root}"
            )

        self.dataframe = pd.read_csv(
            self.manifest_path
        )

        # Build augmentation transforms
        if self.training:
            self.transform = (
                build_train_augmentation(
                    self.image_size
                )
            )
        else:
            self.transform = (
                build_eval_augmentation()
            )

        # Validate all cases have DICOM files
        self._validate_dicom_availability()

    def _validate_dicom_availability(
        self,
    ) -> None:
        """Check that all cases in manifest have DICOM files."""
        missing = []

        for idx in range(len(self.dataframe)):
            row = self.dataframe.iloc[idx]
            case_id = str(row["case_id"])
            case_dir = (
                self.dicom_root / case_id
            )

            if not case_dir.is_dir():
                missing.append(case_id)
                continue

            for view_name in VIEW_ORDER:
                filename = self.view_filenames[view_name]
                dcm_path = case_dir / filename
                if not dcm_path.is_file():
                    missing.append(
                        f"{case_id}/{view_name}"
                    )

        if missing:
            raise FileNotFoundError(
                f"Missing DICOM files for "
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
        case_dir = self.dicom_root / case_id

        # Read four DICOM views
        view_tensors = []

        for view_name in VIEW_ORDER:
            dcm_path = (
                case_dir
                / self.view_filenames[
                    view_name
                ]
            )

            tensor = read_dicom_as_tensor(
                dcm_path,
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
