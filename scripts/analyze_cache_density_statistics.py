"""Read-only breast-mask intensity diagnostic for fixed FIT/DEV manifests."""
import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd


VIEWS = ("L_CC", "L_MLO", "R_CC", "R_MLO")
FEATURES = ("mean", "std", "q10", "q25", "q50", "q75", "q90",
            "fraction_025", "fraction_050", "fraction_075", "mask_fraction")


def view_features(path):
    path = Path(path)
    prefix = str(path)[:-6]
    image = np.load(path, allow_pickle=False)
    shape = np.load(prefix + "_s.npy", allow_pickle=False)
    packed = np.load(prefix + "_m.npy", allow_pickle=False)
    count = int(np.prod(shape.astype(np.int64)))
    mask = np.unpackbits(
        packed, bitorder="big", count=count
    ).reshape(tuple(shape)).astype(bool)
    values = image[mask].astype(np.float64)
    quantiles = np.quantile(values, [.1, .25, .5, .75, .9])
    return np.asarray([
        values.mean(), values.std(), *quantiles,
        (values >= .25).mean(), (values >= .5).mean(),
        (values >= .75).mean(), mask.mean(),
    ])


def records(manifest, role):
    frame = pd.read_csv(manifest, dtype=str)
    frame = frame[frame.label.isin(["A", "B"])]
    result = []
    for row in frame.itertuples(index=False):
        values = np.stack([
            view_features(getattr(row, view)) for view in VIEWS
        ]).mean(axis=0)
        result.append({"role": role, "case_id": row.case_id, "label": row.label,
                       **dict(zip(FEATURES, map(float, values)))})
    return result


def describe(rows):
    matrix = np.asarray([[row[key] for key in FEATURES] for row in rows])
    return {
        key: {"min": float(matrix[:, index].min()),
              "median": float(np.median(matrix[:, index])),
              "max": float(matrix[:, index].max()),
              "mean": float(matrix[:, index].mean())}
        for index, key in enumerate(FEATURES)
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--fit", required=True)
    parser.add_argument("--dev", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    rows = records(args.fit, "fit") + records(args.dev, "dev")
    groups = {
        role + "_" + label: [row for row in rows
                              if row["role"] == role and row["label"] == label]
        for role in ("fit", "dev") for label in "AB"
    }
    if any(not group for group in groups.values()):
        raise ValueError("Both manifests must contain A and B cases")
    fit = np.asarray([[row[key] for key in FEATURES]
                      for row in groups["fit_A"] + groups["fit_B"]])
    center, scale = fit.mean(axis=0), fit.std(axis=0)
    scale[scale == 0] = 1
    standardized = {
        name: (np.asarray([[row[key] for key in FEATURES] for row in group])
               - center) / scale
        for name, group in groups.items()
    }
    centroid_a = standardized["fit_A"].mean(axis=0)
    centroid_b = standardized["fit_B"].mean(axis=0)
    dev_a = standardized["dev_A"]
    cases = []
    for row, vector in zip(groups["dev_A"], dev_a):
        cases.append({
            "case_id": row["case_id"],
            "features": {key: row[key] for key in FEATURES},
            "distance_to_fit_A_centroid": float(np.linalg.norm(vector - centroid_a)),
            "distance_to_fit_B_centroid": float(np.linalg.norm(vector - centroid_b)),
            "percentile_within_fit_A": {
                key: float((standardized["fit_A"][:, index] <= vector[index]).mean())
                for index, key in enumerate(FEATURES)
            },
            "percentile_within_fit_B": {
                key: float((standardized["fit_B"][:, index] <= vector[index]).mean())
                for index, key in enumerate(FEATURES)
            },
        })
    report = {
        "schema": "tn_mammo.cache_density_statistics.v1",
        "features": FEATURES,
        "counts": {name: len(group) for name, group in groups.items()},
        "summaries": {name: describe(group) for name, group in groups.items()},
        "dev_A_cases": cases,
        "limitations": [
            "Descriptive fixed-cache statistics, not a fitted model result",
            "Only five A cases are available in fold1 FIT and one in DEV",
            "Windowed intensity may retain acquisition/scanner effects",
        ],
    }
    Path(args.output).write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
