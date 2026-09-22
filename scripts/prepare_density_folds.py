"""Density-balanced grouped CV, preserving the prior population and registry."""
import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

VIEWS = ("L_CC", "L_MLO", "R_CC", "R_MLO")
LABELS = tuple("ABCD")
SPLITS = ("fit", "dev", "cal", "outer_holdout")


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def assign_folds(frame, n_splits=5, seed=42):
    """Place multi-study components first, then balance singleton class counts."""
    if n_splits < 2:
        raise ValueError("At least two folds required")
    frame = frame.sort_values("case_id").reset_index(drop=True).copy()
    if frame.empty or frame.case_id.duplicated().any() or not frame.label.isin(LABELS).all():
        raise ValueError("Unique cases and valid density labels required")
    rng = np.random.default_rng(seed)
    counts = np.zeros((n_splits, 4), dtype=int)
    totals = frame.label.value_counts().reindex(LABELS, fill_value=0).to_numpy()
    groups = []
    for group, data in frame.groupby("component_id", sort=True):
        vector = data.label.value_counts().reindex(LABELS, fill_value=0).to_numpy()
        groups.append((group, vector, float(rng.random())))
    # Components with multiple studies must never be broken apart for balance.
    groups.sort(key=lambda item: (-int(item[1].sum()),
                                  float(totals[item[1] > 0].min()), item[2]))
    assignments = {}
    for group, vector, _ in groups:
        if vector.sum() == 1:
            label = int(vector.argmax())
            candidates = np.flatnonzero(counts[:, label] == counts[:, label].min())
            sizes = counts.sum(axis=1)
            candidates = candidates[sizes[candidates] == sizes[candidates].min()]
            fold = int(rng.choice(candidates))
        else:
            scores = []
            for fold in range(n_splits):
                proposal = counts.copy()
                proposal[fold] += vector
                scores.append(float(np.square(proposal / np.maximum(totals, 1)).sum()))
            candidates = np.flatnonzero(np.isclose(scores, min(scores), rtol=0, atol=1e-14))
            fold = int(rng.choice(candidates))
        assignments[group] = fold
        counts[fold] += vector
    frame["fold"] = frame.component_id.map(assignments)
    # Fail closed if a different population cannot meet the promised balance.
    if np.any(counts.max(axis=0) - counts.min(axis=0) > 1):
        raise ValueError("Grouped population cannot meet per-class spread <= 1 with this allocation")
    if counts.sum(axis=1).max() - counts.sum(axis=1).min() > 1:
        raise ValueError("Allocation does not meet total fold-size spread <= 1")
    if (counts == 0).any():
        raise ValueError("Every validation fold must contain all four density classes")
    return frame


def prepare(source, registry_path, output, n_splits=5, seed=42):
    source, output = Path(source).resolve(), Path(output).resolve()
    if output.exists() and any(output.iterdir()):
        raise FileExistsError("Use a new empty output directory; existing splits are preserved")
    registry = json.loads(Path(registry_path).read_text())
    mapping = registry["breast_to_component"]
    frames = []
    for split in SPLITS:
        path = source / f"{split}.csv"
        frame = pd.read_csv(path, dtype=str)
        frame["previous_split"] = split
        for view in VIEWS:
            frame[view] = frame[view].map(lambda p: str((source / p).resolve()))
        frames.append(frame)
    frame = pd.concat(frames, ignore_index=True)
    if frame.case_id.duplicated().any():
        raise ValueError("Overlapping source case IDs")
    components = []
    for case in frame.case_id:
        left, right = mapping.get(case + "_L"), mapping.get(case + "_R")
        if left is None or right is None or left != right:
            raise ValueError("Case missing from registry or breasts belong to different components")
        components.append(left)
    frame["component_id"] = components
    # An identical resolved input path cannot appear in independently assigned groups.
    path_groups = {}
    for row in frame.itertuples():
        for view in VIEWS:
            path = getattr(row, view)
            if not Path(path).is_file():
                raise FileNotFoundError(path)
            if path in path_groups and path_groups[path] != row.component_id:
                raise ValueError("Shared image path crosses registry components")
            path_groups[path] = row.component_id
    assigned = assign_folds(frame, n_splits, seed)
    counts = pd.crosstab(assigned.fold, assigned.label).reindex(
        index=range(n_splits), columns=LABELS, fill_value=0)
    output.mkdir(parents=True, exist_ok=True)
    assigned.to_csv(output / "assignments.csv", index=False)
    for fold in range(n_splits):
        directory = output / f"fold_{fold}"
        directory.mkdir()
        for role, subset in (("fit", assigned[assigned.fold != fold]),
                             ("dev", assigned[assigned.fold == fold])):
            subset.loc[:, ["case_id", "label", *VIEWS]].to_csv(directory / f"{role}.csv", index=False)
    audit = {
        "schema": "tn_mammo.density_grouped_cv.v1", "seed": seed, "n_splits": n_splits,
        "algorithm": "largest components first; rarity-ordered singleton class/size balancing",
        "num_studies": len(assigned), "num_components": assigned.component_id.nunique(),
        "component_registry_algorithm": registry.get("algorithm"),
        "class_totals": assigned.label.value_counts().reindex(LABELS).to_dict(),
        "dev_counts": {str(i): counts.loc[i].to_dict() for i in range(n_splits)},
        "fit_counts": {str(i): (counts.sum() - counts.loc[i]).to_dict() for i in range(n_splits)},
        "source_sha256": {str(p): digest(p) for p in
                           [*(source / f"{s}.csv" for s in SPLITS), Path(registry_path)]},
        "assignments_sha256": digest(output / "assignments.csv"),
        "role_policy": "4 folds FIT + 1 DEV; no independent CAL/OUTER in this CV protocol",
        "limitations": ["Only six density-A studies in this population",
                       "DEV is used for selection, not an independent final test",
                       "Some cases were used in prior development runs; this is not a fresh unseen holdout",
                       "Grouping inherits the supplied registry; no new patient/content audit performed"],
    }
    (output / "audit.json").write_text(json.dumps(audit, indent=2))
    print(json.dumps(audit, indent=2))
    return assigned


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-dir", required=True)
    parser.add_argument("--component-registry", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--n-splits", type=int, default=5)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    prepare(args.source_dir, args.component_registry, args.output_dir, args.n_splits, args.seed)
