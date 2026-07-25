from __future__ import annotations

import json
import math
import traceback
from pathlib import Path
from typing import Any

import joblib
import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from sklearn.linear_model import LogisticRegression
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

SOURCE_OOF = (
    ROOT
    / "experiments"
    / "r1_strict_oof5x3_20260724_181205"
)

OUT = Path(__file__).resolve().parent

SEEDS = [42, 43, 44]
FOLDS = [0, 1, 2, 3, 4]
LABELS = ["A", "B", "C", "D"]
EXPECTED_CASES = 544


def normalize_case_id(value: Any) -> str:
    if pd.isna(value):
        return ""

    text = str(value).strip()

    if text.endswith(".0") and text[:-2].isdigit():
        return text[:-2]

    return text


def softmax(logits: np.ndarray) -> np.ndarray:
    shifted = logits - logits.max(axis=1, keepdims=True)
    exp_values = np.exp(shifted)

    return exp_values / exp_values.sum(
        axis=1,
        keepdims=True,
    )


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

    class_f1 = f1_score(
        y_true,
        y_pred,
        labels=[0, 1, 2, 3],
        average=None,
        zero_division=0,
    )

    severe_errors = 0
    within_one = 0

    for true_idx in range(4):
        for pred_idx in range(4):
            count = int(cm[true_idx, pred_idx])

            if abs(true_idx - pred_idx) >= 2:
                severe_errors += count

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
            label: float(class_f1[index])
            for index, label in enumerate(LABELS)
        },
        "confusion_matrix": cm.tolist(),
        "c_to_d": int(cm[2, 3]),
        "d_to_c": int(cm[3, 2]),
        "cd_error_count": int(cm[2, 3] + cm[3, 2]),
        "severe_error_count": int(severe_errors),
        "within_one": (
            float(within_one / total)
            if total > 0
            else 0.0
        ),
    }


def ranking(
    metrics: dict[str, Any],
) -> tuple[float, ...]:
    return (
        float(metrics["macro_f1"]),
        float(metrics["balanced_accuracy"]),
        float(metrics["per_class_recall"]["D"]),
        -float(metrics["cd_error_count"]),
        -float(metrics["severe_error_count"]),
    )


def load_prediction_csv(
    path: Path,
) -> pd.DataFrame:
    if not path.is_file():
        raise FileNotFoundError(
            f"Missing prediction file: {path}"
        )

    df = pd.read_csv(
        path,
        dtype={"case_id": "string"},
    )

    required = {
        "case_id",
        "true_idx",
        "base_pred_idx",
        "logit_A",
        "logit_B",
        "logit_C",
        "logit_D",
    }

    missing = sorted(
        required - set(df.columns)
    )

    if missing:
        raise RuntimeError(
            f"{path} missing columns: {missing}"
        )

    df["case_id"] = (
        df["case_id"]
        .map(normalize_case_id)
        .astype(str)
    )

    return df


def extract_logits(
    df: pd.DataFrame,
) -> np.ndarray:
    return df[
        [
            "logit_A",
            "logit_B",
            "logit_C",
            "logit_D",
        ]
    ].to_numpy(dtype=np.float64)


def specialist_features(
    logits: np.ndarray,
) -> np.ndarray:
    probabilities = softmax(logits)

    cd_sum = (
        probabilities[:, 2]
        + probabilities[:, 3]
    )

    cd_margin_logit = (
        logits[:, 3]
        - logits[:, 2]
    )

    cd_margin_prob = (
        probabilities[:, 3]
        - probabilities[:, 2]
    )

    entropy = -np.sum(
        probabilities
        * np.log(
            np.clip(
                probabilities,
                1e-8,
                1.0,
            )
        ),
        axis=1,
    )

    return np.column_stack(
        [
            logits[:, 2],
            logits[:, 3],
            cd_margin_logit,
            probabilities[:, 2],
            probabilities[:, 3],
            cd_margin_prob,
            cd_sum,
            probabilities.max(axis=1),
            entropy,
        ]
    )


def cd_gate_mask(
    logits: np.ndarray,
) -> np.ndarray:
    top_two = np.argsort(
        logits,
        axis=1,
    )[:, -2:]

    return np.asarray(
        [
            set(pair.tolist()) == {2, 3}
            for pair in top_two
        ],
        dtype=bool,
    )


def apply_specialist(
    logits: np.ndarray,
    model: LogisticRegression,
    threshold: float,
) -> tuple[np.ndarray, np.ndarray]:
    predictions = logits.argmax(axis=1)
    gate = cd_gate_mask(logits)

    specialist_probability = np.full(
        len(logits),
        np.nan,
        dtype=np.float64,
    )

    if gate.any():
        features = specialist_features(
            logits[gate]
        )

        probability_d = model.predict_proba(
            features
        )[:, 1]

        specialist_probability[gate] = (
            probability_d
        )

        predictions[gate] = np.where(
            probability_d >= threshold,
            3,
            2,
        )

    return predictions, specialist_probability


def fit_fold_specialist(
    inner_df: pd.DataFrame,
) -> dict[str, Any]:
    inner_logits = extract_logits(
        inner_df
    )

    inner_y = (
        inner_df["true_idx"]
        .astype(int)
        .to_numpy()
    )

    train_cd = np.isin(
        inner_y,
        [2, 3],
    )

    if train_cd.sum() < 10:
        raise RuntimeError(
            "Too few C/D samples in inner validation."
        )

    train_features = specialist_features(
        inner_logits[train_cd]
    )

    train_binary = (
        inner_y[train_cd] == 3
    ).astype(int)

    if len(np.unique(train_binary)) != 2:
        raise RuntimeError(
            "Inner validation does not contain both C and D."
        )

    baseline_pred = inner_logits.argmax(axis=1)
    baseline_metrics = metric_bundle(
        inner_y,
        baseline_pred,
    )

    c_values = [
        0.001,
        0.003,
        0.01,
        0.03,
        0.1,
        0.3,
        1.0,
        3.0,
        10.0,
    ]

    class_weights: list[Any] = [
        None,
        "balanced",
        {0: 1.0, 1: 1.25},
        {0: 1.0, 1: 1.50},
        {0: 1.0, 1: 2.00},
    ]

    thresholds = np.linspace(
        0.25,
        0.75,
        21,
    )

    best_model: LogisticRegression | None = None
    best_threshold: float | None = None
    best_metrics: dict[str, Any] | None = None
    best_predictions: np.ndarray | None = None
    best_rank: tuple[float, ...] | None = None
    best_parameters: dict[str, Any] | None = None

    grid_rows: list[dict[str, Any]] = []

    for c_value in c_values:
        for class_weight in class_weights:
            model = LogisticRegression(
                C=c_value,
                class_weight=class_weight,
                max_iter=5000,
                solver="liblinear",
                random_state=42,
            )

            model.fit(
                train_features,
                train_binary,
            )

            for threshold in thresholds:
                predictions, _ = apply_specialist(
                    inner_logits,
                    model,
                    float(threshold),
                )

                metrics = metric_bundle(
                    inner_y,
                    predictions,
                )

                current_rank = ranking(
                    metrics
                )

                grid_rows.append({
                    "C": c_value,
                    "class_weight": str(
                        class_weight
                    ),
                    "threshold": float(
                        threshold
                    ),
                    "macro_f1": (
                        metrics["macro_f1"]
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
                })

                if (
                    best_rank is None
                    or current_rank > best_rank
                ):
                    best_rank = current_rank
                    best_model = model
                    best_threshold = float(
                        threshold
                    )
                    best_metrics = metrics
                    best_predictions = (
                        predictions
                    )
                    best_parameters = {
                        "C": c_value,
                        "class_weight": (
                            class_weight
                        ),
                        "threshold": float(
                            threshold
                        ),
                    }

    if (
        best_model is None
        or best_threshold is None
        or best_metrics is None
        or best_predictions is None
        or best_parameters is None
    ):
        raise RuntimeError(
            "No specialist candidate selected."
        )

    return {
        "model": best_model,
        "threshold": best_threshold,
        "parameters": best_parameters,
        "baseline_metrics": (
            baseline_metrics
        ),
        "selected_metrics": (
            best_metrics
        ),
        "selected_predictions": (
            best_predictions
        ),
        "grid": grid_rows,
        "inner_cd_samples": int(
            train_cd.sum()
        ),
        "inner_c_samples": int(
            np.sum(train_binary == 0)
        ),
        "inner_d_samples": int(
            np.sum(train_binary == 1)
        ),
    }


def bootstrap_delta(
    y_true: np.ndarray,
    base_pred: np.ndarray,
    specialist_pred: np.ndarray,
    iterations: int,
    seed: int,
) -> dict[str, Any]:
    rng = np.random.default_rng(seed)
    n = len(y_true)

    deltas: list[float] = []

    for _ in range(iterations):
        indices = rng.integers(
            0,
            n,
            size=n,
        )

        baseline_f1 = f1_score(
            y_true[indices],
            base_pred[indices],
            labels=[0, 1, 2, 3],
            average="macro",
            zero_division=0,
        )

        specialist_f1 = f1_score(
            y_true[indices],
            specialist_pred[indices],
            labels=[0, 1, 2, 3],
            average="macro",
            zero_division=0,
        )

        deltas.append(
            float(
                specialist_f1
                - baseline_f1
            )
        )

    values = np.asarray(
        deltas,
        dtype=np.float64,
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
        "probability_delta_positive": float(
            np.mean(values > 0)
        ),
    }


def run_fold(
    seed: int,
    fold: int,
) -> dict[str, Any]:
    source_dir = (
        SOURCE_OOF
        / "fold_runs"
        / f"seed{seed}_fold{fold}"
    )

    inner_path = (
        source_dir
        / "inner_valid"
        / "predictions.csv"
    )

    outer_path = (
        source_dir
        / "outer_eval"
        / "predictions.csv"
    )

    run_dir = (
        OUT
        / "fold_runs"
        / f"seed{seed}_fold{fold}"
    )

    run_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    inner_df = load_prediction_csv(
        inner_path
    )

    outer_df = load_prediction_csv(
        outer_path
    )

    fitted = fit_fold_specialist(
        inner_df
    )

    model = fitted["model"]
    threshold = fitted["threshold"]

    outer_logits = extract_logits(
        outer_df
    )

    outer_y = (
        outer_df["true_idx"]
        .astype(int)
        .to_numpy()
    )

    base_pred = outer_logits.argmax(
        axis=1
    )

    specialist_pred, specialist_prob = (
        apply_specialist(
            outer_logits,
            model,
            threshold,
        )
    )

    baseline_metrics = metric_bundle(
        outer_y,
        base_pred,
    )

    specialist_metrics = metric_bundle(
        outer_y,
        specialist_pred,
    )

    outer_result = outer_df.copy()

    outer_result[
        "specialist_pred_idx"
    ] = specialist_pred

    outer_result[
        "specialist_pred_label"
    ] = [
        LABELS[index]
        for index in specialist_pred
    ]

    outer_result[
        "specialist_probability_D"
    ] = specialist_prob

    outer_result["seed"] = seed
    outer_result["fold"] = fold

    outer_result[
        "selected_C"
    ] = fitted["parameters"]["C"]

    outer_result[
        "selected_class_weight"
    ] = str(
        fitted[
            "parameters"
        ]["class_weight"]
    )

    outer_result[
        "selected_threshold"
    ] = threshold

    outer_result.to_csv(
        run_dir
        / "outer_predictions_specialist.csv",
        index=False,
    )

    pd.DataFrame(
        fitted["grid"]
    ).to_csv(
        run_dir
        / "inner_specialist_grid.csv",
        index=False,
    )

    joblib.dump(
        model,
        run_dir
        / "cd_specialist.joblib",
    )

    summary = {
        "seed": seed,
        "fold": fold,
        "inner_valid_count": int(
            len(inner_df)
        ),
        "outer_eval_count": int(
            len(outer_df)
        ),
        "inner_cd_samples": (
            fitted["inner_cd_samples"]
        ),
        "inner_c_samples": (
            fitted["inner_c_samples"]
        ),
        "inner_d_samples": (
            fitted["inner_d_samples"]
        ),
        "selected_parameters": (
            fitted["parameters"]
        ),
        "inner_baseline_metrics": (
            fitted["baseline_metrics"]
        ),
        "inner_selected_metrics": (
            fitted["selected_metrics"]
        ),
        "outer_baseline_metrics": (
            baseline_metrics
        ),
        "outer_specialist_metrics": (
            specialist_metrics
        ),
        "outer_delta_macro_f1": (
            specialist_metrics[
                "macro_f1"
            ]
            - baseline_metrics[
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
            summary,
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
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
        "C="
        f"{fitted['parameters']['C']}"
    )
    print(
        "CLASS_WEIGHT="
        f"{fitted['parameters']['class_weight']}"
    )
    print(
        "THRESHOLD="
        f"{threshold}"
    )
    print(
        "OUTER_BASE_MACRO_F1="
        f"{baseline_metrics['macro_f1']:.6f}"
    )
    print(
        "OUTER_R2_MACRO_F1="
        f"{specialist_metrics['macro_f1']:.6f}"
    )
    print(
        "OUTER_DELTA="
        f"{summary['outer_delta_macro_f1']:+.6f}"
    )

    return {
        "summary": summary,
        "predictions": outer_result,
    }


def create_plot(
    seed_summary: pd.DataFrame,
    pooled_baseline: dict[str, Any],
    pooled_specialist: dict[str, Any],
    mean_seed_delta: float,
    fold_wins: int,
) -> None:
    fig = plt.figure(
        figsize=(15, 9)
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
        grid[0, :]
    )
    title_ax.axis("off")

    title_ax.text(
        0.0,
        0.72,
        "R2 C/D Specialist — Strict 5-Fold × 3-Seed OOF",
        fontsize=23,
        fontweight="bold",
    )

    title_ax.text(
        0.0,
        0.20,
        "Specialist fitted on fold-specific inner validation and applied to untouched outer folds. Locked test not used.",
        fontsize=11,
    )

    cards = [
        (
            "Baseline OOF Macro-F1",
            pooled_baseline["macro_f1"],
            "percent",
        ),
        (
            "R2 OOF Macro-F1",
            pooled_specialist["macro_f1"],
            "percent",
        ),
        (
            "Mean seed delta",
            mean_seed_delta,
            "delta",
        ),
        (
            "Baseline D recall",
            pooled_baseline[
                "per_class_recall"
            ]["D"],
            "percent",
        ),
        (
            "R2 D recall",
            pooled_specialist[
                "per_class_recall"
            ]["D"],
            "percent",
        ),
        (
            "Fold wins",
            fold_wins,
            "count",
        ),
    ]

    for index, (
        title,
        value,
        value_type,
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

        if value_type == "percent":
            display = f"{value * 100:.2f}%"
        elif value_type == "delta":
            display = f"{value * 100:+.2f} pts"
        else:
            display = f"{int(value)}/15"

        ax.text(
            0.5,
            0.68,
            title,
            ha="center",
            va="center",
            fontsize=10,
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

    x = np.arange(
        len(seed_summary)
    )

    width = 0.35

    macro_ax = fig.add_subplot(
        grid[2, 0:4]
    )

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
            "r2_macro_f1"
        ],
        width,
        label="R2 specialist",
    )

    macro_ax.set_title(
        "OOF Macro-F1 by seed",
        fontweight="bold",
    )

    macro_ax.set_xticks(
        x,
        [
            f"Seed {seed}"
            for seed in SEEDS
        ],
    )

    macro_ax.set_ylim(0, 1)
    macro_ax.legend()

    recall_ax = fig.add_subplot(
        grid[2, 4:8]
    )

    recall_ax.bar(
        x - width / 2,
        seed_summary[
            "baseline_d_recall"
        ],
        width,
        label="Baseline",
    )

    recall_ax.bar(
        x + width / 2,
        seed_summary[
            "r2_d_recall"
        ],
        width,
        label="R2 specialist",
    )

    recall_ax.set_title(
        "Class D recall by seed",
        fontweight="bold",
    )

    recall_ax.set_xticks(
        x,
        [
            f"Seed {seed}"
            for seed in SEEDS
        ],
    )

    recall_ax.set_ylim(0, 1)
    recall_ax.legend()

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
            "r2_cd_errors"
        ],
        width,
        label="R2 specialist",
    )

    error_ax.set_title(
        "C↔D errors by seed",
        fontweight="bold",
    )

    error_ax.set_xticks(
        x,
        [
            f"Seed {seed}"
            for seed in SEEDS
        ],
    )

    error_ax.legend()

    fig.savefig(
        OUT / "comparison_oof.png",
        dpi=180,
        bbox_inches="tight",
    )

    plt.close(fig)


def main() -> None:
    print(
        "============================================================"
    )
    print(
        " R2 STRICT C/D SPECIALIST OOF 5x3"
    )
    print(
        " NO BACKBONE TRAINING"
    )
    print(
        " LOCKED TEST 132 IS NOT USED"
    )
    print(
        "============================================================"
    )

    all_predictions: list[
        pd.DataFrame
    ] = []

    fold_rows: list[
        dict[str, Any]
    ] = []

    for seed in SEEDS:
        for fold in FOLDS:
            result = run_fold(
                seed,
                fold,
            )

            all_predictions.append(
                result["predictions"]
            )

            summary = result["summary"]

            baseline = summary[
                "outer_baseline_metrics"
            ]

            specialist = summary[
                "outer_specialist_metrics"
            ]

            fold_rows.append({
                "seed": seed,
                "fold": fold,
                "C": (
                    summary[
                        "selected_parameters"
                    ]["C"]
                ),
                "class_weight": str(
                    summary[
                        "selected_parameters"
                    ]["class_weight"]
                ),
                "threshold": (
                    summary[
                        "selected_parameters"
                    ]["threshold"]
                ),
                "baseline_macro_f1": (
                    baseline["macro_f1"]
                ),
                "r2_macro_f1": (
                    specialist["macro_f1"]
                ),
                "delta_macro_f1": (
                    specialist["macro_f1"]
                    - baseline["macro_f1"]
                ),
                "baseline_d_recall": (
                    baseline[
                        "per_class_recall"
                    ]["D"]
                ),
                "r2_d_recall": (
                    specialist[
                        "per_class_recall"
                    ]["D"]
                ),
                "baseline_cd_errors": (
                    baseline[
                        "cd_error_count"
                    ]
                ),
                "r2_cd_errors": (
                    specialist[
                        "cd_error_count"
                    ]
                ),
            })

    combined = pd.concat(
        all_predictions,
        ignore_index=True,
    )

    combined["case_id"] = (
        combined["case_id"]
        .map(normalize_case_id)
        .astype(str)
    )

    combined.to_csv(
        OUT / "all_outer_predictions.csv",
        index=False,
    )

    fold_df = pd.DataFrame(
        fold_rows
    )

    fold_df.to_csv(
        OUT / "fold_summary.csv",
        index=False,
    )

    seed_rows: list[
        dict[str, Any]
    ] = []

    bootstrap_results: dict[
        str,
        Any
    ] = {}

    pooled_true: list[int] = []
    pooled_baseline: list[int] = []
    pooled_specialist: list[int] = []

    for seed in SEEDS:
        seed_df = (
            combined[
                combined["seed"].eq(seed)
            ]
            .copy()
            .sort_values(
                "case_id",
                kind="stable",
            )
            .reset_index(drop=True)
        )

        row_count = int(
            len(seed_df)
        )

        unique_count = int(
            seed_df["case_id"]
            .nunique(dropna=False)
        )

        print(
            f"SEED={seed} "
            f"ROWS={row_count} "
            f"UNIQUE_CASES={unique_count}"
        )

        if row_count != EXPECTED_CASES:
            raise RuntimeError(
                f"Seed {seed}: expected "
                f"{EXPECTED_CASES} rows, "
                f"found {row_count}"
            )

        if unique_count != EXPECTED_CASES:
            raise RuntimeError(
                f"Seed {seed}: expected "
                f"{EXPECTED_CASES} unique IDs, "
                f"found {unique_count}"
            )

        y_true = (
            seed_df["true_idx"]
            .astype(int)
            .to_numpy()
        )

        base_pred = (
            seed_df["base_pred_idx"]
            .astype(int)
            .to_numpy()
        )

        specialist_pred = (
            seed_df[
                "specialist_pred_idx"
            ]
            .astype(int)
            .to_numpy()
        )

        baseline_metrics = metric_bundle(
            y_true,
            base_pred,
        )

        specialist_metrics = metric_bundle(
            y_true,
            specialist_pred,
        )

        bootstrap = bootstrap_delta(
            y_true,
            base_pred,
            specialist_pred,
            iterations=2000,
            seed=20260724 + seed,
        )

        bootstrap_results[
            str(seed)
        ] = bootstrap

        seed_rows.append({
            "seed": seed,
            "baseline_macro_f1": (
                baseline_metrics[
                    "macro_f1"
                ]
            ),
            "r2_macro_f1": (
                specialist_metrics[
                    "macro_f1"
                ]
            ),
            "delta_macro_f1": (
                specialist_metrics[
                    "macro_f1"
                ]
                - baseline_metrics[
                    "macro_f1"
                ]
            ),
            "baseline_accuracy": (
                baseline_metrics[
                    "accuracy"
                ]
            ),
            "r2_accuracy": (
                specialist_metrics[
                    "accuracy"
                ]
            ),
            "baseline_balanced_accuracy": (
                baseline_metrics[
                    "balanced_accuracy"
                ]
            ),
            "r2_balanced_accuracy": (
                specialist_metrics[
                    "balanced_accuracy"
                ]
            ),
            "baseline_d_recall": (
                baseline_metrics[
                    "per_class_recall"
                ]["D"]
            ),
            "r2_d_recall": (
                specialist_metrics[
                    "per_class_recall"
                ]["D"]
            ),
            "baseline_cd_errors": (
                baseline_metrics[
                    "cd_error_count"
                ]
            ),
            "r2_cd_errors": (
                specialist_metrics[
                    "cd_error_count"
                ]
            ),
        })

        seed_df.to_csv(
            OUT / f"oof_seed{seed}_544.csv",
            index=False,
        )

        (
            OUT
            / f"oof_seed{seed}_metrics.json"
        ).write_text(
            json.dumps(
                {
                    "baseline": (
                        baseline_metrics
                    ),
                    "r2_specialist": (
                        specialist_metrics
                    ),
                    "bootstrap_delta": (
                        bootstrap
                    ),
                },
                indent=2,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

        pooled_true.extend(
            y_true.tolist()
        )

        pooled_baseline.extend(
            base_pred.tolist()
        )

        pooled_specialist.extend(
            specialist_pred.tolist()
        )

    seed_summary = pd.DataFrame(
        seed_rows
    )

    seed_summary.to_csv(
        OUT / "seed_summary.csv",
        index=False,
    )

    pooled_true_array = np.asarray(
        pooled_true,
        dtype=int,
    )

    pooled_baseline_array = np.asarray(
        pooled_baseline,
        dtype=int,
    )

    pooled_specialist_array = np.asarray(
        pooled_specialist,
        dtype=int,
    )

    pooled_baseline_metrics = metric_bundle(
        pooled_true_array,
        pooled_baseline_array,
    )

    pooled_specialist_metrics = metric_bundle(
        pooled_true_array,
        pooled_specialist_array,
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

    bootstrap_gate = all(
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
        and pooled_specialist_metrics[
            "per_class_recall"
        ]["D"]
        >= pooled_baseline_metrics[
            "per_class_recall"
        ]["D"]
        and pooled_specialist_metrics[
            "cd_error_count"
        ]
        <= pooled_baseline_metrics[
            "cd_error_count"
        ]
        and pooled_specialist_metrics[
            "severe_error_count"
        ]
        <= pooled_baseline_metrics[
            "severe_error_count"
        ]
        and bootstrap_gate
    )

    decision = {
        "candidate": (
            "R2_STRICT_CD_SPECIALIST"
        ),
        "protocol": (
            "5 outer folds x 3 seeds. "
            "Binary C/D specialist and all "
            "hyperparameters fitted only on "
            "fold-specific inner validation; "
            "applied once to untouched outer fold."
        ),
        "locked_test_evaluated": False,
        "pooled_baseline_metrics": (
            pooled_baseline_metrics
        ),
        "pooled_r2_metrics": (
            pooled_specialist_metrics
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
            "mean_seed_delta_at_least": 0.005,
            "seed_wins_at_least": 2,
            "fold_wins_at_least": 8,
            "d_recall_not_lower": True,
            "cd_errors_not_higher": True,
            "severe_errors_not_higher": True,
            "bootstrap_probability_positive_each_seed_at_least": 0.80,
        },
        "promote_to_locked_test": (
            promote
        ),
        "next_action": (
            "Lock final specialist policy "
            "and evaluate locked test once."
            if promote
            else
            "Reject R2 specialist and do not "
            "reopen the locked test."
        ),
    }

    (
        OUT
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
        OUT
        / "final_decision.json"
    ).write_text(
        json.dumps(
            decision,
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    create_plot(
        seed_summary,
        pooled_baseline_metrics,
        pooled_specialist_metrics,
        mean_seed_delta,
        fold_wins,
    )

    (
        OUT / "PIPELINE_DONE.txt"
    ).write_text(
        "R2 strict specialist OOF completed.\n"
        "Locked test was not evaluated.\n",
        encoding="utf-8",
    )

    print()
    print(
        "============================================================"
    )
    print(
        " FINAL STRICT R2 DECISION"
    )
    print(
        "============================================================"
    )
    print(
        "BASELINE_POOLED_MACRO_F1="
        f"{pooled_baseline_metrics['macro_f1']:.6f}"
    )
    print(
        "R2_POOLED_MACRO_F1="
        f"{pooled_specialist_metrics['macro_f1']:.6f}"
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
        f"{pooled_baseline_metrics['per_class_recall']['D']:.6f}"
    )
    print(
        "R2_D_RECALL="
        f"{pooled_specialist_metrics['per_class_recall']['D']:.6f}"
    )
    print(
        "BASELINE_CD_ERRORS="
        f"{pooled_baseline_metrics['cd_error_count']}"
    )
    print(
        "R2_CD_ERRORS="
        f"{pooled_specialist_metrics['cd_error_count']}"
    )
    print(
        "PROMOTE_TO_LOCKED_TEST="
        f"{promote}"
    )
    print(
        "LOCKED_TEST_EVALUATED=False"
    )
    print(
        f"OUTPUT_DIR={OUT}"
    )


if __name__ == "__main__":
    try:
        main()
    except Exception:
        failure = traceback.format_exc()

        (
            OUT
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
