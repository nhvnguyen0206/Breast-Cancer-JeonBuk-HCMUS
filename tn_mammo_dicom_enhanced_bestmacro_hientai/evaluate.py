"""Evaluate a trained checkpoint on the test set (DICOM-native).

Loads best_checkpoint.pt, runs inference on the test manifest,
computes all metrics, saves results to the output directory.

Usage:
    python evaluate.py \
        --checkpoint <path_to_best_checkpoint.pt> \
        --test-manifest <path_to_test_manifest.csv> \
        --dicom-root <path_to_dicom_root> \
        --output-dir <training_output_dir> \
        --image-size 224
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import numpy as np
import torch
from torch.nn import functional as F
from torch.utils.data import DataLoader

PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from tn_mammo.constants import (
    INDEX_TO_LABEL,
    LABEL_TO_INDEX,
    NUM_CLASSES,
)
from tn_mammo.data.contracts import (
    decode_coral_logits,
)
from tn_mammo.data.dicom_dataset import (
    DicomFourViewDataset,
)
from tn_mammo.metrics.classification import (
    compute_classification_metrics,
)
from tn_mammo.training.engine import (
    build_model,
    seed_worker,
)


LABELS = ["A", "B", "C", "D"]


def json_ready(value: Any) -> Any:
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(
        value,
        (np.integer, np.floating),
    ):
        return value.item()
    raise TypeError(
        f"Unsupported JSON type: "
        f"{type(value).__name__}"
    )


@torch.no_grad()
def run_test_inference(
    *,
    model: torch.nn.Module,
    loader: DataLoader,
    device: torch.device,
    amp_enabled: bool,
) -> dict[str, Any]:
    """Run inference on test set and compute all metrics."""
    model.eval()

    all_true: list[int] = []
    all_flat_pred: list[int] = []
    all_ordinal_pred: list[int] = []
    all_flat_probs: list[list[float]] = []
    all_case_ids: list[str] = []
    all_sources: list[str] = []

    for batch in loader:
        views = batch["views"].to(
            device,
            non_blocking=True,
        )

        labels = batch["label"].to(
            device,
            non_blocking=True,
        ).long()

        with torch.amp.autocast(
            device_type=device.type,
            dtype=torch.float16,
            enabled=amp_enabled,
        ):
            outputs = model(views)

        flat_logits = outputs["flat_logits"]
        ordinal_logits = outputs[
            "ordinal_logits"
        ]

        flat_probs = F.softmax(
            flat_logits.float(),
            dim=1,
        )

        flat_pred = flat_probs.argmax(dim=1)

        if ordinal_logits is not None:
            ordinal_pred = decode_coral_logits(
                ordinal_logits,
                threshold=0.5,
            )
        else:
            ordinal_pred = flat_pred

        batch_size = int(labels.shape[0])

        all_case_ids.extend(
            list(batch["case_id"])
        )
        all_sources.extend(
            list(batch["source"])
        )

        all_true.extend(
            labels.detach().cpu().tolist()
        )
        all_flat_pred.extend(
            flat_pred.detach().cpu().tolist()
        )
        all_ordinal_pred.extend(
            ordinal_pred.detach().cpu().tolist()
        )
        all_flat_probs.extend(
            flat_probs.detach()
            .float()
            .cpu()
            .tolist()
        )

    # Compute metrics using flat head (primary)
    flat_metrics = compute_classification_metrics(
        all_true,
        all_flat_pred,
    )

    # Compute ordinal metrics
    ordinal_metrics = (
        compute_classification_metrics(
            all_true,
            all_ordinal_pred,
        )
    )

    # Build per-case predictions
    predictions = []
    for i in range(len(all_true)):
        row = {
            "case_id": all_case_ids[i],
            "source": all_sources[i],
            "true_index": all_true[i],
            "true_label": INDEX_TO_LABEL[
                all_true[i]
            ],
            "flat_pred_index": all_flat_pred[i],
            "flat_pred_label": INDEX_TO_LABEL[
                all_flat_pred[i]
            ],
            "ordinal_pred_index": (
                all_ordinal_pred[i]
            ),
            "ordinal_pred_label": INDEX_TO_LABEL[
                all_ordinal_pred[i]
            ],
        }

        for ci in range(NUM_CLASSES):
            row[f"prob_{LABELS[ci]}"] = (
                all_flat_probs[i][ci]
            )

        predictions.append(row)

    return {
        "flat_metrics": flat_metrics,
        "ordinal_metrics": ordinal_metrics,
        "predictions": predictions,
        "num_samples": len(all_true),
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Evaluate checkpoint on test set "
            "(DICOM-native)"
        ),
    )

    parser.add_argument(
        "--checkpoint",
        type=str,
        required=True,
        help="Path to checkpoint .pt file",
    )

    parser.add_argument(
        "--test-manifest",
        type=str,
        required=True,
        help="Path to test manifest CSV",
    )

    parser.add_argument(
        "--dicom-root",
        type=str,
        required=True,
        help="Root directory of DICOM files",
    )

    parser.add_argument(
        "--output-dir",
        type=str,
        required=True,
        help=(
            "Directory to save test results "
            "(same as training output)"
        ),
    )

    parser.add_argument(
        "--image-size",
        type=int,
        default=224,
        help="Image resize dimension",
    )

    parser.add_argument(
        "--batch-size",
        type=int,
        default=2,
        help="Batch size for inference",
    )

    parser.add_argument(
        "--num-workers",
        type=int,
        default=4,
        help="DataLoader workers",
    )

    args = parser.parse_args()

    checkpoint_path = Path(args.checkpoint)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    if not checkpoint_path.exists():
        raise FileNotFoundError(
            f"Checkpoint not found: "
            f"{checkpoint_path}"
        )

    print(
        f"[INFO] Loading checkpoint: "
        f"{checkpoint_path}"
    )

    # Load checkpoint to get config
    checkpoint = torch.load(
        checkpoint_path,
        map_location="cpu",
        weights_only=True,
    )

    config = checkpoint.get(
        "config",
        None,
    )

    if config is None:
        raise RuntimeError(
            "Checkpoint does not contain config"
        )

    # Build model from config
    from tn_mammo.models import (
        FourViewDensityModel,
        ModelOptions,
    )

    model_config = config["model"]
    options = ModelOptions(
        use_ordinal_head=bool(
            model_config.get(
                "use_ordinal_head",
                False,
            )
        ),
        use_binary_head=bool(
            model_config.get(
                "use_binary_head",
                False,
            )
        ),
        imagenet_init=False,
        fusion=str(
            model_config.get(
                "fusion",
                "mean",
            )
        ),
    )

    model = FourViewDensityModel(options)

    # Load weights
    state_dict = checkpoint.get(
        "model_state_dict",
        checkpoint,
    )

    load_result = model.load_state_dict(
        state_dict,
        strict=True,
    )

    print(
        f"[INFO] Model loaded successfully"
    )

    # Setup device
    device = torch.device(
        "cuda"
        if torch.cuda.is_available()
        else "cpu"
    )

    model = model.to(device)
    model.eval()

    amp_enabled = device.type == "cuda"

    # Build test dataset
    print(
        f"[INFO] Loading test dataset: "
        f"{args.test_manifest}"
    )

    test_dataset = DicomFourViewDataset(
        args.test_manifest,
        dicom_root=args.dicom_root,
        image_size=args.image_size,
        training=False,
    )

    print(
        f"[INFO] Test samples: "
        f"{len(test_dataset)}"
    )

    test_loader = DataLoader(
        test_dataset,
        batch_size=args.batch_size,
        shuffle=False,
        num_workers=args.num_workers,
        pin_memory=True,
        worker_init_fn=seed_worker,
        persistent_workers=(
            args.num_workers > 0
        ),
        drop_last=False,
    )

    # Run inference
    print("[INFO] Running test inference...")

    results = run_test_inference(
        model=model,
        loader=test_loader,
        device=device,
        amp_enabled=amp_enabled,
    )

    flat_metrics = results["flat_metrics"]
    ordinal_metrics = results[
        "ordinal_metrics"
    ]

    # Print results
    print("\n" + "=" * 60)
    print("TEST RESULTS (Flat Head - Primary)")
    print("=" * 60)
    print(
        f"  Samples:            "
        f"{flat_metrics['num_samples']}"
    )
    print(
        f"  Macro F1:           "
        f"{flat_metrics['macro_f1']:.4f}"
    )
    print(
        f"  Weighted F1:        "
        f"{flat_metrics['weighted_f1']:.4f}"
    )
    print(
        f"  Accuracy:           "
        f"{flat_metrics['accuracy']:.4f}"
    )
    print(
        f"  Balanced Accuracy:  "
        f"{flat_metrics['balanced_accuracy']:.4f}"
    )
    print(
        f"  QWK:                "
        f"{flat_metrics['qwk']:.4f}"
    )
    print(
        f"  Within-One:         "
        f"{flat_metrics['within_one']:.4f}"
    )
    print(
        f"  Severe Errors:      "
        f"{flat_metrics['severe_error_count']}"
    )
    print(
        f"\n  Confusion Matrix:"
    )
    for row in flat_metrics[
        "confusion_matrix"
    ]:
        print(f"    {row}")

    print("\n" + "=" * 60)
    print("TEST RESULTS (Ordinal Head)")
    print("=" * 60)
    print(
        f"  Macro F1:           "
        f"{ordinal_metrics['macro_f1']:.4f}"
    )
    print(
        f"  QWK:                "
        f"{ordinal_metrics['qwk']:.4f}"
    )

    # Save results
    test_results = {
        "checkpoint": str(checkpoint_path),
        "test_manifest": str(
            args.test_manifest
        ),
        "dicom_root": str(args.dicom_root),
        "image_size": args.image_size,
        "num_samples": results["num_samples"],
        "flat_metrics": flat_metrics,
        "ordinal_metrics": ordinal_metrics,
    }

    results_path = (
        output_dir / "test_metrics.json"
    )
    results_path.write_text(
        json.dumps(
            test_results,
            indent=2,
            ensure_ascii=False,
            default=json_ready,
        ),
        encoding="utf-8",
    )

    print(
        f"\n[SAVED] Test metrics: {results_path}"
    )

    # Save per-case predictions
    import csv

    predictions_path = (
        output_dir / "test_predictions.csv"
    )

    predictions = results["predictions"]

    if predictions:
        with predictions_path.open(
            "w",
            encoding="utf-8",
            newline="",
        ) as f:
            writer = csv.DictWriter(
                f,
                fieldnames=list(
                    predictions[0].keys()
                ),
            )
            writer.writeheader()
            writer.writerows(predictions)

        print(
            f"[SAVED] Test predictions: "
            f"{predictions_path}"
        )

    print("\n[DONE] Test evaluation complete.")


if __name__ == "__main__":
    main()
