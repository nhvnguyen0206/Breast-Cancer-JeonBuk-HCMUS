"""DICOM input: VOI LUT, inversion, foreground crop, CLAHE, ImageNet normalization."""
from pathlib import Path
import cv2
import numpy as np
import pandas as pd
import pydicom
from pydicom.pixels import apply_voi_lut
import torch
from torch.utils.data import Dataset

VIEWS = ("L_CC", "L_MLO", "R_CC", "R_MLO")
LABELS = {name: i for i, name in enumerate("ABCD")}


def read_dicom(path, size):
    ds = pydicom.dcmread(path)
    array = np.asarray(apply_voi_lut(ds.pixel_array, ds), dtype=np.float32)
    if array.ndim != 2 or not np.isfinite(array).all():
        raise ValueError(f"Invalid grayscale DICOM: {path}")
    if ds.get("PhotometricInterpretation") == "MONOCHROME1":
        array = array.max() + array.min() - array
    span = float(array.max() - array.min())
    array = ((array - array.min()) / max(span, 1e-6) * 255).astype(np.uint8)
    _, mask = cv2.threshold(array, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        x, y, w, h = cv2.boundingRect(max(contours, key=cv2.contourArea))
        array = array[max(0, y-10):y+h+10, max(0, x-10):x+w+10]
    array = cv2.createCLAHE(clipLimit=2, tileGridSize=(8, 8)).apply(array)
    array = cv2.resize(array, (size, size), interpolation=cv2.INTER_LINEAR)
    return torch.from_numpy(array.astype(np.float32) / 255).repeat(3, 1, 1)


class FourViewDataset(Dataset):
    def __init__(self, manifest, image_size=512, training=False, require_labels=True):
        manifest = Path(manifest).resolve()
        self.frame = pd.read_csv(manifest, dtype=str).fillna("").reset_index(drop=True)
        required = {"case_id", *VIEWS} | ({"label"} if require_labels else set())
        if not required.issubset(self.frame.columns) or self.frame.empty:
            raise ValueError(f"Nonempty manifest requires columns {sorted(required)}")
        if self.frame.case_id.eq("").any() or self.frame.case_id.duplicated().any():
            raise ValueError("Empty or duplicate case_id")
        self.labels = None
        if "label" in self.frame:
            normalized = self.frame.label.str.strip().str.upper()
            if not normalized.isin(LABELS).all():
                raise ValueError("label must be A/B/C/D")
            self.labels = normalized.map(LABELS).to_numpy(dtype=np.int64)
        self.paths = []
        for _, row in self.frame.iterrows():
            paths = [str((manifest.parent / row[view]).resolve()) for view in VIEWS]
            if any(not row[v] for v in VIEWS) or any(not Path(p).is_file() for p in paths):
                raise FileNotFoundError(f"Four DICOM files required for case {row.case_id}")
            self.paths.append(paths)
        self.image_size, self.training = int(image_size), training
        if self.image_size < 32:
            raise ValueError("image_size must be >= 32")

    def __len__(self):
        return len(self.frame)

    def __getitem__(self, index):
        views = torch.stack([read_dicom(p, self.image_size) for p in self.paths[index]])
        if self.training:
            # Same mild photometric augmentation for all four views; orientation preserved.
            views = (views * (0.9 + 0.2 * torch.rand(()))).clamp(0, 1)
        mean = torch.tensor([.485, .456, .406])[None, :, None, None]
        std = torch.tensor([.229, .224, .225])[None, :, None, None]
        return {"views": (views - mean) / std, "case_id": self.frame.case_id.iloc[index],
                "label": int(self.labels[index]) if self.labels is not None else -1}


def assert_disjoint(train, valid):
    if set(train.frame.case_id) & set(valid.frame.case_id):
        raise ValueError("Train-validation case overlap")
    train_paths = {p for case in train.paths for p in case}
    if train_paths & {p for case in valid.paths for p in case}:
        raise ValueError("Train-validation image overlap")
