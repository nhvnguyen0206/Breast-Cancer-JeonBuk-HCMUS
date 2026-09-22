"""Four-view DICOM or frozen window16 tensor input, with ImageNet normalization."""
from pathlib import Path
import cv2
import numpy as np
import pandas as pd
import pydicom
from pydicom.pixels import apply_voi_lut
import torch
from torch.utils.data import Dataset
from torchvision.transforms import InterpolationMode
from torchvision.transforms.functional import affine

VIEWS = ("L_CC", "L_MLO", "R_CC", "R_MLO")
LABELS = {name: i for i, name in enumerate("ABCD")}


def augment_views(views, options=None):
    """Apply one mild transform consistently to all views in an exam."""
    options = {} if options is None else dict(options)
    allowed = {"brightness_min", "brightness_max", "rotation_degrees",
               "translation_fraction"}
    unknown = set(options) - allowed
    if unknown:
        raise ValueError(f"Unknown augmentation options: {sorted(unknown)}")
    low = float(options.get("brightness_min", 0.9))
    high = float(options.get("brightness_max", 1.1))
    degrees = float(options.get("rotation_degrees", 0.0))
    fraction = float(options.get("translation_fraction", 0.0))
    if not 0 < low <= high or not 0 <= degrees <= 15 or not 0 <= fraction <= 0.1:
        raise ValueError("Invalid augmentation range")
    # Keep the original random draw and brightness behavior when no options are supplied.
    views = (views * (low + (high - low) * torch.rand(()))).clamp(0, 1)
    if degrees or fraction:
        angle = float((2 * torch.rand(()) - 1) * degrees)
        height, width = views.shape[-2:]
        tx = round(float((2 * torch.rand(()) - 1) * fraction * width))
        ty = round(float((2 * torch.rand(()) - 1) * fraction * height))
        views = affine(views, angle=angle, translate=[tx, ty], scale=1.0,
                       shear=[0.0, 0.0], interpolation=InterpolationMode.BILINEAR,
                       fill=0.0).clamp(0, 1)
    return views


def resize_cache(image, size, mode="stretch"):
    if mode == "stretch":
        return cv2.resize(image, (size, size), interpolation=cv2.INTER_AREA)
    if mode != "letterbox":
        raise ValueError(f"Unsupported resize mode: {mode}")
    height, width = image.shape
    scale = size / max(height, width)
    h, w = max(1, round(height * scale)), max(1, round(width * scale))
    resized = cv2.resize(image, (w, h), interpolation=cv2.INTER_AREA)
    padded = np.zeros((size, size), dtype=image.dtype)
    top, left = (size - h) // 2, (size - w) // 2
    padded[top:top+h, left:left+w] = resized
    return padded


def read_cache(path, size, resize_mode="stretch"):
    """Read frozen float32 cache without repeating DICOM windowing or CLAHE."""
    path = Path(path)
    if not path.name.endswith("_a.npy"):
        raise ValueError("Cache image filename must end with _a.npy")
    prefix = str(path)[:-6]
    image = np.load(path, allow_pickle=False)
    shape = np.load(prefix + "_s.npy", allow_pickle=False)
    packed = np.load(prefix + "_m.npy", allow_pickle=False)
    if shape.dtype != np.int32 or shape.shape != (2,) or (shape <= 0).any():
        raise ValueError(f"Invalid cache mask shape: {path}")
    count = int(np.prod(shape.astype(np.int64)))
    if packed.dtype != np.uint8 or packed.ndim != 1 or packed.size != (count + 7) // 8:
        raise ValueError(f"Invalid packed mask: {path}")
    mask = np.unpackbits(packed, bitorder="big", count=count).reshape(tuple(shape)).astype(bool)
    if (image.dtype != np.float32 or image.shape != mask.shape or
            not np.isfinite(image).all() or image.min() < 0 or image.max() > 1 or
            np.any(image[~mask] != 0) or not mask.any()):
        raise ValueError(f"Invalid cache pixels: {path}")
    image = resize_cache(image, size, resize_mode)
    return torch.from_numpy(image).repeat(3, 1, 1)


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
    def __init__(self, manifest, image_size=512, training=False, require_labels=True, input_mode="dicom",
                 resize_mode="stretch", augmentation=None):
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
        if input_mode not in ("dicom", "window16_cache"):
            raise ValueError(f"Unsupported input_mode: {input_mode}")
        self.input_mode = input_mode
        if resize_mode not in ("stretch", "letterbox"):
            raise ValueError("Unsupported resize mode")
        if input_mode != "window16_cache" and resize_mode != "stretch":
            raise ValueError("Letterbox is currently supported only for frozen-cache inputs")
        self.resize_mode = resize_mode
        for _, row in self.frame.iterrows():
            paths = [str((manifest.parent / row[view]).resolve()) for view in VIEWS]
            if any(not row[v] for v in VIEWS) or any(not Path(p).is_file() for p in paths):
                raise FileNotFoundError(f"Four image files required for case {row.case_id}")
            self.paths.append(paths)
            if input_mode == "window16_cache":
                for p in paths:
                    if not p.endswith("_a.npy") or any(not Path(p[:-6] + suffix).is_file()
                                                      for suffix in ("_m.npy", "_s.npy")):
                        raise FileNotFoundError(f"Incomplete tensor cache: {p}")
        self.image_size, self.training = int(image_size), training
        self.augmentation = None if augmentation is None else dict(augmentation)
        # Validate once at construction without consuming training RNG.
        if self.augmentation is not None:
            probe = torch.zeros(4, 3, 32, 32)
            rng = torch.get_rng_state()
            try:
                augment_views(probe, self.augmentation)
            finally:
                torch.set_rng_state(rng)
        if self.image_size < 32:
            raise ValueError("image_size must be >= 32")

    def __len__(self):
        return len(self.frame)

    def __getitem__(self, index):
        views = torch.stack([read_cache(p, self.image_size, self.resize_mode)
                             if self.input_mode == "window16_cache" else read_dicom(p, self.image_size)
                             for p in self.paths[index]])
        if self.training:
            views = augment_views(views, self.augmentation)
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
