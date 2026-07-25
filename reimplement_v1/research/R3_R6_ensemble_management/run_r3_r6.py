from __future__ import annotations

import itertools
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
)
from sklearn.model_selection import GroupKFold
from sklearn.neighbors import NearestNeighbors
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


try:
    from sklearn.model_selection import StratifiedGroupKFold
except ImportError:
    StratifiedGroupKFold = None


ROOT_V2 = Path(
    "/mnt/hcmus/breast_vn/code/new_implement_v2"
)

E1_TEST_DIR = Path(
    "/mnt/hcmus/breast_vn/code/new_implement/"
    "outputs/FINAL_TN_LOCKED_TEST132_E1_20260721_153338"
)

R2_OOF_DIR = Path(
    "/mnt/hcmus/breast_vn/code/new_implement/"
    "tn-mammo-bestmacro-hientai/experiments/"
    "r2_strict_cd_specialist_oof5x3_20260724_184412"
)

OUT = Path(__file__).resolve().parent

LABELS = ["A", "B", "C", "D"]
RANDOM_STATE = 20260725


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


def normalize_probabilities(
    probabilities: np.ndarray,
) -> np.ndarray:
    probabilities = np.asarray(
        probabilities,
        dtype=np.float64,
    )

    probabilities = np.clip(
        probabilities,
        1e-8,
        1.0,
    )

    return probabilities / probabilities.sum(
        axis=1,
        keepdims=True,
    )


def entropy_from_probs(
    probabilities: np.ndarray,
) -> np.ndarray:
    return -np.sum(
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


def top2_cd_mask(
    probabilities: np.ndarray,
) -> np.ndarray:
    top_two = np.argsort(
        probabilities,
        axis=1,
    )[:, -2:]

    return np.asarray(
        [
            set(pair.tolist()) == {2, 3}
            for pair in top_two
        ],
        dtype=bool,
    )


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

    entropy = entropy_from_probs(
        probabilities
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


def one_hot(
    values: np.ndarray,
    classes: int = 4,
) -> np.ndarray:
    output = np.zeros(
        (len(values), classes),
        dtype=np.float64,
    )

    output[
        np.arange(len(values)),
        values.astype(int),
    ] = 1.0

    return output


def build_meta_features(
    probabilities: np.ndarray,
    base_predictions: np.ndarray,
    r2_predictions: np.ndarray,
    specialist_probability_d: np.ndarray,
    specialist_margin: np.ndarray,
) -> tuple[np.ndarray, list[str]]:
    probabilities = normalize_probabilities(
        probabilities
    )

    sorted_probs = np.sort(
        probabilities,
        axis=1,
    )

    top1_confidence = sorted_probs[:, -1]

    top1_top2_margin = (
        sorted_probs[:, -1]
        - sorted_probs[:, -2]
    )

    entropy = entropy_from_probs(
        probabilities
    )

    cd_signed_margin = (
        probabilities[:, 3]
        - probabilities[:, 2]
    )

    cd_absolute_margin = np.abs(
        cd_signed_margin
    )

    cd_sum = (
        probabilities[:, 2]
        + probabilities[:, 3]
    )

    top2_cd = top2_cd_mask(
        probabilities
    ).astype(np.float64)

    disagreement = (
        base_predictions
        != r2_predictions
    ).astype(np.float64)

    base_one_hot = one_hot(
        base_predictions
    )

    r2_one_hot = one_hot(
        r2_predictions
    )

    features = np.column_stack(
        [
            probabilities,
            top1_confidence,
            top1_top2_margin,
            entropy,
            cd_signed_margin,
            cd_absolute_margin,
            cd_sum,
            top2_cd,
            specialist_probability_d,
            specialist_margin,
            disagreement,
            base_one_hot,
            r2_one_hot,
        ]
    )

    names = [
        "prob_A",
        "prob_B",
        "prob_C",
        "prob_D",
        "top1_confidence",
        "top1_top2_margin",
        "entropy",
        "cd_signed_margin",
        "cd_absolute_margin",
        "cd_probability_sum",
        "top2_is_cd",
        "specialist_probability_D",
        "specialist_margin",
        "base_r2_disagreement",
        "base_pred_A",
        "base_pred_B",
        "base_pred_C",
        "base_pred_D",
        "r2_pred_A",
        "r2_pred_B",
        "r2_pred_C",
        "r2_pred_D",
    ]

    return features, names


def metric_bundle(
    y_true: np.ndarray,
    y_pred: np.ndarray,
) -> dict[str, Any]:
    cm = confusion_matrix(
        y_true,
        y_pred,
        labels=[0, 1, 2, 3],
    )

    recalls = []

    for class_index in range(4):
        denominator = int(
            cm[class_index].sum()
        )

        recall = (
            float(
                cm[class_index, class_index]
                / denominator
            )
            if denominator > 0
            else 0.0
        )

        recalls.append(recall)

    severe_error_count = 0
    within_one_count = 0

    for true_index in range(4):
        for pred_index in range(4):
            count = int(
                cm[true_index, pred_index]
            )

            distance = abs(
                true_index - pred_index
            )

            if distance >= 2:
                severe_error_count += count

            if distance <= 1:
                within_one_count += count

    total = int(cm.sum())

    return {
        "num_samples": int(len(y_true)),
        "accuracy": float(
            accuracy_score(
                y_true,
                y_pred,
            )
        ),
        "balanced_accuracy": float(
            balanced_accuracy_score(
                y_true,
                y_pred,
            )
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
        "within_one": (
            float(
                within_one_count / total
            )
            if total > 0
            else 0.0
        ),
        "severe_error_count": int(
            severe_error_count
        ),
        "severe_error_rate": (
            float(
                severe_error_count / total
            )
            if total > 0
            else 0.0
        ),
        "per_class_recall": {
            label: float(recalls[index])
            for index, label in enumerate(
                LABELS
            )
        },
        "d_recall": float(
            recalls[3]
        ),
        "c_to_d": int(cm[2, 3]),
        "d_to_c": int(cm[3, 2]),
        "cd_total": int(
            cm[2, 3] + cm[3, 2]
        ),
        "confusion_matrix": cm.tolist(),
    }


def metric_rank(
    metrics: dict[str, Any],
    changed_count: int = 0,
) -> tuple[float, ...]:
    return (
        float(metrics["macro_f1"]),
        float(metrics["balanced_accuracy"]),
        float(metrics["d_recall"]),
        -float(metrics["cd_total"]),
        -float(metrics["severe_error_count"]),
        -float(changed_count),
    )


def make_group_splits(
    indices: np.ndarray,
    y: np.ndarray,
    groups: np.ndarray,
    n_splits: int,
    random_state: int,
) -> list[tuple[np.ndarray, np.ndarray]]:
    local_y = y[indices]
    local_groups = groups[indices]

    unique_groups = np.unique(
        local_groups
    )

    actual_splits = min(
        n_splits,
        len(unique_groups),
    )

    if actual_splits < 2:
        return []

    dummy = np.zeros(
        (len(indices), 1),
        dtype=np.float64,
    )

    if StratifiedGroupKFold is not None:
        splitter = StratifiedGroupKFold(
            n_splits=actual_splits,
            shuffle=True,
            random_state=random_state,
        )

        local_splits = splitter.split(
            dummy,
            local_y,
            local_groups,
        )
    else:
        splitter = GroupKFold(
            n_splits=actual_splits,
        )

        local_splits = splitter.split(
            dummy,
            local_y,
            local_groups,
        )

    output = []

    for local_train, local_valid in local_splits:
        output.append(
            (
                indices[local_train],
                indices[local_valid],
            )
        )

    return output


def fit_r3_gate(
    X: np.ndarray,
    y: np.ndarray,
    base_pred: np.ndarray,
    r2_pred: np.ndarray,
    indices: np.ndarray,
    c_value: float,
) -> dict[str, Any]:
    base_correct = (
        base_pred[indices]
        == y[indices]
    )

    r2_correct = (
        r2_pred[indices]
        == y[indices]
    )

    informative = (
        base_correct
        != r2_correct
    )

    informative_indices = (
        indices[informative]
    )

    if len(informative_indices) < 10:
        return {
            "model": None,
            "constant_probability": 0.0,
        }

    gate_target = (
        r2_pred[informative_indices]
        == y[informative_indices]
    ).astype(int)

    unique_targets = np.unique(
        gate_target
    )

    if len(unique_targets) < 2:
        return {
            "model": None,
            "constant_probability": float(
                unique_targets[0]
            ),
        }

    model = Pipeline(
        [
            (
                "scaler",
                StandardScaler(),
            ),
            (
                "classifier",
                LogisticRegression(
                    C=c_value,
                    class_weight="balanced",
                    max_iter=5000,
                    solver="liblinear",
                    random_state=RANDOM_STATE,
                ),
            ),
        ]
    )

    model.fit(
        X[informative_indices],
        gate_target,
    )

    return {
        "model": model,
        "constant_probability": None,
    }


def predict_r3_gate_probability(
    fitted: dict[str, Any],
    X: np.ndarray,
    indices: np.ndarray,
) -> np.ndarray:
    model = fitted["model"]

    if model is None:
        return np.full(
            len(indices),
            float(
                fitted[
                    "constant_probability"
                ]
            ),
            dtype=np.float64,
        )

    return model.predict_proba(
        X[indices]
    )[:, 1]


def select_r3_parameters(
    X: np.ndarray,
    y: np.ndarray,
    groups: np.ndarray,
    base_pred: np.ndarray,
    r2_pred: np.ndarray,
    train_indices: np.ndarray,
) -> dict[str, Any]:
    candidates = list(
        itertools.product(
            [0.01, 0.1, 1.0, 10.0],
            [0.55, 0.65, 0.75, 0.85],
        )
    )

    splits = make_group_splits(
        train_indices,
        y,
        groups,
        n_splits=3,
        random_state=RANDOM_STATE + 3,
    )

    best = None
    best_rank = None

    for c_value, threshold in candidates:
        predictions = base_pred[
            train_indices
        ].copy()

        for inner_train, inner_valid in splits:
            fitted = fit_r3_gate(
                X,
                y,
                base_pred,
                r2_pred,
                inner_train,
                c_value,
            )

            probability = (
                predict_r3_gate_probability(
                    fitted,
                    X,
                    inner_valid,
                )
            )

            choose_r2 = (
                probability >= threshold
            )

            local_predictions = base_pred[
                inner_valid
            ].copy()

            local_predictions[
                choose_r2
            ] = r2_pred[
                inner_valid
            ][choose_r2]

            positions = np.searchsorted(
                train_indices,
                inner_valid,
            )

            predictions[
                positions
            ] = local_predictions

        metrics = metric_bundle(
            y[train_indices],
            predictions,
        )

        changed = int(
            np.sum(
                predictions
                != base_pred[train_indices]
            )
        )

        rank = metric_rank(
            metrics,
            changed,
        )

        if (
            best_rank is None
            or rank > best_rank
        ):
            best_rank = rank
            best = {
                "C": float(c_value),
                "threshold": float(
                    threshold
                ),
            }

    return best


def predict_r4_des(
    X: np.ndarray,
    y: np.ndarray,
    base_pred: np.ndarray,
    r2_pred: np.ndarray,
    train_indices: np.ndarray,
    test_indices: np.ndarray,
    neighbors: int,
    advantage: float,
) -> np.ndarray:
    scaler = StandardScaler()

    train_x = scaler.fit_transform(
        X[train_indices]
    )

    test_x = scaler.transform(
        X[test_indices]
    )

    actual_neighbors = min(
        neighbors,
        len(train_indices),
    )

    nearest = NearestNeighbors(
        n_neighbors=actual_neighbors,
        metric="euclidean",
    )

    nearest.fit(train_x)

    neighbor_indices = nearest.kneighbors(
        test_x,
        return_distance=False,
    )

    base_correct = (
        base_pred[train_indices]
        == y[train_indices]
    ).astype(np.float64)

    r2_correct = (
        r2_pred[train_indices]
        == y[train_indices]
    ).astype(np.float64)

    local_base_competence = np.mean(
        base_correct[neighbor_indices],
        axis=1,
    )

    local_r2_competence = np.mean(
        r2_correct[neighbor_indices],
        axis=1,
    )

    choose_r2 = (
        local_r2_competence
        >= (
            local_base_competence
            + advantage
        )
    )

    predictions = base_pred[
        test_indices
    ].copy()

    predictions[
        choose_r2
    ] = r2_pred[
        test_indices
    ][choose_r2]

    return predictions


def select_r4_parameters(
    X: np.ndarray,
    y: np.ndarray,
    groups: np.ndarray,
    base_pred: np.ndarray,
    r2_pred: np.ndarray,
    train_indices: np.ndarray,
) -> dict[str, Any]:
    candidates = list(
        itertools.product(
            [15, 25, 40, 60],
            [0.0, 0.05, 0.10, 0.15],
        )
    )

    splits = make_group_splits(
        train_indices,
        y,
        groups,
        n_splits=3,
        random_state=RANDOM_STATE + 4,
    )

    best = None
    best_rank = None

    for neighbors, advantage in candidates:
        predictions_by_index = {}

        for inner_train, inner_valid in splits:
            local_predictions = predict_r4_des(
                X,
                y,
                base_pred,
                r2_pred,
                inner_train,
                inner_valid,
                neighbors,
                advantage,
            )

            for index, prediction in zip(
                inner_valid,
                local_predictions,
            ):
                predictions_by_index[
                    int(index)
                ] = int(prediction)

        predictions = np.asarray(
            [
                predictions_by_index.get(
                    int(index),
                    int(base_pred[index]),
                )
                for index in train_indices
            ],
            dtype=int,
        )

        metrics = metric_bundle(
            y[train_indices],
            predictions,
        )

        changed = int(
            np.sum(
                predictions
                != base_pred[train_indices]
            )
        )

        rank = metric_rank(
            metrics,
            changed,
        )

        if (
            best_rank is None
            or rank > best_rank
        ):
            best_rank = rank
            best = {
                "neighbors": int(
                    neighbors
                ),
                "advantage": float(
                    advantage
                ),
            }

    return best


def fit_r5_stacking(
    X: np.ndarray,
    y: np.ndarray,
    indices: np.ndarray,
    c_value: float,
) -> Pipeline:
    model = Pipeline(
        [
            (
                "scaler",
                StandardScaler(),
            ),
            (
                "classifier",
                LogisticRegression(
                    C=c_value,
                    class_weight="balanced",
                    max_iter=5000,
                    solver="lbfgs",
                    random_state=RANDOM_STATE,
                ),
            ),
        ]
    )

    model.fit(
        X[indices],
        y[indices],
    )

    return model


def select_r5_parameters(
    X: np.ndarray,
    y: np.ndarray,
    groups: np.ndarray,
    train_indices: np.ndarray,
) -> dict[str, Any]:
    candidates = [
        0.01,
        0.1,
        1.0,
        10.0,
    ]

    splits = make_group_splits(
        train_indices,
        y,
        groups,
        n_splits=3,
        random_state=RANDOM_STATE + 5,
    )

    best = None
    best_rank = None

    for c_value in candidates:
        predictions_by_index = {}

        for inner_train, inner_valid in splits:
            model = fit_r5_stacking(
                X,
                y,
                inner_train,
                c_value,
            )

            local_predictions = (
                model.predict(
                    X[inner_valid]
                )
            )

            for index, prediction in zip(
                inner_valid,
                local_predictions,
            ):
                predictions_by_index[
                    int(index)
                ] = int(prediction)

        predictions = np.asarray(
            [
                predictions_by_index.get(
                    int(index),
                    0,
                )
                for index in train_indices
            ],
            dtype=int,
        )

        metrics = metric_bundle(
            y[train_indices],
            predictions,
        )

        rank = metric_rank(
            metrics,
            changed_count=0,
        )

        if (
            best_rank is None
            or rank > best_rank
        ):
            best_rank = rank
            best = {
                "C": float(c_value),
            }

    return best


def predict_r6_selective(
    probabilities: np.ndarray,
    base_pred: np.ndarray,
    r2_pred: np.ndarray,
    specialist_margin: np.ndarray,
    indices: np.ndarray,
    min_specialist_margin: float,
    max_base_cd_margin: float,
) -> tuple[np.ndarray, np.ndarray]:
    local_probs = probabilities[
        indices
    ]

    local_base = base_pred[
        indices
    ]

    local_r2 = r2_pred[
        indices
    ]

    local_specialist_margin = (
        specialist_margin[indices]
    )

    top2_cd = top2_cd_mask(
        local_probs
    )

    base_cd_margin = np.abs(
        local_probs[:, 3]
        - local_probs[:, 2]
    )

    disagreement = (
        local_base != local_r2
    )

    override = (
        disagreement
        & top2_cd
        & (
            local_specialist_margin
            >= min_specialist_margin
        )
        & (
            base_cd_margin
            <= max_base_cd_margin
        )
    )

    review = (
        disagreement
        & top2_cd
        & (~override)
    )

    predictions = local_base.copy()

    predictions[
        override
    ] = local_r2[
        override
    ]

    return predictions, review


def select_r6_parameters(
    probabilities: np.ndarray,
    y: np.ndarray,
    groups: np.ndarray,
    base_pred: np.ndarray,
    r2_pred: np.ndarray,
    specialist_margin: np.ndarray,
    train_indices: np.ndarray,
) -> dict[str, Any]:
    candidates = list(
        itertools.product(
            [
                0.00,
                0.05,
                0.10,
                0.15,
                0.20,
            ],
            [
                0.05,
                0.10,
                0.20,
                0.30,
                1.00,
            ],
        )
    )

    splits = make_group_splits(
        train_indices,
        y,
        groups,
        n_splits=3,
        random_state=RANDOM_STATE + 6,
    )

    best = None
    best_rank = None

    for (
        min_specialist_margin,
        max_base_cd_margin,
    ) in candidates:
        predictions_by_index = {}
        review_by_index = {}

        for _, inner_valid in splits:
            local_predictions, local_review = (
                predict_r6_selective(
                    probabilities,
                    base_pred,
                    r2_pred,
                    specialist_margin,
                    inner_valid,
                    min_specialist_margin,
                    max_base_cd_margin,
                )
            )

            for index, prediction, review in zip(
                inner_valid,
                local_predictions,
                local_review,
            ):
                predictions_by_index[
                    int(index)
                ] = int(prediction)

                review_by_index[
                    int(index)
                ] = bool(review)

        predictions = np.asarray(
            [
                predictions_by_index.get(
                    int(index),
                    int(base_pred[index]),
                )
                for index in train_indices
            ],
            dtype=int,
        )

        review_count = int(
            sum(
                review_by_index.get(
                    int(index),
                    False,
                )
                for index in train_indices
            )
        )

        metrics = metric_bundle(
            y[train_indices],
            predictions,
        )

        changed = int(
            np.sum(
                predictions
                != base_pred[train_indices]
            )
        )

        rank = (
            *metric_rank(
                metrics,
                changed,
            ),
            -float(review_count),
        )

        if (
            best_rank is None
            or rank > best_rank
        ):
            best_rank = rank
            best = {
                "min_specialist_margin": float(
                    min_specialist_margin
                ),
                "max_base_cd_margin": float(
                    max_base_cd_margin
                ),
            }

    return best


def load_oof_data() -> dict[str, Any]:
    path = (
        R2_OOF_DIR
        / "all_outer_predictions.csv"
    )

    if not path.is_file():
        raise FileNotFoundError(
            f"Missing OOF file: {path}"
        )

    df = pd.read_csv(
        path,
        dtype={"case_id": "string"},
    )

    required = {
        "case_id",
        "true_idx",
        "base_pred_idx",
        "specialist_pred_idx",
        "specialist_probability_D",
        "selected_threshold",
        "seed",
        "fold",
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
            f"OOF missing columns: {missing}"
        )

    df["case_id"] = (
        df["case_id"]
        .astype(str)
        .str.replace(
            r"\.0$",
            "",
            regex=True,
        )
    )

    logits = df[
        [
            "logit_A",
            "logit_B",
            "logit_C",
            "logit_D",
        ]
    ].to_numpy(dtype=np.float64)

    probabilities = softmax(logits)

    base_pred = (
        df["base_pred_idx"]
        .astype(int)
        .to_numpy()
    )

    r2_pred = (
        df["specialist_pred_idx"]
        .astype(int)
        .to_numpy()
    )

    specialist_probability_d = (
        df["specialist_probability_D"]
        .astype(float)
        .fillna(0.5)
        .to_numpy()
    )

    selected_threshold = (
        df["selected_threshold"]
        .astype(float)
        .to_numpy()
    )

    specialist_margin = np.abs(
        specialist_probability_d
        - selected_threshold
    )

    X, feature_names = build_meta_features(
        probabilities,
        base_pred,
        r2_pred,
        specialist_probability_d,
        specialist_margin,
    )

    return {
        "df": df,
        "X": X,
        "feature_names": feature_names,
        "probabilities": probabilities,
        "y": (
            df["true_idx"]
            .astype(int)
            .to_numpy()
        ),
        "groups": (
            df["case_id"]
            .astype(str)
            .to_numpy()
        ),
        "base_pred": base_pred,
        "r2_pred": r2_pred,
        "specialist_probability_d": (
            specialist_probability_d
        ),
        "specialist_margin": (
            specialist_margin
        ),
    }


def find_probability_columns(
    df: pd.DataFrame,
) -> list[str]:
    candidate_sets = [
        [
            "flat_prob_A",
            "flat_prob_B",
            "flat_prob_C",
            "flat_prob_D",
        ],
        [
            "prob_A",
            "prob_B",
            "prob_C",
            "prob_D",
        ],
    ]

    for candidates in candidate_sets:
        if all(
            column in df.columns
            for column in candidates
        ):
            return candidates

    raise RuntimeError(
        "Cannot find A/B/C/D probability columns "
        f"in {list(df.columns)}"
    )


def find_column(
    df: pd.DataFrame,
    candidates: list[str],
) -> str:
    for candidate in candidates:
        if candidate in df.columns:
            return candidate

    raise RuntimeError(
        f"Cannot find any column from: {candidates}"
    )


def build_locked_test_r2() -> dict[str, Any]:
    prediction_path = (
        E1_TEST_DIR
        / "test_predictions.csv"
    )

    if not prediction_path.is_file():
        raise FileNotFoundError(
            f"Missing E1 test predictions: "
            f"{prediction_path}"
        )

    df = pd.read_csv(
        prediction_path,
        dtype={"case_id": "string"},
    )

    probability_columns = (
        find_probability_columns(df)
    )

    probabilities = normalize_probabilities(
        df[
            probability_columns
        ].to_numpy(dtype=np.float64)
    )

    logits = np.log(
        np.clip(
            probabilities,
            1e-8,
            1.0,
        )
    )

    true_column = find_column(
        df,
        [
            "true_index",
            "true_idx",
        ],
    )

    pred_column = find_column(
        df,
        [
            "pred_index",
            "base_pred_idx",
        ],
    )

    y = (
        df[true_column]
        .astype(int)
        .to_numpy()
    )

    base_pred = (
        df[pred_column]
        .astype(int)
        .to_numpy()
    )

    gate = top2_cd_mask(
        probabilities
    )

    specialist_input = (
        specialist_features(logits)
    )

    all_predictions = []
    all_probability_d = []
    all_margins = []
    policy_rows = []

    summaries = sorted(
        R2_OOF_DIR.glob(
            "fold_runs/seed*_fold*/"
            "fold_summary.json"
        )
    )

    if len(summaries) != 15:
        raise RuntimeError(
            "Expected 15 specialist summaries, "
            f"found {len(summaries)}"
        )

    for summary_path in summaries:
        run_dir = summary_path.parent

        model_path = (
            run_dir
            / "cd_specialist.joblib"
        )

        summary = json.loads(
            summary_path.read_text(
                encoding="utf-8"
            )
        )

        model = joblib.load(
            model_path
        )

        threshold = float(
            summary[
                "selected_parameters"
            ]["threshold"]
        )

        probability_d = (
            model.predict_proba(
                specialist_input
            )[:, 1]
        )

        local_pred = base_pred.copy()

        local_pred[gate] = np.where(
            probability_d[gate]
            >= threshold,
            3,
            2,
        )

        all_predictions.append(
            local_pred
        )

        all_probability_d.append(
            probability_d
        )

        all_margins.append(
            np.abs(
                probability_d
                - threshold
            )
        )

        policy_rows.append({
            "run": run_dir.name,
            "threshold": threshold,
            "C": summary[
                "selected_parameters"
            ]["C"],
            "class_weight": str(
                summary[
                    "selected_parameters"
                ]["class_weight"]
            ),
        })

    vote_matrix = np.stack(
        all_predictions,
        axis=1,
    )

    r2_pred = []

    for row_index, row in enumerate(
        vote_matrix
    ):
        counts = np.bincount(
            row,
            minlength=4,
        )

        winners = np.flatnonzero(
            counts == counts.max()
        )

        if len(winners) == 1:
            prediction = int(
                winners[0]
            )
        else:
            prediction = int(
                base_pred[row_index]
            )

        r2_pred.append(prediction)

    r2_pred = np.asarray(
        r2_pred,
        dtype=int,
    )

    specialist_probability_d = np.mean(
        np.stack(
            all_probability_d,
            axis=1,
        ),
        axis=1,
    )

    specialist_margin = np.mean(
        np.stack(
            all_margins,
            axis=1,
        ),
        axis=1,
    )

    X, feature_names = build_meta_features(
        probabilities,
        base_pred,
        r2_pred,
        specialist_probability_d,
        specialist_margin,
    )

    pd.DataFrame(
        policy_rows
    ).to_csv(
        OUT / "locked_test_r2_policies.csv",
        index=False,
    )

    return {
        "df": df,
        "X": X,
        "feature_names": feature_names,
        "probabilities": probabilities,
        "y": y,
        "base_pred": base_pred,
        "r2_pred": r2_pred,
        "specialist_probability_d": (
            specialist_probability_d
        ),
        "specialist_margin": (
            specialist_margin
        ),
        "vote_matrix": vote_matrix,
    }


def run_meta_oof(
    data: dict[str, Any],
) -> dict[str, Any]:
    X = data["X"]
    y = data["y"]
    groups = data["groups"]
    probabilities = data[
        "probabilities"
    ]
    base_pred = data["base_pred"]
    r2_pred = data["r2_pred"]
    specialist_margin = data[
        "specialist_margin"
    ]

    all_indices = np.arange(
        len(y),
        dtype=int,
    )

    outer_splits = make_group_splits(
        all_indices,
        y,
        groups,
        n_splits=5,
        random_state=RANDOM_STATE,
    )

    predictions = {
        "R3_MoE": np.full(
            len(y),
            -1,
            dtype=int,
        ),
        "R4_DES": np.full(
            len(y),
            -1,
            dtype=int,
        ),
        "R5_Stacking": np.full(
            len(y),
            -1,
            dtype=int,
        ),
        "R6_Selective": np.full(
            len(y),
            -1,
            dtype=int,
        ),
    }

    r6_review = np.zeros(
        len(y),
        dtype=bool,
    )

    fold_rows = []

    for outer_fold, (
        train_indices,
        valid_indices,
    ) in enumerate(outer_splits):
        print()
        print("=" * 72)
        print(
            f"META OUTER FOLD {outer_fold}"
        )
        print("=" * 72)

        r3_params = select_r3_parameters(
            X,
            y,
            groups,
            base_pred,
            r2_pred,
            train_indices,
        )

        r3_model = fit_r3_gate(
            X,
            y,
            base_pred,
            r2_pred,
            train_indices,
            r3_params["C"],
        )

        r3_probability = (
            predict_r3_gate_probability(
                r3_model,
                X,
                valid_indices,
            )
        )

        r3_choose = (
            r3_probability
            >= r3_params["threshold"]
        )

        r3_pred = base_pred[
            valid_indices
        ].copy()

        r3_pred[
            r3_choose
        ] = r2_pred[
            valid_indices
        ][r3_choose]

        predictions[
            "R3_MoE"
        ][valid_indices] = r3_pred

        r4_params = select_r4_parameters(
            X,
            y,
            groups,
            base_pred,
            r2_pred,
            train_indices,
        )

        r4_pred = predict_r4_des(
            X,
            y,
            base_pred,
            r2_pred,
            train_indices,
            valid_indices,
            r4_params["neighbors"],
            r4_params["advantage"],
        )

        predictions[
            "R4_DES"
        ][valid_indices] = r4_pred

        r5_params = select_r5_parameters(
            X,
            y,
            groups,
            train_indices,
        )

        r5_model = fit_r5_stacking(
            X,
            y,
            train_indices,
            r5_params["C"],
        )

        r5_pred = r5_model.predict(
            X[valid_indices]
        ).astype(int)

        predictions[
            "R5_Stacking"
        ][valid_indices] = r5_pred

        r6_params = select_r6_parameters(
            probabilities,
            y,
            groups,
            base_pred,
            r2_pred,
            specialist_margin,
            train_indices,
        )

        r6_pred, local_review = (
            predict_r6_selective(
                probabilities,
                base_pred,
                r2_pred,
                specialist_margin,
                valid_indices,
                r6_params[
                    "min_specialist_margin"
                ],
                r6_params[
                    "max_base_cd_margin"
                ],
            )
        )

        predictions[
            "R6_Selective"
        ][valid_indices] = r6_pred

        r6_review[
            valid_indices
        ] = local_review

        for method_name, method_pred in [
            ("R3_MoE", r3_pred),
            ("R4_DES", r4_pred),
            ("R5_Stacking", r5_pred),
            ("R6_Selective", r6_pred),
        ]:
            metrics = metric_bundle(
                y[valid_indices],
                method_pred,
            )

            print(
                f"{method_name:<15} "
                f"Macro-F1="
                f"{metrics['macro_f1']:.6f} "
                f"D-recall="
                f"{metrics['d_recall']:.6f} "
                f"CD-errors="
                f"{metrics['cd_total']}"
            )

        fold_rows.append({
            "outer_fold": outer_fold,
            "train_rows": int(
                len(train_indices)
            ),
            "valid_rows": int(
                len(valid_indices)
            ),
            "R3_parameters": r3_params,
            "R4_parameters": r4_params,
            "R5_parameters": r5_params,
            "R6_parameters": r6_params,
        })

    for method_name, values in predictions.items():
        if np.any(values < 0):
            raise RuntimeError(
                f"Incomplete OOF predictions: "
                f"{method_name}"
            )

    metrics = {
        "BASE_OOF": metric_bundle(
            y,
            base_pred,
        ),
        "R2_OOF": metric_bundle(
            y,
            r2_pred,
        ),
    }

    for method_name, values in predictions.items():
        metrics[method_name] = (
            metric_bundle(
                y,
                values,
            )
        )

    prediction_df = data["df"].copy()

    for method_name, values in predictions.items():
        prediction_df[
            f"{method_name}_pred_idx"
        ] = values

        prediction_df[
            f"{method_name}_pred_label"
        ] = [
            LABELS[index]
            for index in values
        ]

    prediction_df[
        "R6_review_flag"
    ] = r6_review.astype(int)

    prediction_df.to_csv(
        OUT / "meta_oof_predictions.csv",
        index=False,
    )

    pd.DataFrame(
        fold_rows
    ).to_json(
        OUT / "meta_oof_fold_parameters.json",
        orient="records",
        indent=2,
    )

    return {
        "predictions": predictions,
        "r6_review": r6_review,
        "metrics": metrics,
        "fold_rows": fold_rows,
    }


def select_final_parameters(
    data: dict[str, Any],
) -> dict[str, Any]:
    X = data["X"]
    y = data["y"]
    groups = data["groups"]
    probabilities = data[
        "probabilities"
    ]
    base_pred = data["base_pred"]
    r2_pred = data["r2_pred"]
    specialist_margin = data[
        "specialist_margin"
    ]

    indices = np.arange(
        len(y),
        dtype=int,
    )

    return {
        "R3_MoE": select_r3_parameters(
            X,
            y,
            groups,
            base_pred,
            r2_pred,
            indices,
        ),
        "R4_DES": select_r4_parameters(
            X,
            y,
            groups,
            base_pred,
            r2_pred,
            indices,
        ),
        "R5_Stacking": select_r5_parameters(
            X,
            y,
            groups,
            indices,
        ),
        "R6_Selective": select_r6_parameters(
            probabilities,
            y,
            groups,
            base_pred,
            r2_pred,
            specialist_margin,
            indices,
        ),
    }


def run_locked_test(
    oof_data: dict[str, Any],
    test_data: dict[str, Any],
    final_parameters: dict[str, Any],
) -> dict[str, Any]:
    train_indices = np.arange(
        len(oof_data["y"]),
        dtype=int,
    )

    test_indices = np.arange(
        len(test_data["y"]),
        dtype=int,
    )

    X_train = oof_data["X"]
    X_test = test_data["X"]

    y_train = oof_data["y"]
    y_test = test_data["y"]

    base_train = oof_data[
        "base_pred"
    ]

    r2_train = oof_data[
        "r2_pred"
    ]

    base_test = test_data[
        "base_pred"
    ]

    r2_test = test_data[
        "r2_pred"
    ]

    r3_params = final_parameters[
        "R3_MoE"
    ]

    r3_model = fit_r3_gate(
        X_train,
        y_train,
        base_train,
        r2_train,
        train_indices,
        r3_params["C"],
    )

    r3_probability = (
        predict_r3_gate_probability(
            r3_model,
            X_test,
            test_indices,
        )
    )

    r3_choose = (
        r3_probability
        >= r3_params["threshold"]
    )

    r3_test = base_test.copy()

    r3_test[
        r3_choose
    ] = r2_test[
        r3_choose
    ]

    r4_params = final_parameters[
        "R4_DES"
    ]

    combined_x = np.vstack(
        [
            X_train,
            X_test,
        ]
    )

    combined_y = np.concatenate(
        [
            y_train,
            np.full(
                len(y_test),
                -1,
                dtype=int,
            ),
        ]
    )

    combined_base = np.concatenate(
        [
            base_train,
            base_test,
        ]
    )

    combined_r2 = np.concatenate(
        [
            r2_train,
            r2_test,
        ]
    )

    combined_train_indices = np.arange(
        len(y_train),
        dtype=int,
    )

    combined_test_indices = np.arange(
        len(y_train),
        len(y_train) + len(y_test),
        dtype=int,
    )

    r4_test = predict_r4_des(
        combined_x,
        combined_y,
        combined_base,
        combined_r2,
        combined_train_indices,
        combined_test_indices,
        r4_params["neighbors"],
        r4_params["advantage"],
    )

    r5_params = final_parameters[
        "R5_Stacking"
    ]

    r5_model = fit_r5_stacking(
        X_train,
        y_train,
        train_indices,
        r5_params["C"],
    )

    r5_test = r5_model.predict(
        X_test
    ).astype(int)

    r6_params = final_parameters[
        "R6_Selective"
    ]

    r6_test, r6_review = (
        predict_r6_selective(
            test_data[
                "probabilities"
            ],
            base_test,
            r2_test,
            test_data[
                "specialist_margin"
            ],
            test_indices,
            r6_params[
                "min_specialist_margin"
            ],
            r6_params[
                "max_base_cd_margin"
            ],
        )
    )

    joblib.dump(
        r3_model,
        OUT / "R3_final_gate.joblib",
    )

    joblib.dump(
        r5_model,
        OUT / "R5_final_stacking.joblib",
    )

    predictions = {
        "E1": base_test,
        "R2": r2_test,
        "R3_MoE": r3_test,
        "R4_DES": r4_test,
        "R5_Stacking": r5_test,
        "R6_Selective": r6_test,
    }

    metrics = {
        method_name: metric_bundle(
            y_test,
            values,
        )
        for method_name, values
        in predictions.items()
    }

    output_df = test_data[
        "df"
    ].copy()

    output_df[
        "R2_pred_index"
    ] = r2_test

    output_df[
        "R2_pred_label"
    ] = [
        LABELS[index]
        for index in r2_test
    ]

    output_df[
        "R3_gate_probability"
    ] = r3_probability

    output_df[
        "R3_used_R2"
    ] = r3_choose.astype(int)

    for method_name in [
        "R3_MoE",
        "R4_DES",
        "R5_Stacking",
        "R6_Selective",
    ]:
        values = predictions[
            method_name
        ]

        output_df[
            f"{method_name}_pred_index"
        ] = values

        output_df[
            f"{method_name}_pred_label"
        ] = [
            LABELS[index]
            for index in values
        ]

        output_df[
            f"{method_name}_changed_from_E1"
        ] = (
            values != base_test
        ).astype(int)

    output_df[
        "R6_review_flag"
    ] = r6_review.astype(int)

    output_df.to_csv(
        OUT / "locked_test_predictions_R3_R6.csv",
        index=False,
    )

    accepted = ~r6_review

    r6_selective_accuracy = (
        float(
            accuracy_score(
                y_test[accepted],
                r6_test[accepted],
            )
        )
        if accepted.any()
        else None
    )

    return {
        "predictions": predictions,
        "metrics": metrics,
        "R3_gate_probability": (
            r3_probability
        ),
        "R3_used_R2_count": int(
            r3_choose.sum()
        ),
        "R6_review_count": int(
            r6_review.sum()
        ),
        "R6_coverage": float(
            accepted.mean()
        ),
        "R6_selective_accuracy": (
            r6_selective_accuracy
        ),
    }


def metrics_to_table(
    metrics: dict[str, dict[str, Any]],
    baseline_name: str,
) -> pd.DataFrame:
    baseline = metrics[
        baseline_name
    ]

    rows = []

    for method_name, values in metrics.items():
        rows.append({
            "method": method_name,
            "num_samples": values[
                "num_samples"
            ],
            "accuracy": values[
                "accuracy"
            ],
            "balanced_accuracy": values[
                "balanced_accuracy"
            ],
            "macro_f1": values[
                "macro_f1"
            ],
            "weighted_f1": values[
                "weighted_f1"
            ],
            "qwk": values["qwk"],
            "d_recall": values[
                "d_recall"
            ],
            "c_to_d": values[
                "c_to_d"
            ],
            "d_to_c": values[
                "d_to_c"
            ],
            "cd_total": values[
                "cd_total"
            ],
            "severe_error_count": values[
                "severe_error_count"
            ],
            "within_one": values[
                "within_one"
            ],
            "delta_macro_f1_vs_baseline": (
                values["macro_f1"]
                - baseline["macro_f1"]
            ),
            "delta_d_recall_vs_baseline": (
                values["d_recall"]
                - baseline["d_recall"]
            ),
            "delta_cd_errors_vs_baseline": (
                values["cd_total"]
                - baseline["cd_total"]
            ),
        })

    return pd.DataFrame(rows)


def save_plots(
    test_table: pd.DataFrame,
) -> None:
    methods = test_table[
        "method"
    ].tolist()

    for column, title, filename in [
        (
            "macro_f1",
            "Locked Test Macro-F1",
            "locked_test_macro_f1.png",
        ),
        (
            "d_recall",
            "Locked Test Class-D Recall",
            "locked_test_d_recall.png",
        ),
        (
            "cd_total",
            "Locked Test C↔D Errors",
            "locked_test_cd_errors.png",
        ),
    ]:
        values = test_table[
            column
        ].to_numpy()

        fig, ax = plt.subplots(
            figsize=(10, 6)
        )

        bars = ax.bar(
            methods,
            values,
        )

        ax.set_title(
            title,
            fontweight="bold",
        )

        ax.tick_params(
            axis="x",
            rotation=25,
        )

        if column != "cd_total":
            ax.set_ylim(0, 1)

        for bar, value in zip(
            bars,
            values,
        ):
            label = (
                f"{value:.3f}"
                if column != "cd_total"
                else f"{int(value)}"
            )

            ax.text(
                bar.get_x()
                + bar.get_width() / 2,
                bar.get_height()
                + (
                    0.015
                    if column != "cd_total"
                    else 0.3
                ),
                label,
                ha="center",
                va="bottom",
                fontsize=9,
            )

        fig.tight_layout()

        fig.savefig(
            OUT / filename,
            dpi=180,
            bbox_inches="tight",
        )

        plt.close(fig)


def print_comparison(
    title: str,
    table: pd.DataFrame,
) -> None:
    print()
    print("=" * 116)
    print(f" {title}")
    print("=" * 116)

    print(
        f"{'Method':<16}"
        f"{'Macro-F1':>12}"
        f"{'Accuracy':>12}"
        f"{'Bal Acc':>12}"
        f"{'D Recall':>12}"
        f"{'C↔D':>8}"
        f"{'Severe':>9}"
        f"{'ΔF1':>12}"
    )

    print("-" * 116)

    for _, row in table.iterrows():
        print(
            f"{row['method']:<16}"
            f"{row['macro_f1']:>12.6f}"
            f"{row['accuracy']:>12.6f}"
            f"{row['balanced_accuracy']:>12.6f}"
            f"{row['d_recall']:>12.6f}"
            f"{int(row['cd_total']):>8}"
            f"{int(row['severe_error_count']):>9}"
            f"{row['delta_macro_f1_vs_baseline']:>+12.6f}"
        )


def main() -> None:
    print("=" * 72)
    print(" R3-R6 ENSEMBLE MANAGEMENT")
    print(" R3 = MIXTURE OF EXPERTS")
    print(" R4 = DYNAMIC ENSEMBLE SELECTION")
    print(" R5 = STACKING")
    print(" R6 = SELECTIVE CLASSIFICATION")
    print(" CPU ONLY — NO CNN INFERENCE")
    print(" LOCKED TEST RESULT = EXPLORATORY")
    print("=" * 72)

    oof_data = load_oof_data()

    print(
        f"OOF_ROWS={len(oof_data['y'])}"
    )

    print(
        "OOF_UNIQUE_CASES="
        f"{len(np.unique(oof_data['groups']))}"
    )

    meta_oof = run_meta_oof(
        oof_data
    )

    oof_table = metrics_to_table(
        meta_oof["metrics"],
        baseline_name="BASE_OOF",
    )

    oof_table.to_csv(
        OUT / "oof_comparison_R3_R6.csv",
        index=False,
    )

    final_parameters = (
        select_final_parameters(
            oof_data
        )
    )

    (
        OUT / "final_parameters.json"
    ).write_text(
        json.dumps(
            final_parameters,
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    test_data = build_locked_test_r2()

    print(
        f"LOCKED_TEST_ROWS="
        f"{len(test_data['y'])}"
    )

    test_result = run_locked_test(
        oof_data,
        test_data,
        final_parameters,
    )

    test_table = metrics_to_table(
        test_result["metrics"],
        baseline_name="E1",
    )

    test_table.to_csv(
        OUT / "locked_test_comparison_R3_R6.csv",
        index=False,
    )

    save_plots(
        test_table
    )

    report = {
        "status": (
            "EXPLORATORY_LOCKED_TEST"
        ),
        "warning": (
            "R3-R6 were designed after earlier "
            "locked-test inspection. Results must "
            "not replace the official E1 result."
        ),
        "protocol": {
            "meta_development": (
                "Group-aware cross-validation on "
                "existing strict OOF predictions."
            ),
            "grouping": (
                "All repeated seed predictions for "
                "the same case_id remain in the "
                "same meta fold."
            ),
            "locked_test_tuning": False,
            "cnn_inference": False,
        },
        "feature_names": oof_data[
            "feature_names"
        ],
        "final_parameters": (
            final_parameters
        ),
        "oof_metrics": (
            meta_oof["metrics"]
        ),
        "locked_test_metrics": (
            test_result["metrics"]
        ),
        "R3_used_R2_count": (
            test_result[
                "R3_used_R2_count"
            ]
        ),
        "R6_review_count": (
            test_result[
                "R6_review_count"
            ]
        ),
        "R6_coverage": (
            test_result[
                "R6_coverage"
            ]
        ),
        "R6_selective_accuracy": (
            test_result[
                "R6_selective_accuracy"
            ]
        ),
    }

    (
        OUT / "final_report_R3_R6.json"
    ).write_text(
        json.dumps(
            report,
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    print_comparison(
        "STRICT META-OOF COMPARISON",
        oof_table,
    )

    print_comparison(
        "EXPLORATORY LOCKED TEST 132",
        test_table,
    )

    best_row = test_table.sort_values(
        [
            "macro_f1",
            "balanced_accuracy",
            "d_recall",
        ],
        ascending=[
            False,
            False,
            False,
        ],
    ).iloc[0]

    print()
    print("=" * 72)
    print(" FINAL EXPLORATORY RESULT")
    print("=" * 72)

    print(
        f"BEST_TEST_METHOD="
        f"{best_row['method']}"
    )

    print(
        f"BEST_TEST_MACRO_F1="
        f"{best_row['macro_f1']:.6f}"
    )

    print(
        f"E1_MACRO_F1="
        f"{test_result['metrics']['E1']['macro_f1']:.6f}"
    )

    print(
        "BEST_DELTA_VS_E1="
        f"{best_row['delta_macro_f1_vs_baseline']:+.6f}"
    )

    print(
        "R3_USED_R2_COUNT="
        f"{test_result['R3_used_R2_count']}"
    )

    print(
        "R6_REVIEW_COUNT="
        f"{test_result['R6_review_count']}"
    )

    print(
        "R6_COVERAGE="
        f"{test_result['R6_coverage']:.6f}"
    )

    if (
        test_result[
            "R6_selective_accuracy"
        ] is not None
    ):
        print(
            "R6_SELECTIVE_ACCURACY="
            f"{test_result['R6_selective_accuracy']:.6f}"
        )

    print(
        "OFFICIAL_MODEL_REMAINS=E1"
    )

    print(
        "LOCKED_TEST_STATUS="
        "EXPLORATORY_ONLY"
    )

    print(
        f"OUTPUT_DIR={OUT}"
    )

    (
        OUT / "PIPELINE_DONE.txt"
    ).write_text(
        "R3-R6 ensemble-management pipeline completed.\n"
        "No CNN inference was performed.\n"
        "Locked-test comparison is exploratory only.\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    try:
        main()
    except Exception:
        failure = traceback.format_exc()

        (
            OUT / "PIPELINE_FAILED.txt"
        ).write_text(
            failure,
            encoding="utf-8",
        )

        print()
        print("=" * 72)
        print(" PIPELINE FAILED")
        print("=" * 72)
        print(failure)
