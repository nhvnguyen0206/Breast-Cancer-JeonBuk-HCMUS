from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

import torch
from coral_pytorch.losses import coral_loss
from torch import nn
from torch.nn import functional as F

from tn_mammo.data.contracts import (
    make_binary_targets,
    make_ordinal_targets,
)
from tn_mammo.constants import (
    NUM_CLASSES,
)


def compute_class_balanced_weights(
    class_counts: list[int] | tuple[int, ...],
    *,
    beta: float,
) -> torch.Tensor:
    counts = torch.tensor(
        class_counts,
        dtype=torch.float64,
    )

    if torch.any(counts <= 0):
        raise ValueError(
            "Class counts must be positive."
        )

    if not 0.0 <= beta < 1.0:
        raise ValueError(
            "beta must lie in [0, 1)."
        )

    effective_number = (
        1.0 - torch.pow(beta, counts)
    )

    weights = (
        (1.0 - beta)
        / effective_number
    )

    weights = (
        weights
        / weights.sum()
        * len(class_counts)
    )

    return weights.to(torch.float32)


class ClassBalancedFocalLoss(nn.Module):
    def __init__(
        self,
        class_counts: list[int] | tuple[int, ...],
        *,
        beta: float = 0.99,
        gamma: float = 2.0,
        use_hard_mining: bool = False,
    ) -> None:
        super().__init__()

        self.gamma = float(gamma)
        self.use_hard_mining = use_hard_mining

        weights = (
            compute_class_balanced_weights(
                class_counts,
                beta=beta,
            )
        )

        self.register_buffer(
            "class_weights",
            weights,
        )

    def forward(
        self,
        logits: torch.Tensor,
        targets: torch.Tensor,
    ) -> torch.Tensor:
        ce = F.cross_entropy(
            logits,
            targets,
            weight=self.class_weights,
            reduction="none",
        )

        probabilities = torch.softmax(
            logits,
            dim=1,
        )

        pt = probabilities.gather(
            1,
            targets.unsqueeze(1),
        ).squeeze(1)

        focal_factor = torch.pow(
            1.0 - pt,
            self.gamma,
        )

        losses = focal_factor * ce

        if self.use_hard_mining:
            preds = torch.argmax(logits, dim=1)
            # Find confused C/D (C=2, D=3)
            is_c_pred_d = (targets == 2) & (preds == 3)
            is_d_pred_c = (targets == 3) & (preds == 2)
            hard_mask = is_c_pred_d | is_d_pred_c
            # Upweight them by 3x
            losses[hard_mask] = losses[hard_mask] * 3.0

        return losses.mean()


@dataclass(frozen=True)
class MultiTaskLossOptions:
    lambda_ordinal: float = 0.0
    lambda_binary: float = 0.0
    lambda_neighbor_penalty: float = 0.0
    use_hard_mining: bool = False
    lambda_cd: float = 0.0
    cd_class_counts: list[int] | None = None


class MultiTaskCriterion(nn.Module):
    def __init__(
        self,
        *,
        flat_class_counts: list[int],
        binary_class_counts: list[int],
        beta: float,
        gamma: float,
        options: MultiTaskLossOptions,
    ) -> None:
        super().__init__()

        self.options = options

        self.flat_loss = (
            ClassBalancedFocalLoss(
                flat_class_counts,
                beta=beta,
                gamma=gamma,
                use_hard_mining=options.use_hard_mining,
            )
        )

        binary_weights = (
            compute_class_balanced_weights(
                binary_class_counts,
                beta=beta,
            )
        )

        self.register_buffer(
            "binary_weights",
            binary_weights,
        )

        # CD auxiliary loss (C-vs-D)
        if (
            options.lambda_cd > 0
            and options.cd_class_counts is not None
        ):
            self.cd_loss: ClassBalancedFocalLoss | None = (
                ClassBalancedFocalLoss(
                    options.cd_class_counts,
                    beta=beta,
                    gamma=gamma,
                )
            )
        else:
            self.cd_loss = None

        # Neighbor Ordinal Penalty: penalize C↔D and B↔C harder
        # Cost matrix: cost[i][j] = extra penalty for predicting j when true is i
        # Higher penalty for adjacent-class confusion that is clinically significant
        cost_matrix = torch.zeros(
            (NUM_CLASSES, NUM_CLASSES),
            dtype=torch.float32,
        )
        # C(2) predicted as D(3) or D(3) predicted as C(2): high penalty
        cost_matrix[2, 3] = 3.0  # True=C, Pred=D
        cost_matrix[3, 2] = 3.0  # True=D, Pred=C
        # B(1) predicted as C(2) or C(2) predicted as B(1): moderate penalty
        cost_matrix[1, 2] = 1.5  # True=B, Pred=C
        cost_matrix[2, 1] = 1.5  # True=C, Pred=B
        # A(0) predicted as B(1): light penalty
        cost_matrix[0, 1] = 1.0
        cost_matrix[1, 0] = 1.0
        # Severe: A↔D, A↔C, B↔D
        cost_matrix[0, 3] = 5.0
        cost_matrix[3, 0] = 5.0
        cost_matrix[0, 2] = 3.0
        cost_matrix[2, 0] = 3.0
        cost_matrix[1, 3] = 2.5
        cost_matrix[3, 1] = 2.5
        self.register_buffer(
            "cost_matrix",
            cost_matrix,
        )

    def forward(
        self,
        outputs: Mapping[
            str,
            torch.Tensor | None
        ],
        labels: torch.Tensor,
    ) -> tuple[
        torch.Tensor,
        dict[str, torch.Tensor],
    ]:
        flat_logits = outputs.get(
            "flat_logits"
        )

        if flat_logits is None:
            raise ValueError(
                "flat_logits are required."
            )

        flat = self.flat_loss(
            flat_logits,
            labels,
        )

        total = flat

        parts: dict[str, torch.Tensor] = {
            "flat": flat.detach(),
        }

        if self.options.lambda_ordinal > 0:
            ordinal_logits = outputs.get(
                "ordinal_logits"
            )

            if ordinal_logits is None:
                raise ValueError(
                    "Ordinal loss enabled but "
                    "ordinal_logits are missing."
                )

            levels = make_ordinal_targets(
                labels
            )

            ordinal = coral_loss(
                ordinal_logits,
                levels,
            )

            total = (
                total
                + self.options.lambda_ordinal
                * ordinal
            )

            parts["ordinal"] = (
                ordinal.detach()
            )

        if self.options.lambda_binary > 0:
            binary_logits = outputs.get(
                "binary_logits"
            )

            if binary_logits is None:
                raise ValueError(
                    "Binary loss enabled but "
                    "binary_logits are missing."
                )

            binary_targets = (
                make_binary_targets(labels)
            )

            binary = F.cross_entropy(
                binary_logits,
                binary_targets,
                weight=self.binary_weights,
            )

            total = (
                total
                + self.options.lambda_binary
                * binary
            )

            parts["binary"] = binary.detach()

        if self.options.lambda_neighbor_penalty > 0:
            # Soft neighbor penalty using predicted probabilities
            flat_logits_for_penalty = outputs.get(
                "flat_logits"
            )
            probs = torch.softmax(
                flat_logits_for_penalty.float(),
                dim=1,
            )
            # For each sample, compute expected penalty:
            # penalty_i = sum_j probs[i,j] * cost_matrix[labels[i], j]
            batch_costs = self.cost_matrix[
                labels
            ]  # [B, NUM_CLASSES]
            neighbor_penalty = (
                (probs * batch_costs).sum(dim=1)
            ).mean()

            total = (
                total
                + self.options.lambda_neighbor_penalty
                * neighbor_penalty
            )

            parts["neighbor_penalty"] = (
                neighbor_penalty.detach()
            )

        if self.options.lambda_cd > 0:
            cd_logits = outputs.get(
                "cd_logits"
            )

            if cd_logits is None:
                raise ValueError(
                    "CD loss enabled but "
                    "cd_logits are missing."
                )

            # Only compute on C(2) and D(3) samples
            mask = (labels == 2) | (labels == 3)

            if bool(mask.any()):
                cd_targets = labels[mask] - 2
                cd = self.cd_loss(
                    cd_logits[mask],
                    cd_targets,
                )
            else:
                cd = cd_logits.sum() * 0.0

            total = (
                total
                + self.options.lambda_cd
                * cd
            )

            parts["cd"] = cd.detach()

        parts["total"] = total.detach()

        return total, parts
