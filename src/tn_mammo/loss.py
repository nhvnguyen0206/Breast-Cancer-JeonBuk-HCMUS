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
    def __init__(self, counts, beta=0.999, gamma=2.0, ordinal=0.5, binary=0.3, neighbor=0.2):
        super().__init__()
        self.gamma, self.ordinal, self.binary, self.neighbor = gamma, ordinal, binary, neighbor
        self.register_buffer("weights", class_weights(counts, beta))
        self.register_buffer("binary_weights", class_weights([sum(counts[:2]), sum(counts[2:])], beta))
        self.register_buffer("cost", torch.tensor([
            [0., 1., 3., 5.], [1., 0., 1.5, 2.5],
            [3., 1.5, 0., 3.], [5., 2.5, 3., 0.],
        ]))

    def forward(self, outputs, labels):
        logits = outputs["flat_logits"].float()
        probs = logits.softmax(dim=1)
        pt = probs.gather(1, labels[:, None]).squeeze(1)
        focal = ((1 - pt) ** self.gamma * F.cross_entropy(
            logits, labels, weight=self.weights, reduction="none")).mean()
        levels = (labels[:, None] > torch.arange(3, device=labels.device)).float()
        # Sum threshold losses per case, then average cases (CORAL reduction).
        ordinal = F.binary_cross_entropy_with_logits(
            outputs["ordinal_logits"].float(), levels, reduction="none").sum(1).mean()
        binary = F.cross_entropy(outputs["binary_logits"].float(), (labels >= 2).long(),
                                 weight=self.binary_weights)
        neighbor = (probs * self.cost[labels]).sum(1).mean()
        total = focal + self.ordinal * ordinal + self.binary * binary + self.neighbor * neighbor
        return total, {"focal": focal.detach(), "ordinal": ordinal.detach(),
                       "binary": binary.detach(), "neighbor": neighbor.detach()}
