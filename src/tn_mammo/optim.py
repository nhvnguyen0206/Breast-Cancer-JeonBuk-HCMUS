"""Optimizer construction with opt-in discriminative learning rates."""
import math

import torch


def build_optimizer(model, settings):
    ordinal_multiplier = float(settings.get("ordinal_bias_lr_multiplier", 1.0))
    backbone_multiplier = float(settings.get("backbone_lr_multiplier", 1.0))
    for name, multiplier in (("ordinal_bias_lr_multiplier", ordinal_multiplier),
                             ("backbone_lr_multiplier", backbone_multiplier)):
        if not math.isfinite(multiplier) or multiplier <= 0:
            raise ValueError(f"{name} must be finite and positive")
    lr = settings["learning_rate"]
    parameters = model.parameters()
    if ordinal_multiplier != 1.0 or backbone_multiplier != 1.0:
        bias = model.ordinal_bias
        backbone = getattr(model, "features", None)
        if backbone_multiplier != 1.0 and backbone is None:
            raise ValueError("backbone_lr_multiplier requires model.features")
        backbone_ids = ({id(p) for p in backbone.parameters()}
                        if backbone_multiplier != 1.0 else set())
        parameters = [{"params": [p for p in model.parameters()
                                   if p is not bias and id(p) not in backbone_ids]}]
        if backbone_multiplier != 1.0:
            parameters.append({"params": list(backbone.parameters()),
                               "lr": lr * backbone_multiplier})
        if ordinal_multiplier == 1.0:
            parameters[0]["params"].append(bias)
        else:
            parameters.append({"params": [bias], "lr": lr * ordinal_multiplier})
    return torch.optim.AdamW(parameters, lr=lr, weight_decay=settings["weight_decay"])
