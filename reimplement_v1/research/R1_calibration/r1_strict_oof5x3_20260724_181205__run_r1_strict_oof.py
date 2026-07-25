from __future__ import annotations

import ast
import contextlib
import io
import json
import math
import os
import re
import runpy
import sys
import traceback
from pathlib import Path
from typing import Any

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import torch
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    cohen_kappa_score,
    confusion_matrix,
    f1_score,
    recall_score,
)


ROOT = Path(
    "/mnt/hcmus/breast_vn/code/new_implement/"
    "tn-mammo-bestmacro-hientai"
)

PHASEI = Path(
    "/mnt/hcmus/breast_vn/code/new_implement/"
    "outputs/phaseI_cv5x3_20260721_162651"
)

EVALUATE_SCRIPT = ROOT / "evaluate.py"
OUTPUT = Path(__file__).resolve().parent

SEEDS = [42, 43, 44]
FOLDS = [0, 1, 2, 3, 4]
LABELS = ["A", "B", "C", "D"]

EXPECTED_DEV_CASES = 544


def metric_bundle(
    y_true: np.ndarray,
    y_pred: np.ndarray,
) -> dict[str, Any]:
    cm = confusion_matrix(
        y_true,
        y_pred,
        labels=[0, 1, 2, 3],
    )

    recalls = recall_score(
        y_true,
        y_pred,
        labels=[0, 1, 2, 3],
        average=None,
        zero_division=0,
    )

    per_class_f1 = f1_score(
        y_true,
        y_pred,
        labels=[0, 1, 2, 3],
        average=None,
        zero_division=0,
    )

    severe = 0
    within_one = 0

    for true_idx in range(4):
        for pred_idx in range(4):
            count = int(cm[true_idx, pred_idx])

            if abs(true_idx - pred_idx) >= 2:
                severe += count

            if abs(true_idx - pred_idx) <= 1:
                within_one += count

    total = int(cm.sum())

    return {
        "num_samples": int(len(y_true)),
        "accuracy": float(
            accuracy_score(y_true, y_pred)
        ),
        "balanced_accuracy": float(
            balanced_accuracy_score(y_true, y_pred)
        ),
        "macro_f1": float(
            f1_score(
                y_true,
                y_pred,
                labels=[0, 1, 2, 3],
                average="macro",
                zero_division=0,
            )
        ),
        "weighted_f1": float(
            f1_score(
                y_true,
                y_pred,
                labels=[0, 1, 2, 3],
                average="weighted",
                zero_division=0,
            )
        ),
        "qwk": float(
            cohen_kappa_score(
                y_true,
                y_pred,
                weights="quadratic",
            )
        ),
        "per_class_recall": {
            label: float(recalls[index])
            for index, label in enumerate(LABELS)
        },
        "per_class_f1": {
            label: float(per_class_f1[index])
            for index, label in enumerate(LABELS)
        },
        "confusion_matrix": cm.tolist(),
        "c_to_d": int(cm[2, 3]),
        "d_to_c": int(cm[3, 2]),
        "cd_error_count": int(cm[2, 3] + cm[3, 2]),
        "severe_error_count": int(severe),
        "within_one": (
            float(within_one / total)
            if total > 0
            else 0.0
        ),
    }


def ranking(metrics: dict[str, Any]) -> tuple[float, ...]:
    return (
        float(metrics["macro_f1"]),
        float(metrics["balanced_accuracy"]),
        float(metrics["per_class_recall"]["D"]),
        -float(metrics["cd_error_count"]),
        -float(metrics["severe_error_count"]),
    )


def softmax(logits: np.ndarray) -> np.ndarray:
    shifted = logits - logits.max(
        axis=1,
        keepdims=True,
    )

    exp_values = np.exp(shifted)

    return exp_values / exp_values.sum(
        axis=1,
        keepdims=True,
    )


def labels_from_manifest(
    manifest: pd.DataFrame,
) -> np.ndarray:
    if "label_idx" in manifest.columns:
        return (
            manifest["label_idx"]
            .astype(int)
            .to_numpy()
        )

    mapping = {
        "A": 0,
        "B": 1,
        "C": 2,
        "D": 3,
    }

    return (
        manifest["label"]
        .astype(str)
        .str.upper()
        .map(mapping)
        .astype(int)
        .to_numpy()
    )


def collect_tensor_candidates(
    value: Any,
    bucket: list[torch.Tensor],
) -> None:
    if torch.is_tensor(value):
        if (
            value.ndim == 2
            and value.shape[1] == 4
        ):
            bucket.append(
                value.detach().float().cpu()
            )
        return

    if isinstance(value, dict):
        for nested in value.values():
            collect_tensor_candidates(
                nested,
                bucket,
            )
        return

    if isinstance(value, (tuple, list)):
        for nested in value:
            collect_tensor_candidates(
                nested,
                bucket,
            )


def parse_json_from_log(
    text: str,
) -> dict[str, Any] | None:
    start = text.find("{")
    end = text.rfind("}")

    if start < 0 or end < start:
        return None

    try:
        return json.loads(
            text[start:end + 1]
        )
    except Exception:
        return None


def locate_checkpoint(
    seed: int,
    fold: int,
) -> Path:
    checkpoint = (
        PHASEI
        / "runs"
        / "I1_MEAN_CORAL"
        / f"seed{seed}"
        / f"fold{fold}"
        / "training"
        / "best_checkpoint.pt"
    )

    if not checkpoint.is_file():
        raise FileNotFoundError(
            "Missing expected I1 checkpoint: "
            f"{checkpoint}"
        )

    print(
        "[CHECKPOINT RESOLVED] "
        f"seed={seed} fold={fold} "
        f"path={checkpoint}"
    )

    return checkpoint


def capture_logits(
    checkpoint: Path,
    manifest_path: Path,
    output_dir: Path,
) -> dict[str, Any]:
    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    manifest = pd.read_csv(
        manifest_path
    )

    y_true = labels_from_manifest(
        manifest
    )

    expected_count = int(
        len(manifest)
    )

    captured: dict[
        str,
        list[torch.Tensor]
    ] = {}

    original_call = (
        torch.nn.Module._call_impl
    )

    def patched_call(
        module: torch.nn.Module,
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        output = original_call(
            module,
            *args,
            **kwargs,
        )

        tensors: list[torch.Tensor] = []

        collect_tensor_candidates(
            output,
            tensors,
        )

        if tensors:
            key = (
                f"{module.__class__.__module__}."
                f"{module.__class__.__qualname__}"
                f"@{id(module)}"
            )

            captured.setdefault(
                key,
                [],
            )

            captured[key].extend(
                tensors
            )

        return output

    old_argv = list(sys.argv)
    old_cwd = Path.cwd()

    buffer = io.StringIO()
    evaluator_error = ""

    try:
        os.chdir(ROOT)

        if str(ROOT) not in sys.path:
            sys.path.insert(
                0,
                str(ROOT),
            )

        if str(ROOT / "src") not in sys.path:
            sys.path.insert(
                0,
                str(ROOT / "src"),
            )

        sys.argv = [
            str(EVALUATE_SCRIPT),
            "--checkpoint",
            str(checkpoint),
            "--manifest",
            str(manifest_path),
        ]

        torch.nn.Module._call_impl = (
            patched_call
        )

        with contextlib.redirect_stdout(
            buffer
        ):
            with contextlib.redirect_stderr(
                buffer
            ):
                try:
                    runpy.run_path(
                        str(EVALUATE_SCRIPT),
                        run_name="__main__",
                    )
                except SystemExit as exc:
                    if exc.code not in (
                        None,
                        0,
                    ):
                        evaluator_error = (
                            f"SystemExit({exc.code})"
                        )
                except Exception:
                    evaluator_error = (
                        traceback.format_exc()
                    )

    finally:
        torch.nn.Module._call_impl = (
            original_call
        )

        sys.argv = old_argv
        os.chdir(old_cwd)

    log_text = buffer.getvalue()

    (output_dir / "evaluate.log").write_text(
        log_text,
        encoding="utf-8",
    )

    evaluator_json = parse_json_from_log(
        log_text
    )

    reported_macro = None
    reported_accuracy = None

    if evaluator_json is not None:
        reported_macro = (
            evaluator_json.get(
                "macro_f1"
            )
        )

        reported_accuracy = (
            evaluator_json.get(
                "accuracy"
            )
        )

    best_values: np.ndarray | None = None
    best_key: str | None = None
    best_distance = float("inf")

    candidate_rows: list[
        dict[str, Any]
    ] = []

    for key, chunks in captured.items():
        try:
            values = torch.cat(
                chunks,
                dim=0,
            ).numpy()
        except Exception:
            continue

        if values.shape != (
            expected_count,
            4,
        ):
            candidate_rows.append(
                {
                    "key": key,
                    "shape": list(
                        values.shape
                    ),
                    "selected": False,
                }
            )
            continue

        pred = values.argmax(
            axis=1
        )

        candidate_metrics = metric_bundle(
            y_true,
            pred,
        )

        distance = 0.0

        if reported_macro is not None:
            distance += abs(
                candidate_metrics[
                    "macro_f1"
                ]
                - float(reported_macro)
            )

        if reported_accuracy is not None:
            distance += abs(
                candidate_metrics[
                    "accuracy"
                ]
                - float(
                    reported_accuracy
                )
            )

        candidate_rows.append(
            {
                "key": key,
                "shape": list(
                    values.shape
                ),
                "distance": distance,
                "macro_f1": (
                    candidate_metrics[
                        "macro_f1"
                    ]
                ),
                "selected": False,
            }
        )

        if distance < best_distance:
            best_distance = distance
            best_values = values
            best_key = key

    if best_values is None:
        raise RuntimeError(
            "Không capture được tensor "
            f"shape ({expected_count}, 4). "
            f"Evaluator error: {evaluator_error}"
        )

    for row in candidate_rows:
        if row.get("key") == best_key:
            row["selected"] = True

    looks_like_probability = (
        np.all(best_values >= -1e-6)
        and np.all(
            best_values <= 1.0 + 1e-6
        )
        and np.allclose(
            best_values.sum(axis=1),
            1.0,
            atol=1e-3,
        )
    )

    if looks_like_probability:
        probabilities = np.clip(
            best_values,
            1e-8,
            1.0,
        )

        logits = np.log(
            probabilities
        )
    else:
        logits = (
            best_values.astype(
                np.float64
            )
        )

        probabilities = softmax(
            logits
        )

    pred = logits.argmax(
        axis=1
    )

    metrics = metric_bundle(
        y_true,
        pred,
    )

    np.save(
        output_dir / "logits.npy",
        logits,
    )

    np.save(
        output_dir / "probabilities.npy",
        probabilities,
    )

    case_column = (
        "case_id"
        if "case_id" in manifest.columns
        else manifest.columns[0]
    )

    result = pd.DataFrame(
        {
            "case_id": (
                manifest[
                    case_column
                ].astype(str)
            ),
            "true_idx": y_true,
            "true_label": [
                LABELS[index]
                for index in y_true
            ],
            "base_pred_idx": pred,
            "base_pred_label": [
                LABELS[index]
                for index in pred
            ],
            "logit_A": logits[:, 0],
            "logit_B": logits[:, 1],
            "logit_C": logits[:, 2],
            "logit_D": logits[:, 3],
            "prob_A": probabilities[:, 0],
            "prob_B": probabilities[:, 1],
            "prob_C": probabilities[:, 2],
            "prob_D": probabilities[:, 3],
        }
    )

    result.to_csv(
        output_dir / "predictions.csv",
        index=False,
    )

    capture_report = {
        "checkpoint": str(
            checkpoint
        ),
        "manifest": str(
            manifest_path
        ),
        "expected_count": expected_count,
        "selected_tensor": best_key,
        "selected_distance": (
            best_distance
            if math.isfinite(
                best_distance
            )
            else None
        ),
        "evaluator_error": (
            evaluator_error
        ),
        "baseline_metrics": metrics,
        "candidates": candidate_rows,
    }

    (
        output_dir
        / "capture_report.json"
    ).write_text(
        json.dumps(
            capture_report,
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    return {
        "manifest": manifest,
        "y_true": y_true,
        "logits": logits,
        "probabilities": probabilities,
        "predictions": pred,
        "metrics": metrics,
    }


def apply_cd_calibration(
    logits: np.ndarray,
    alpha: float,
    beta: float,
) -> np.ndarray:
    adjusted = logits.copy()

    center = (
        adjusted[:, 2]
        + adjusted[:, 3]
    ) / 2.0

    margin = (
        adjusted[:, 3]
        - adjusted[:, 2]
    )

    calibrated_margin = (
        alpha * margin
        + beta
    )

    adjusted[:, 2] = (
        center
        - calibrated_margin / 2.0
    )

    adjusted[:, 3] = (
        center
        + calibrated_margin / 2.0
    )

    return adjusted


def fit_calibration(
    logits: np.ndarray,
    y_true: np.ndarray,
) -> dict[str, Any]:
    alpha_grid = np.linspace(
        0.50,
        2.00,
        31,
    )

    beta_grid = np.linspace(
        -2.00,
        2.00,
        81,
    )

    best: dict[str, Any] | None = None
    best_rank: tuple[
        float,
        ...
    ] | None = None

    rows: list[
        dict[str, Any]
    ] = []

    baseline_pred = logits.argmax(
        axis=1
    )

    baseline_metrics = metric_bundle(
        y_true,
        baseline_pred,
    )

    for alpha in alpha_grid:
        for beta in beta_grid:
            adjusted = (
                apply_cd_calibration(
                    logits,
                    float(alpha),
                    float(beta),
                )
            )

            pred = adjusted.argmax(
                axis=1
            )

            metrics = metric_bundle(
                y_true,
                pred,
            )

            current_rank = ranking(
                metrics
            )

            rows.append(
                {
                    "alpha": float(alpha),
                    "beta": float(beta),
                    "macro_f1": (
                        metrics[
                            "macro_f1"
                        ]
                    ),
                    "balanced_accuracy": (
                        metrics[
                            "balanced_accuracy"
                        ]
                    ),
                    "d_recall": (
                        metrics[
                            "per_class_recall"
                        ]["D"]
                    ),
                    "cd_error_count": (
                        metrics[
                            "cd_error_count"
                        ]
                    ),
                    "c_to_d": (
                        metrics["c_to_d"]
                    ),
                    "d_to_c": (
                        metrics["d_to_c"]
                    ),
                    "severe_error_count": (
                        metrics[
                            "severe_error_count"
                        ]
                    ),
                }
            )

            if (
                best_rank is None
                or current_rank
                > best_rank
            ):
                best_rank = (
                    current_rank
                )

                best = {
                    "alpha": float(
                        alpha
                    ),
                    "beta": float(
                        beta
                    ),
                    "metrics": metrics,
                    "predictions": pred,
                }

    assert best is not None

    return {
        "baseline_metrics": (
            baseline_metrics
        ),
        "selected_alpha": (
            best["alpha"]
        ),
        "selected_beta": (
            best["beta"]
        ),
        "selected_metrics": (
            best["metrics"]
        ),
        "selected_predictions": (
            best["predictions"]
        ),
        "grid": rows,
    }


def bootstrap_seed_delta(
    y_true: np.ndarray,
    base_pred: np.ndarray,
    calibrated_pred: np.ndarray,
    iterations: int = 2000,
    seed: int = 20260724,
) -> dict[str, Any]:
    rng = np.random.default_rng(
        seed
    )

    sample_count = len(y_true)
    deltas: list[float] = []

    for _ in range(iterations):
        indices = rng.integers(
            0,
            sample_count,
            size=sample_count,
        )

        y_sample = y_true[
            indices
        ]

        base_sample = base_pred[
            indices
        ]

        calibrated_sample = (
            calibrated_pred[
                indices
            ]
        )

        base_f1 = f1_score(
            y_sample,
            base_sample,
            labels=[0, 1, 2, 3],
            average="macro",
            zero_division=0,
        )

        calibrated_f1 = f1_score(
            y_sample,
            calibrated_sample,
            labels=[0, 1, 2, 3],
            average="macro",
            zero_division=0,
        )

        deltas.append(
            float(
                calibrated_f1
                - base_f1
            )
        )

    values = np.asarray(
        deltas,
        dtype=float,
    )

    return {
        "iterations": iterations,
        "mean_delta": float(
            values.mean()
        ),
        "median_delta": float(
            np.median(values)
        ),
        "ci95_low": float(
            np.quantile(
                values,
                0.025,
            )
        ),
        "ci95_high": float(
            np.quantile(
                values,
                0.975,
            )
        ),
        "probability_delta_positive": (
            float(
                np.mean(
                    values > 0
                )
            )
        ),
    }


def find_manifest(
    name: str,
) -> Path:
    path = (
        PHASEI
        / "manifests"
        / name
    )

    if not path.is_file():
        raise FileNotFoundError(
            f"Missing manifest: {path}"
        )

    return path


def run_fold(
    seed: int,
    fold: int,
) -> dict[str, Any]:
    run_name = (
        f"seed{seed}_fold{fold}"
    )

    run_dir = (
        OUTPUT
        / "fold_runs"
        / run_name
    )

    inner_dir = (
        run_dir
        / "inner_valid"
    )

    outer_dir = (
        run_dir
        / "outer_eval"
    )

    run_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    checkpoint = locate_checkpoint(
        seed,
        fold,
    )

    inner_manifest = find_manifest(
        f"fold{fold}_inner_valid.csv"
    )

    outer_manifest = find_manifest(
        f"fold{fold}_outer_eval.csv"
    )

    print()
    print(
        "============================================================"
    )
    print(
        f" SEED={seed} FOLD={fold}"
    )
    print(
        "============================================================"
    )
    print(
        f"CHECKPOINT={checkpoint}"
    )
    print(
        f"INNER_VALID={inner_manifest}"
    )
    print(
        f"OUTER_EVAL={outer_manifest}"
    )

    inner = capture_logits(
        checkpoint,
        inner_manifest,
        inner_dir,
    )

    calibration = fit_calibration(
        inner["logits"],
        inner["y_true"],
    )

    pd.DataFrame(
        calibration["grid"]
    ).to_csv(
        run_dir
        / "inner_calibration_grid.csv",
        index=False,
    )

    outer = capture_logits(
        checkpoint,
        outer_manifest,
        outer_dir,
    )

    base_pred = outer[
        "logits"
    ].argmax(axis=1)

    calibrated_logits = (
        apply_cd_calibration(
            outer["logits"],
            calibration[
                "selected_alpha"
            ],
            calibration[
                "selected_beta"
            ],
        )
    )

    calibrated_pred = (
        calibrated_logits.argmax(
            axis=1
        )
    )

    base_metrics = metric_bundle(
        outer["y_true"],
        base_pred,
    )

    calibrated_metrics = (
        metric_bundle(
            outer["y_true"],
            calibrated_pred,
        )
    )

    outer_predictions = (
        outer_dir
        / "predictions.csv"
    )

    result_df = pd.read_csv(
        outer_predictions
    )

    result_df[
        "calibrated_pred_idx"
    ] = calibrated_pred

    result_df[
        "calibrated_pred_label"
    ] = [
        LABELS[index]
        for index
        in calibrated_pred
    ]

    result_df[
        "selected_alpha"
    ] = calibration[
        "selected_alpha"
    ]

    result_df[
        "selected_beta"
    ] = calibration[
        "selected_beta"
    ]

    result_df[
        "seed"
    ] = seed

    result_df[
        "fold"
    ] = fold

    result_df.to_csv(
        run_dir
        / "outer_predictions_calibrated.csv",
        index=False,
    )

    fold_summary = {
        "seed": seed,
        "fold": fold,
        "checkpoint": str(
            checkpoint
        ),
        "inner_valid_count": int(
            len(inner["y_true"])
        ),
        "outer_eval_count": int(
            len(outer["y_true"])
        ),
        "selected_alpha": (
            calibration[
                "selected_alpha"
            ]
        ),
        "selected_beta": (
            calibration[
                "selected_beta"
            ]
        ),
        "inner_baseline_metrics": (
            calibration[
                "baseline_metrics"
            ]
        ),
        "inner_selected_metrics": (
            calibration[
                "selected_metrics"
            ]
        ),
        "outer_baseline_metrics": (
            base_metrics
        ),
        "outer_calibrated_metrics": (
            calibrated_metrics
        ),
        "outer_delta_macro_f1": (
            calibrated_metrics[
                "macro_f1"
            ]
            - base_metrics[
                "macro_f1"
            ]
        ),
        "locked_test_used": False,
    }

    (
        run_dir
        / "fold_summary.json"
    ).write_text(
        json.dumps(
            fold_summary,
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    print(
        "ALPHA="
        f"{calibration['selected_alpha']}"
    )
    print(
        "BETA="
        f"{calibration['selected_beta']}"
    )
    print(
        "OUTER_BASE_MACRO_F1="
        f"{base_metrics['macro_f1']:.6f}"
    )
    print(
        "OUTER_R1_MACRO_F1="
        f"{calibrated_metrics['macro_f1']:.6f}"
    )
    print(
        "OUTER_DELTA="
        f"{fold_summary['outer_delta_macro_f1']:+.6f}"
    )

    return {
        "summary": fold_summary,
        "predictions": result_df,
    }


def plot_summary(
    seed_summary: pd.DataFrame,
    combined_base: dict[str, Any],
    combined_r1: dict[str, Any],
) -> None:
    fig = plt.figure(
        figsize=(15, 9),
    )

    grid = fig.add_gridspec(
        3,
        12,
        height_ratios=[
            0.8,
            1.4,
            3.2,
        ],
        hspace=0.45,
        wspace=0.8,
    )

    title_ax = fig.add_subplot(
        grid[0, :],
    )

    title_ax.axis("off")

    title_ax.text(
        0.0,
        0.72,
        "R1 C/D Calibration — Strict 5-Fold × 3-Seed OOF",
        fontsize=23,
        fontweight="bold",
    )

    title_ax.text(
        0.0,
        0.20,
        "Alpha/Beta fitted on inner validation only; applied once to outer evaluation. Locked test not used.",
        fontsize=11,
    )

    cards = [
        (
            "Baseline OOF Macro-F1",
            combined_base[
                "macro_f1"
            ],
            True,
        ),
        (
            "R1 OOF Macro-F1",
            combined_r1[
                "macro_f1"
            ],
            True,
        ),
        (
            "Delta",
            combined_r1[
                "macro_f1"
            ]
            - combined_base[
                "macro_f1"
            ],
            False,
        ),
        (
            "Baseline D Recall",
            combined_base[
                "per_class_recall"
            ]["D"],
            True,
        ),
        (
            "R1 D Recall",
            combined_r1[
                "per_class_recall"
            ]["D"],
            True,
        ),
        (
            "R1 C↔D Errors",
            combined_r1[
                "cd_error_count"
            ],
            None,
        ),
    ]

    for index, (
        title,
        value,
        percentage,
    ) in enumerate(cards):
        ax = fig.add_subplot(
            grid[
                1,
                index * 2:
                (index + 1) * 2,
            ]
        )

        ax.set_xticks([])
        ax.set_yticks([])

        if percentage is True:
            display = (
                f"{value * 100:.2f}%"
            )
        elif percentage is False:
            display = (
                f"{value * 100:+.2f} pts"
            )
        else:
            display = str(
                int(value)
            )

        ax.text(
            0.5,
            0.68,
            title,
            ha="center",
            va="center",
            fontsize=10,
            wrap=True,
        )

        ax.text(
            0.5,
            0.31,
            display,
            ha="center",
            va="center",
            fontsize=19,
            fontweight="bold",
        )

    macro_ax = fig.add_subplot(
        grid[2, 0:4]
    )

    x = np.arange(
        len(seed_summary)
    )

    width = 0.35

    macro_ax.bar(
        x - width / 2,
        seed_summary[
            "baseline_macro_f1"
        ],
        width,
        label="Baseline",
    )

    macro_ax.bar(
        x + width / 2,
        seed_summary[
            "r1_macro_f1"
        ],
        width,
        label="R1",
    )

    macro_ax.set_title(
        "OOF Macro-F1 by seed",
        fontweight="bold",
    )

    macro_ax.set_xticks(
        x,
        [
            f"Seed {seed}"
            for seed
            in seed_summary["seed"]
        ],
    )

    macro_ax.set_ylim(
        0,
        1,
    )

    macro_ax.legend()

    d_ax = fig.add_subplot(
        grid[2, 4:8]
    )

    d_ax.bar(
        x - width / 2,
        seed_summary[
            "baseline_d_recall"
        ],
        width,
        label="Baseline",
    )

    d_ax.bar(
        x + width / 2,
        seed_summary[
            "r1_d_recall"
        ],
        width,
        label="R1",
    )

    d_ax.set_title(
        "Class D recall by seed",
        fontweight="bold",
    )

    d_ax.set_xticks(
        x,
        [
            f"Seed {seed}"
            for seed
            in seed_summary["seed"]
        ],
    )

    d_ax.set_ylim(
        0,
        1,
    )

    d_ax.legend()

    error_ax = fig.add_subplot(
        grid[2, 8:12]
    )

    error_ax.bar(
        x - width / 2,
        seed_summary[
            "baseline_cd_errors"
        ],
        width,
        label="Baseline",
    )

    error_ax.bar(
        x + width / 2,
        seed_summary[
            "r1_cd_errors"
        ],
        width,
        label="R1",
    )

    error_ax.set_title(
        "C↔D errors by seed",
        fontweight="bold",
    )

    error_ax.set_xticks(
        x,
        [
            f"Seed {seed}"
            for seed
            in seed_summary["seed"]
        ],
    )

    error_ax.legend()

    fig.savefig(
        OUTPUT
        / "comparison_oof.png",
        dpi=180,
        bbox_inches="tight",
    )

    plt.close(fig)


def main() -> None:
    print(
        "============================================================"
    )
    print(
        " R1 STRICT 5x3 OOF CONFIRMATION"
    )
    print(
        " GPU PHYSICAL 0"
    )
    print(
        " LOCKED TEST 132 IS NOT USED"
    )
    print(
        "============================================================"
    )

    required = [
        EVALUATE_SCRIPT,
        PHASEI
        / "manifests",
    ]

    missing = [
        str(path)
        for path in required
        if not path.exists()
    ]

    if missing:
        print(
            "[FAILED] Missing inputs:"
        )

        for path in missing:
            print(path)

        (
            OUTPUT
            / "PIPELINE_FAILED.txt"
        ).write_text(
            "\n".join(missing),
            encoding="utf-8",
        )

        return

    all_fold_summaries: list[
        dict[str, Any]
    ] = []

    all_predictions: list[
        pd.DataFrame
    ] = []

    for seed in SEEDS:
        for fold in FOLDS:
            result = run_fold(
                seed,
                fold,
            )

            all_fold_summaries.append(
                result["summary"]
            )

            all_predictions.append(
                result["predictions"]
            )

    fold_rows: list[
        dict[str, Any]
    ] = []

    for summary in all_fold_summaries:
        base = summary[
            "outer_baseline_metrics"
        ]

        r1 = summary[
            "outer_calibrated_metrics"
        ]

        fold_rows.append(
            {
                "seed": summary["seed"],
                "fold": summary["fold"],
                "alpha": (
                    summary[
                        "selected_alpha"
                    ]
                ),
                "beta": (
                    summary[
                        "selected_beta"
                    ]
                ),
                "baseline_macro_f1": (
                    base["macro_f1"]
                ),
                "r1_macro_f1": (
                    r1["macro_f1"]
                ),
                "delta_macro_f1": (
                    r1["macro_f1"]
                    - base["macro_f1"]
                ),
                "baseline_balanced_accuracy": (
                    base[
                        "balanced_accuracy"
                    ]
                ),
                "r1_balanced_accuracy": (
                    r1[
                        "balanced_accuracy"
                    ]
                ),
                "baseline_d_recall": (
                    base[
                        "per_class_recall"
                    ]["D"]
                ),
                "r1_d_recall": (
                    r1[
                        "per_class_recall"
                    ]["D"]
                ),
                "baseline_cd_errors": (
                    base[
                        "cd_error_count"
                    ]
                ),
                "r1_cd_errors": (
                    r1[
                        "cd_error_count"
                    ]
                ),
            }
        )

    fold_df = pd.DataFrame(
        fold_rows
    )

    fold_df.to_csv(
        OUTPUT
        / "fold_summary.csv",
        index=False,
    )

    combined_predictions = (
        pd.concat(
            all_predictions,
            ignore_index=True,
        )
    )

    combined_predictions.to_csv(
        OUTPUT
        / "all_outer_predictions.csv",
        index=False,
    )

    seed_rows: list[
        dict[str, Any]
    ] = []

    bootstrap_results: dict[
        str,
        Any
    ] = {}

    for seed in SEEDS:
        seed_df = (
            combined_predictions[
                combined_predictions[
                    "seed"
                ].eq(seed)
            ]
            .copy()
            .sort_values(
                "case_id"
            )
            .reset_index(
                drop=True
            )
        )

        if len(seed_df) != (
            EXPECTED_DEV_CASES
        ):
            raise RuntimeError(
                f"Seed {seed} OOF count "
                f"expected {EXPECTED_DEV_CASES}, "
                f"found {len(seed_df)}"
            )

        if seed_df[
            "case_id"
        ].nunique() != (
            EXPECTED_DEV_CASES
        ):
            raise RuntimeError(
                f"Seed {seed} has duplicate "
                "or missing OOF case IDs."
            )

        y_true = (
            seed_df[
                "true_idx"
            ]
            .astype(int)
            .to_numpy()
        )

        base_pred = (
            seed_df[
                "base_pred_idx"
            ]
            .astype(int)
            .to_numpy()
        )

        r1_pred = (
            seed_df[
                "calibrated_pred_idx"
            ]
            .astype(int)
            .to_numpy()
        )

        base_metrics = metric_bundle(
            y_true,
            base_pred,
        )

        r1_metrics = metric_bundle(
            y_true,
            r1_pred,
        )

        seed_rows.append(
            {
                "seed": seed,
                "baseline_macro_f1": (
                    base_metrics[
                        "macro_f1"
                    ]
                ),
                "r1_macro_f1": (
                    r1_metrics[
                        "macro_f1"
                    ]
                ),
                "delta_macro_f1": (
                    r1_metrics[
                        "macro_f1"
                    ]
                    - base_metrics[
                        "macro_f1"
                    ]
                ),
                "baseline_accuracy": (
                    base_metrics[
                        "accuracy"
                    ]
                ),
                "r1_accuracy": (
                    r1_metrics[
                        "accuracy"
                    ]
                ),
                "baseline_balanced_accuracy": (
                    base_metrics[
                        "balanced_accuracy"
                    ]
                ),
                "r1_balanced_accuracy": (
                    r1_metrics[
                        "balanced_accuracy"
                    ]
                ),
                "baseline_d_recall": (
                    base_metrics[
                        "per_class_recall"
                    ]["D"]
                ),
                "r1_d_recall": (
                    r1_metrics[
                        "per_class_recall"
                    ]["D"]
                ),
                "baseline_cd_errors": (
                    base_metrics[
                        "cd_error_count"
                    ]
                ),
                "r1_cd_errors": (
                    r1_metrics[
                        "cd_error_count"
                    ]
                ),
            }
        )

        bootstrap_results[
            str(seed)
        ] = bootstrap_seed_delta(
            y_true,
            base_pred,
            r1_pred,
            iterations=2000,
            seed=20260724 + seed,
        )

        seed_df.to_csv(
            OUTPUT
            / f"oof_seed{seed}_544.csv",
            index=False,
        )

        (
            OUTPUT
            / f"oof_seed{seed}_metrics.json"
        ).write_text(
            json.dumps(
                {
                    "baseline": (
                        base_metrics
                    ),
                    "r1": (
                        r1_metrics
                    ),
                    "bootstrap_delta": (
                        bootstrap_results[
                            str(seed)
                        ]
                    ),
                },
                indent=2,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

    seed_summary = pd.DataFrame(
        seed_rows
    )

    seed_summary.to_csv(
        OUTPUT
        / "seed_summary.csv",
        index=False,
    )

    pooled_y: list[int] = []
    pooled_base: list[int] = []
    pooled_r1: list[int] = []

    for seed in SEEDS:
        seed_df = (
            combined_predictions[
                combined_predictions[
                    "seed"
                ].eq(seed)
            ]
        )

        pooled_y.extend(
            seed_df[
                "true_idx"
            ]
            .astype(int)
            .tolist()
        )

        pooled_base.extend(
            seed_df[
                "base_pred_idx"
            ]
            .astype(int)
            .tolist()
        )

        pooled_r1.extend(
            seed_df[
                "calibrated_pred_idx"
            ]
            .astype(int)
            .tolist()
        )

    pooled_y_array = np.asarray(
        pooled_y,
        dtype=int,
    )

    pooled_base_array = np.asarray(
        pooled_base,
        dtype=int,
    )

    pooled_r1_array = np.asarray(
        pooled_r1,
        dtype=int,
    )

    pooled_base_metrics = (
        metric_bundle(
            pooled_y_array,
            pooled_base_array,
        )
    )

    pooled_r1_metrics = (
        metric_bundle(
            pooled_y_array,
            pooled_r1_array,
        )
    )

    mean_seed_delta = float(
        seed_summary[
            "delta_macro_f1"
        ].mean()
    )

    seed_wins = int(
        (
            seed_summary[
                "delta_macro_f1"
            ] > 0
        ).sum()
    )

    fold_wins = int(
        (
            fold_df[
                "delta_macro_f1"
            ] > 0
        ).sum()
    )

    all_bootstrap_positive = all(
        bootstrap_results[
            str(seed)
        ][
            "probability_delta_positive"
        ] >= 0.80
        for seed in SEEDS
    )

    promote = bool(
        mean_seed_delta >= 0.005
        and seed_wins >= 2
        and fold_wins >= 8
        and pooled_r1_metrics[
            "per_class_recall"
        ]["D"]
        >= pooled_base_metrics[
            "per_class_recall"
        ]["D"]
        and pooled_r1_metrics[
            "severe_error_count"
        ]
        <= pooled_base_metrics[
            "severe_error_count"
        ]
        and all_bootstrap_positive
    )

    decision = {
        "candidate": (
            "R1_CD_PAIRWISE_CALIBRATION"
        ),
        "protocol": (
            "5 outer folds x 3 seeds; "
            "alpha/beta fitted only on "
            "fold-specific inner validation; "
            "applied to untouched outer fold."
        ),
        "locked_test_evaluated": False,
        "expected_oof_cases_per_seed": (
            EXPECTED_DEV_CASES
        ),
        "seed_count": len(SEEDS),
        "fold_count": len(FOLDS),
        "pooled_baseline_metrics": (
            pooled_base_metrics
        ),
        "pooled_r1_metrics": (
            pooled_r1_metrics
        ),
        "mean_seed_delta_macro_f1": (
            mean_seed_delta
        ),
        "seed_wins": seed_wins,
        "fold_wins": fold_wins,
        "bootstrap_by_seed": (
            bootstrap_results
        ),
        "promotion_rule": {
            "mean_seed_delta_at_least": (
                0.005
            ),
            "seed_wins_at_least": 2,
            "fold_wins_at_least": 8,
            "d_recall_not_lower": True,
            "severe_errors_not_higher": (
                True
            ),
            "bootstrap_probability_positive_each_seed_at_least": (
                0.80
            ),
        },
        "promote_to_locked_test": (
            promote
        ),
        "next_action": (
            "Lock one final calibration policy "
            "and evaluate locked test once."
            if promote
            else
            "Reject R1; keep current E1 and "
            "do not reopen locked test."
        ),
    }

    (
        OUTPUT
        / "bootstrap_comparison.json"
    ).write_text(
        json.dumps(
            bootstrap_results,
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    (
        OUTPUT
        / "final_decision.json"
    ).write_text(
        json.dumps(
            decision,
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    plot_summary(
        seed_summary,
        pooled_base_metrics,
        pooled_r1_metrics,
    )

    (
        OUTPUT
        / "PIPELINE_DONE.txt"
    ).write_text(
        "R1 strict OOF 5x3 completed.\n"
        "Locked test was not evaluated.\n",
        encoding="utf-8",
    )

    print()
    print(
        "============================================================"
    )
    print(
        " FINAL STRICT OOF DECISION"
    )
    print(
        "============================================================"
    )
    print(
        "BASELINE_POOLED_MACRO_F1="
        f"{pooled_base_metrics['macro_f1']:.6f}"
    )
    print(
        "R1_POOLED_MACRO_F1="
        f"{pooled_r1_metrics['macro_f1']:.6f}"
    )
    print(
        "MEAN_SEED_DELTA="
        f"{mean_seed_delta:+.6f}"
    )
    print(
        f"SEED_WINS={seed_wins}/3"
    )
    print(
        f"FOLD_WINS={fold_wins}/15"
    )
    print(
        "BASELINE_D_RECALL="
        f"{pooled_base_metrics['per_class_recall']['D']:.6f}"
    )
    print(
        "R1_D_RECALL="
        f"{pooled_r1_metrics['per_class_recall']['D']:.6f}"
    )
    print(
        "PROMOTE_TO_LOCKED_TEST="
        f"{promote}"
    )
    print(
        "LOCKED_TEST_EVALUATED=False"
    )
    print(
        f"OUTPUT_DIR={OUTPUT}"
    )


if __name__ == "__main__":
    try:
        main()
    except Exception:
        failure = traceback.format_exc()

        (
            OUTPUT
            / "PIPELINE_FAILED.txt"
        ).write_text(
            failure,
            encoding="utf-8",
        )

        print(
            "============================================================"
        )
        print(
            " PIPELINE FAILED"
        )
        print(
            "============================================================"
        )
        print(failure)
