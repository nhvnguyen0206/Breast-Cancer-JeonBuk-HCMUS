from __future__ import annotations

import json
import traceback
from pathlib import Path
from typing import Any

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    cohen_kappa_score,
    confusion_matrix,
    f1_score,
    recall_score,
)

OUT = Path(
    "/mnt/hcmus/breast_vn/code/new_implement/"
    "tn-mammo-bestmacro-hientai/experiments/"
    "r1_strict_oof5x3_20260724_181205"
)

SEEDS = [42, 43, 44]
FOLDS = [0, 1, 2, 3, 4]
LABELS = ["A", "B", "C", "D"]
EXPECTED_CASES = 544


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


def bootstrap_delta(
    y_true: np.ndarray,
    base_pred: np.ndarray,
    r1_pred: np.ndarray,
    iterations: int,
    seed: int,
) -> dict[str, Any]:
    rng = np.random.default_rng(seed)
    n = len(y_true)
    deltas = []

    for _ in range(iterations):
        indices = rng.integers(
            0,
            n,
            size=n,
        )

        base_f1 = f1_score(
            y_true[indices],
            base_pred[indices],
            labels=[0, 1, 2, 3],
            average="macro",
            zero_division=0,
        )

        r1_f1 = f1_score(
            y_true[indices],
            r1_pred[indices],
            labels=[0, 1, 2, 3],
            average="macro",
            zero_division=0,
        )

        deltas.append(
            float(r1_f1 - base_f1)
        )

    values = np.asarray(deltas)

    return {
        "iterations": iterations,
        "mean_delta": float(values.mean()),
        "median_delta": float(np.median(values)),
        "ci95_low": float(np.quantile(values, 0.025)),
        "ci95_high": float(np.quantile(values, 0.975)),
        "probability_delta_positive": float(
            np.mean(values > 0)
        ),
    }


def normalize_case_id(value: Any) -> str:
    if pd.isna(value):
        return ""

    text = str(value).strip()

    if text.endswith(".0"):
        integer_part = text[:-2]

        if integer_part.isdigit():
            return integer_part

    return text


def main() -> None:
    prediction_frames = []
    fold_rows = []

    print("============================================================")
    print(" FINALIZE EXISTING R1 STRICT OOF RESULTS")
    print(" NO INFERENCE — NO LOCKED TEST")
    print("============================================================")

    for seed in SEEDS:
        for fold in FOLDS:
            run_dir = (
                OUT
                / "fold_runs"
                / f"seed{seed}_fold{fold}"
            )

            pred_path = (
                run_dir
                / "outer_predictions_calibrated.csv"
            )

            summary_path = (
                run_dir
                / "fold_summary.json"
            )

            if not pred_path.is_file():
                raise FileNotFoundError(
                    f"Missing: {pred_path}"
                )

            if not summary_path.is_file():
                raise FileNotFoundError(
                    f"Missing: {summary_path}"
                )

            df = pd.read_csv(
                pred_path,
                dtype={"case_id": "string"},
            )

            df["case_id"] = (
                df["case_id"]
                .map(normalize_case_id)
                .astype(str)
            )

            df["seed"] = seed
            df["fold"] = fold

            prediction_frames.append(df)

            summary = json.loads(
                summary_path.read_text(
                    encoding="utf-8"
                )
            )

            base = summary[
                "outer_baseline_metrics"
            ]

            r1 = summary[
                "outer_calibrated_metrics"
            ]

            fold_rows.append({
                "seed": seed,
                "fold": fold,
                "alpha": summary["selected_alpha"],
                "beta": summary["selected_beta"],
                "baseline_macro_f1": base["macro_f1"],
                "r1_macro_f1": r1["macro_f1"],
                "delta_macro_f1": (
                    r1["macro_f1"]
                    - base["macro_f1"]
                ),
                "baseline_d_recall": (
                    base["per_class_recall"]["D"]
                ),
                "r1_d_recall": (
                    r1["per_class_recall"]["D"]
                ),
                "baseline_cd_errors": (
                    base["cd_error_count"]
                ),
                "r1_cd_errors": (
                    r1["cd_error_count"]
                ),
            })

            print(
                f"[PASS] seed={seed} fold={fold} "
                f"rows={len(df)}"
            )

    combined = pd.concat(
        prediction_frames,
        ignore_index=True,
    )

    combined.to_csv(
        OUT / "all_outer_predictions.csv",
        index=False,
    )

    fold_df = pd.DataFrame(fold_rows)

    fold_df.to_csv(
        OUT / "fold_summary.csv",
        index=False,
    )

    seed_rows = []
    bootstrap_results = {}

    pooled_true = []
    pooled_base = []
    pooled_r1 = []

    for seed in SEEDS:
        seed_df = (
            combined[
                combined["seed"].eq(seed)
            ]
            .copy()
        )

        seed_df["case_id"] = (
            seed_df["case_id"]
            .astype(str)
        )

        seed_df = (
            seed_df
            .sort_values(
                "case_id",
                kind="stable",
            )
            .reset_index(drop=True)
        )

        row_count = len(seed_df)
        unique_count = (
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
            duplicates = (
                seed_df[
                    seed_df["case_id"].duplicated(
                        keep=False
                    )
                ][["case_id", "fold"]]
                .sort_values("case_id")
            )

            duplicates.to_csv(
                OUT / f"duplicate_case_ids_seed{seed}.csv",
                index=False,
            )

            raise RuntimeError(
                f"Seed {seed}: expected "
                f"{EXPECTED_CASES} unique case IDs, "
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

        r1_pred = (
            seed_df["calibrated_pred_idx"]
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

        bootstrap = bootstrap_delta(
            y_true,
            base_pred,
            r1_pred,
            iterations=2000,
            seed=20260724 + seed,
        )

        bootstrap_results[str(seed)] = bootstrap

        seed_rows.append({
            "seed": seed,
            "baseline_macro_f1": (
                base_metrics["macro_f1"]
            ),
            "r1_macro_f1": (
                r1_metrics["macro_f1"]
            ),
            "delta_macro_f1": (
                r1_metrics["macro_f1"]
                - base_metrics["macro_f1"]
            ),
            "baseline_accuracy": (
                base_metrics["accuracy"]
            ),
            "r1_accuracy": (
                r1_metrics["accuracy"]
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
                    "baseline": base_metrics,
                    "r1": r1_metrics,
                    "bootstrap_delta": bootstrap,
                },
                indent=2,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

        pooled_true.extend(
            y_true.tolist()
        )

        pooled_base.extend(
            base_pred.tolist()
        )

        pooled_r1.extend(
            r1_pred.tolist()
        )

    seed_summary = pd.DataFrame(
        seed_rows
    )

    seed_summary.to_csv(
        OUT / "seed_summary.csv",
        index=False,
    )

    pooled_true = np.asarray(
        pooled_true,
        dtype=int,
    )

    pooled_base = np.asarray(
        pooled_base,
        dtype=int,
    )

    pooled_r1 = np.asarray(
        pooled_r1,
        dtype=int,
    )

    pooled_base_metrics = metric_bundle(
        pooled_true,
        pooled_base,
    )

    pooled_r1_metrics = metric_bundle(
        pooled_true,
        pooled_r1,
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
        bootstrap_results[str(seed)][
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
        and bootstrap_gate
    )

    decision = {
        "candidate": "R1_CD_PAIRWISE_CALIBRATION",
        "protocol": (
            "5 outer folds x 3 seeds; "
            "alpha/beta fitted on fold-specific "
            "inner validation and applied to "
            "untouched outer evaluation."
        ),
        "locked_test_evaluated": False,
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
        "promote_to_locked_test": promote,
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
        OUT / "bootstrap_comparison.json"
    ).write_text(
        json.dumps(
            bootstrap_results,
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    (
        OUT / "final_decision.json"
    ).write_text(
        json.dumps(
            decision,
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    fig = plt.figure(
        figsize=(15, 9)
    )

    grid = fig.add_gridspec(
        3,
        12,
        height_ratios=[0.8, 1.4, 3.2],
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
        "R1 C/D Calibration — Strict 5-Fold × 3-Seed OOF",
        fontsize=23,
        fontweight="bold",
    )

    title_ax.text(
        0.0,
        0.20,
        "Inner-validation calibration applied to untouched outer folds. Locked test not used.",
        fontsize=11,
    )

    cards = [
        (
            "Baseline OOF Macro-F1",
            pooled_base_metrics["macro_f1"],
            "percent",
        ),
        (
            "R1 OOF Macro-F1",
            pooled_r1_metrics["macro_f1"],
            "percent",
        ),
        (
            "Mean seed delta",
            mean_seed_delta,
            "delta",
        ),
        (
            "Baseline D recall",
            pooled_base_metrics[
                "per_class_recall"
            ]["D"],
            "percent",
        ),
        (
            "R1 D recall",
            pooled_r1_metrics[
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
            "r1_d_recall"
        ],
        width,
        label="R1",
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

    (
        OUT / "PIPELINE_DONE.txt"
    ).write_text(
        "R1 strict OOF finalization completed.\n"
        "Locked test was not evaluated.\n",
        encoding="utf-8",
    )

    failed_file = (
        OUT / "PIPELINE_FAILED.txt"
    )

    if failed_file.exists():
        failed_file.rename(
            OUT / "PIPELINE_FAILED_original_sort_error.txt"
        )

    print()
    print("============================================================")
    print(" FINAL STRICT OOF DECISION")
    print("============================================================")
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
        f"OUTPUT_DIR={OUT}"
    )


if __name__ == "__main__":
    try:
        main()
    except Exception:
        failure = traceback.format_exc()

        (
            OUT
            / "FINALIZATION_FAILED.txt"
        ).write_text(
            failure,
            encoding="utf-8",
        )

        print("============================================================")
        print(" FINALIZATION FAILED")
        print("============================================================")
        print(failure)
