"""Optional FIT-only sampling; never rebalance validation membership."""
import numpy as np
import torch
from torch.utils.data import WeightedRandomSampler


def training_sampler(labels, power, seed):
    """power=0 retains shuffle without replacement; 0.5 tempers, 1 balances.

    Keep the number of draws equal to FIT size for comparable epoch budgets.
    Returns the sampler and expected class probabilities, not realized counts.
    """
    labels = np.asarray(labels)
    if labels.ndim != 1 or not len(labels) or not np.isin(labels, range(4)).all():
        raise ValueError("FIT labels must be nonempty indices 0..3")
    if not np.isfinite(power) or not 0 <= power <= 1:
        raise ValueError("sampling_power must be between zero and one")
    labels = labels.astype(np.int64)
    counts = np.bincount(labels, minlength=4)
    if (counts == 0).any():
        raise ValueError("All four FIT classes are required")
    mass = counts.astype(float) ** (1 - power)
    expected = (mass / mass.sum()).tolist()
    if power == 0:
        return None, expected
    weights = counts[labels].astype(float) ** -power
    return WeightedRandomSampler(weights, num_samples=len(labels), replacement=True,
                                 generator=torch.Generator().manual_seed(seed)), expected
