import math

import torch
from torch import nn
from torch.nn import functional as F


def class_weights(counts, beta):
    counts = torch.as_tensor(counts, dtype=torch.float64)
    if (counts <= 0).any() or not 0 <= beta < 1:
        raise ValueError("All four training classes must be present; beta must be in [0,1)")
    weights = (1 - beta) / (1 - beta ** counts)
    return (weights / weights.mean()).float()


class MultiTaskLoss(nn.Module):
    def __init__(self, counts, beta=0.999, gamma=2.0, ordinal=0.5, binary=0.3, neighbor=0.2,
                 focal_normalization="class_mean", label_smoothing=0.0, focal_scale=1.0,
                 binary_normalization="batch_weight_mean", view_auxiliary=0.0):
        super().__init__()
        self.gamma, self.ordinal, self.binary, self.neighbor = gamma, ordinal, binary, neighbor
        self.view_auxiliary = float(view_auxiliary)
        if not math.isfinite(self.view_auxiliary) or self.view_auxiliary < 0:
            raise ValueError("view_auxiliary must be finite and non-negative")
        self.focal_scale = float(focal_scale)
        if not math.isfinite(self.focal_scale) or self.focal_scale <= 0:
            raise ValueError("focal_scale must be finite and positive")
        if not 0 <= label_smoothing < 1:
            raise ValueError("label_smoothing must be in [0,1)")
        self.label_smoothing = float(label_smoothing)
        self.register_buffer("weights", class_weights(counts, beta))
        if focal_normalization not in {"class_mean", "train_expectation"}:
            raise ValueError("Unknown focal_normalization")
        # Fixed FIT-only denominator, not the noisy composition of a batch of two.
        # Preserves relative class weights and does not use DEV frequencies.
        frequencies = torch.as_tensor(counts, dtype=torch.float32)
        frequencies = frequencies / frequencies.sum()
        self.focal_denominator = (float((self.weights * frequencies).sum())
                                  if focal_normalization == "train_expectation" else 1.0)
        self.register_buffer("binary_weights", class_weights([sum(counts[:2]), sum(counts[2:])], beta))
        if binary_normalization not in {"batch_weight_mean", "train_expectation"}:
            raise ValueError("Unknown binary_normalization")
        self.binary_normalization = binary_normalization
        binary_frequencies = torch.stack((frequencies[:2].sum(), frequencies[2:].sum()))
        self.binary_denominator = float((self.binary_weights * binary_frequencies).sum())
        self.register_buffer("cost", torch.tensor([
            [0., 1., 3., 5.], [1., 0., 1.5, 2.5],
            [3., 1.5, 0., 3.], [5., 2.5, 3., 0.],
        ]))

    def forward(self, outputs, labels):
        logits = outputs["flat_logits"].float()
        probs = logits.softmax(dim=1)
        pt = probs.gather(1, labels[:, None]).squeeze(1)
        if self.label_smoothing:
            # Apply the effective-number weight of the observed class only.
            # Passing both weight= and label_smoothing= to cross_entropy would
            # leak the very large rare-class weight into every smoothed target.
            cross_entropy = F.cross_entropy(
                logits, labels, reduction="none", label_smoothing=self.label_smoothing
            ) * self.weights[labels]
        else:
            # Preserve the exact established objective for every existing arm.
            cross_entropy = F.cross_entropy(logits, labels, weight=self.weights, reduction="none")
        focal = (self.focal_scale * ((1 - pt) ** self.gamma * cross_entropy).mean()
                 / self.focal_denominator)
        levels = (labels[:, None] > torch.arange(3, device=labels.device)).float()
        # Sum threshold losses per case, then average cases (CORAL reduction).
        ordinal = F.binary_cross_entropy_with_logits(
            outputs["ordinal_logits"].float(), levels, reduction="none").sum(1).mean()
        if self.binary_normalization == "train_expectation":
            # Fixed FIT-only scale preserves weights even in homogeneous batches.
            binary = F.cross_entropy(
                outputs["binary_logits"].float(), (labels >= 2).long(),
                weight=self.binary_weights, reduction="none").mean() / self.binary_denominator
        else:
            binary = F.cross_entropy(outputs["binary_logits"].float(), (labels >= 2).long(),
                                     weight=self.binary_weights)
        neighbor = (probs * self.cost[labels]).sum(1).mean()
        total = focal + self.ordinal * ordinal + self.binary * binary + self.neighbor * neighbor
        parts = {"focal": focal.detach(), "ordinal": ordinal.detach(),
                 "binary": binary.detach(), "neighbor": neighbor.detach()}
        if self.view_auxiliary:
            if "view_logits" not in outputs:
                raise ValueError("view_logits are required when view_auxiliary is enabled")
            view_logits = outputs["view_logits"].float()
            if view_logits.ndim != 3 or view_logits.shape[0] != labels.shape[0] \
                    or view_logits.shape[1:] != (4, 4):
                raise ValueError("view_logits must have shape [B,4,4]")
            view_labels = labels[:, None].expand(-1, 4).reshape(-1)
            view_logits = view_logits.reshape(-1, 4)
            view_probabilities = view_logits.softmax(dim=1)
            view_pt = view_probabilities.gather(1, view_labels[:, None]).squeeze(1)
            if self.label_smoothing:
                view_cross_entropy = F.cross_entropy(
                    view_logits, view_labels, reduction="none",
                    label_smoothing=self.label_smoothing
                ) * self.weights[view_labels]
            else:
                view_cross_entropy = F.cross_entropy(
                    view_logits, view_labels, weight=self.weights, reduction="none")
            view_focal = (self.focal_scale
                          * ((1 - view_pt) ** self.gamma * view_cross_entropy).mean()
                          / self.focal_denominator)
            total = total + self.view_auxiliary * view_focal
            parts["view_auxiliary"] = view_focal.detach()
        return total, parts
