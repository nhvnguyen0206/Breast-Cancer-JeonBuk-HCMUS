import cv2
import numpy as np
import torch

def to_uint8(pixel_array: np.ndarray) -> np.ndarray:
    """Normalize pixel array to uint8."""
    pmin = pixel_array.min()
    pmax = pixel_array.max()
    if pmax > pmin:
        img_8u = ((pixel_array - pmin) / (pmax - pmin) * 255).astype(np.uint8)
    else:
        img_8u = np.zeros_like(pixel_array, dtype=np.uint8)
    return img_8u

def otsu_bbox(img_8u: np.ndarray) -> tuple[int, int, int, int]:
    """Find the bounding box of the breast using Otsu thresholding."""
    _, thresh = cv2.threshold(img_8u, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if not contours:
        return 0, 0, img_8u.shape[1], img_8u.shape[0]
        
    largest_contour = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(largest_contour)
    return x, y, x + w, y + h

def preprocess_P2(dicom_arr: np.ndarray, target: int = 512) -> np.ndarray:
    """
    Apply aspect-preserving crop, resize, deterministic padding, and CLAHE.
    This replaces the legacy square stretch approach.
    """
    img = to_uint8(dicom_arr)
    H, W = img.shape
    x0, y0, x1, y1 = otsu_bbox(img)
    
    bw, bh = x1 - x0, y1 - y0
    if bw <= 0 or bh <= 0:
        bw, bh = W, H
        x0, y0, x1, y1 = 0, 0, W, H
        
    px = int(np.ceil(0.05 * bw))
    py = int(np.ceil(0.05 * bh))
    
    x0c = max(0, x0 - px)
    x1c = min(W, x1 + px)
    y0c = max(0, y0 - py)
    y1c = min(H, y1 + py)
    
    crop = img[y0c:y1c, x0c:x1c]
    
    if crop.shape[0] == 0 or crop.shape[1] == 0:
        crop = img
        
    # Uniform scale - DO NOT stretch
    s = min(target / crop.shape[0], target / crop.shape[1])
    nH, nW = int(round(crop.shape[0] * s)), int(round(crop.shape[1] * s))
    
    # Ensure nH, nW are within target dimensions due to rounding
    nH = min(nH, target)
    nW = min(nW, target)
    
    if nH <= 0 or nW <= 0:
        # Fallback if scaling fails catastrophically
        nH, nW = target, target
        
    resized = cv2.resize(crop, (nW, nH), interpolation=cv2.INTER_AREA)
    
    canvas = np.zeros((target, target), dtype=resized.dtype)
    canvas[:nH, :nW] = resized
    
    # Create explicit valid mask
    valid_mask = np.zeros((target, target), dtype=bool)
    valid_mask[:nH, :nW] = True
    
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(canvas)
    
    return enhanced.astype(np.float32) / 255.0, valid_mask
