"""FIT-only mask-area retention diagnostic; does not evaluate model accuracy."""
import argparse
import json
from pathlib import Path

import cv2
import numpy as np
import pandas as pd
import torch
from torchvision.transforms import InterpolationMode
from torchvision.transforms.functional import affine


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("fit_csv")
    parser.add_argument("--studies", type=int, default=32)
    args = parser.parse_args()
    torch.set_num_threads(2)
    frame = pd.read_csv(args.fit_csv).sort_values("case_id")
    frame = frame.sample(n=min(args.studies, len(frame)), random_state=42)
    masks = []
    for _, row in frame.iterrows():
        for view in ("L_CC", "L_MLO", "R_CC", "R_MLO"):
            prefix = str(Path(row[view]))[:-6]
            shape = np.load(prefix + "_s.npy", allow_pickle=False)
            packed = np.load(prefix + "_m.npy", allow_pickle=False)
            mask = np.unpackbits(packed, bitorder="big", count=int(np.prod(shape)))
            mask = mask.reshape(tuple(shape)).astype(np.float32)
            masks.append(torch.from_numpy(cv2.resize(mask, (512, 512), interpolation=cv2.INTER_AREA)))
    masks = torch.stack(masks)[:, None]
    denominator = masks.sum((1, 2, 3))
    assert bool((denominator > 0).all())
    draws = torch.rand((16, 3), generator=torch.Generator().manual_seed(42)) * 2 - 1
    result = {"studies": len(frame), "views": len(masks), "draws_per_view": 16,
              "seed": 42, "fit_only": True, "metric": "transformed_mask_mass/original_mask_mass"}
    for name, degrees, fraction in (("parent", 5, .03), ("candidate", 10, .05),
                                     ("rotation_only_increase", 10, .03)):
        retention = []
        for draw in draws:
            transformed = affine(masks, angle=float(draw[0] * degrees),
                                 translate=[round(float(draw[1] * fraction * 512)),
                                            round(float(draw[2] * fraction * 512))],
                                 scale=1., shear=[0., 0.],
                                 interpolation=InterpolationMode.BILINEAR, fill=0.)
            retention.extend((transformed.sum((1, 2, 3)) / denominator).tolist())
        values = np.asarray(retention)
        result[name] = {"mean": float(values.mean()), "min": float(values.min()),
                        "p05": float(np.quantile(values, .05)),
                        "fraction_below_95pct": float((values < .95).mean())}
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
