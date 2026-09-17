from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path
from typing import Iterable, Sequence

import torch
from torch.utils.data import WeightedRandomSampler

from tn_mammo.constants import (
    LABEL_TO_INDEX,
    NUM_CLASSES,
    VIEW_ORDER,
)


REQUIRED_MANIFEST_COLUMNS = {
    "case_id",
    "split",
    "source",
    "label",
    "label_idx",
    *VIEW_ORDER,
}


def read_manifest(
    path: str | Path,
) -> list[dict[str, str]]:
    manifest_path = Path(path)

    if not manifest_path.exists():
        raise FileNotFoundError(
            f"Manifest not found: {manifest_path}"
        )

    with manifest_path.open(
        "r",
        encoding="utf-8-sig",
        newline="",
    ) as handle:
        reader = csv.DictReader(handle)
        fieldnames = set(reader.fieldnames or [])

        missing = (
            REQUIRED_MANIFEST_COLUMNS
            - fieldnames
        )

        if missing:
            raise ValueError(
                "Manifest missing columns: "
                f"{sorted(missing)}"
            )

        return list(reader)


def validate_manifest(
    rows: Sequence[dict[str, str]],
    *,
    check_paths: bool = True,
) -> dict[str, object]:
    case_ids: set[str] = set()
    duplicate_case_ids: list[str] = []
    invalid_labels: list[str] = []
    missing_paths: list[dict[str, object]] = []
    class_counts: Counter[str] = Counter()
    source_counts: Counter[str] = Counter()

    for row in rows:
        case_id = str(row["case_id"]).strip()
        label = str(row["label"]).strip()
        source = str(row["source"]).strip()

        if case_id in case_ids:
            duplicate_case_ids.append(case_id)

        case_ids.add(case_id)

        if label not in LABEL_TO_INDEX:
            invalid_labels.append(label)
        else:
            class_counts[label] += 1

        source_counts[source] += 1

        if check_paths:
            missing_views = [
                view
                for view in VIEW_ORDER
                if not Path(row[view]).exists()
            ]

            if missing_views:
                missing_paths.append({
                    "case_id": case_id,
                    "missing_views": missing_views,
                })

    return {
        "rows": len(rows),
        "unique_cases": len(case_ids),
        "duplicate_case_ids": duplicate_case_ids,
        "invalid_labels": invalid_labels,
        "missing_paths": missing_paths,
        "class_counts": dict(class_counts),
        "source_counts": dict(source_counts),
        "valid": (
            not duplicate_case_ids
            and not invalid_labels
            and not missing_paths
        ),
    }


def make_ordinal_targets(
    labels: torch.Tensor,
    *,
    num_classes: int = NUM_CLASSES,
) -> torch.Tensor:
    """Map ranks 0..K-1 to cumulative CORAL targets.

    A/0 -> [0,0,0]
    B/1 -> [1,0,0]
    C/2 -> [1,1,0]
    D/3 -> [1,1,1]
    """
    if labels.ndim != 1:
        raise ValueError(
            "labels must have shape [batch]"
        )

    if labels.numel() == 0:
        return torch.empty(
            (0, num_classes - 1),
            dtype=torch.float32,
            device=labels.device,
        )

    if int(labels.min()) < 0:
        raise ValueError("Negative ordinal label.")

    if int(labels.max()) >= num_classes:
        raise ValueError(
            "Ordinal label exceeds num_classes."
        )

    thresholds = torch.arange(
        num_classes - 1,
        device=labels.device,
    )

    return (
        labels.unsqueeze(1) > thresholds
    ).to(torch.float32)


def make_binary_targets(
    labels: torch.Tensor,
) -> torch.Tensor:
    """A/B -> 0; C/D -> 1."""
    return (labels >= 2).to(torch.long)


def decode_coral_logits(
    logits: torch.Tensor,
    *,
    threshold: float = 0.5,
) -> torch.Tensor:
    if logits.ndim != 2:
        raise ValueError(
            "CORAL logits must have shape "
            "[batch, num_classes - 1]."
        )

    probabilities = torch.sigmoid(logits)

    return (
        probabilities > threshold
    ).sum(dim=1).to(torch.long)


def compute_domain_sample_weights(
    domains: Sequence[str],
    *,
    tn_ratio: float,
) -> torch.Tensor:
    if not 0.0 <= tn_ratio <= 1.0:
        raise ValueError(
            "tn_ratio must lie in [0, 1]."
        )

    counts = Counter(domains)

    tn_count = counts.get("TN", 0)
    vindr_count = counts.get("VinDr", 0)

    if tn_count == 0 or vindr_count == 0:
        raise ValueError(
            "Both TN and VinDr must be present."
        )

    domain_weight = {
        "TN": tn_ratio / tn_count,
        "VinDr": (
            1.0 - tn_ratio
        ) / vindr_count,
    }

    unknown = sorted(
        set(domains)
        - set(domain_weight)
    )

    if unknown:
        raise ValueError(
            f"Unsupported domains: {unknown}"
        )

    return torch.tensor(
        [
            domain_weight[domain]
            for domain in domains
        ],
        dtype=torch.double,
    )


def realized_domain_mass(
    domains: Sequence[str],
    weights: torch.Tensor,
) -> dict[str, float]:
    if len(domains) != len(weights):
        raise ValueError(
            "domains and weights length mismatch."
        )

    mass: Counter[str] = Counter()

    for domain, weight in zip(
        domains,
        weights.tolist(),
    ):
        mass[domain] += float(weight)

    total = sum(mass.values())

    return {
        domain: value / total
        for domain, value in mass.items()
    }


def build_target_aware_sampler(
    domains: Sequence[str],
    *,
    tn_ratio: float,
    num_samples: int | None = None,
    generator: torch.Generator | None = None,
) -> WeightedRandomSampler:
    weights = compute_domain_sample_weights(
        domains,
        tn_ratio=tn_ratio,
    )

    return WeightedRandomSampler(
        weights=weights,
        num_samples=(
            int(num_samples)
            if num_samples is not None
            else len(domains)
        ),
        replacement=True,
        generator=generator,
    )


def assert_disjoint_case_ids(
    *manifest_rows: Iterable[dict[str, str]],
) -> None:
    seen: set[str] = set()

    for rows in manifest_rows:
        current = {
            str(row["case_id"]).strip()
            for row in rows
        }

        overlap = seen & current

        if overlap:
            raise ValueError(
                "Case overlap detected: "
                f"{sorted(overlap)[:20]}"
            )

        seen |= current
