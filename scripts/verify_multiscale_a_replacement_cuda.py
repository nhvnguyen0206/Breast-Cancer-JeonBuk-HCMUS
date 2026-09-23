#!/usr/bin/env python3
"""Verify A53 shared-state/RNG parity and gradients on an RTX 5090."""

import json

import torch

from tn_mammo.loss import MultiTaskLoss
from tn_mammo.model import DensityModel


def build(*, multiscale_a_replacement=False):
    return DensityModel(
        pretrained=False, backbone="convnext_tiny", dropout=0.4,
        bottleneck=256, fusion="hybrid_relational_spatial_attention",
        primary_head="a_gate_hierarchical", attention_dim=256,
        attention_heads=8, attention_layers=2, attention_dropout=0.1,
        spatial_grid_size=4,
        multiscale_a_replacement=multiscale_a_replacement,
    )


def main():
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA allocation is required")
    device = torch.device("cuda")
    gpu = torch.cuda.get_device_name(device)
    if "5090" not in gpu:
        raise RuntimeError(f"Expected RTX 5090, received {gpu}")

    torch.manual_seed(42)
    control = build().to(device).train()
    control_construction_rng = torch.random.get_rng_state().clone()
    torch.manual_seed(42)
    treatment = build(multiscale_a_replacement=True).to(device).train()
    treatment_construction_rng = torch.random.get_rng_state().clone()
    shared_state_exact = all(
        torch.equal(value, treatment.state_dict()[key])
        for key, value in control.state_dict().items()
    )
    views = torch.randn(2, 4, 3, 64, 64, device=device)

    torch.manual_seed(123)
    with torch.no_grad():
        expected = control(views)
    expected_cpu_rng = torch.random.get_rng_state().clone()
    expected_cuda_rng = torch.cuda.get_rng_state(device).clone()
    torch.manual_seed(123)
    with torch.no_grad():
        actual = treatment(views)
    actual_cpu_rng = torch.random.get_rng_state().clone()
    actual_cuda_rng = torch.cuda.get_rng_state(device).clone()
    checks = {
        "construction_cpu_rng_exact": torch.equal(
            control_construction_rng, treatment_construction_rng
        ),
        "shared_state_exact": shared_state_exact,
        "forward_cpu_rng_exact": torch.equal(expected_cpu_rng, actual_cpu_rng),
        "forward_cuda_rng_exact": torch.equal(expected_cuda_rng, actual_cuda_rng),
        "flat_logits_changed": not torch.equal(
            expected["flat_logits"], actual["flat_logits"]
        ),
        "ordinal_logits_exact": torch.equal(
            expected["ordinal_logits"], actual["ordinal_logits"]
        ),
        "binary_logits_exact": torch.equal(
            expected["binary_logits"], actual["binary_logits"]
        ),
    }
    if not all(checks.values()):
        raise RuntimeError(f"A53 parity failed: {checks}")

    treatment.zero_grad(set_to_none=True)
    torch.manual_seed(321)
    outputs = treatment(views)
    loss, _ = MultiTaskLoss([2, 3, 4, 5]).to(device)(
        outputs, torch.tensor([0, 3], device=device)
    )
    loss.backward()
    gradients = {
        "a_gate": treatment.a_gate.weight.grad,
        "fine_projection": treatment.a_multiscale_fusion.fine_projection.weight.grad,
        "coarse_projection": treatment.a_multiscale_fusion.coarse_projection.weight.grad,
        "attention": treatment.a_multiscale_fusion.encoder.layers[0]
        .self_attn.in_proj_weight.grad,
    }
    gradient_l1 = {key: float(value.abs().sum())
                   for key, value in gradients.items()}
    if any(not torch.isfinite(value).all() or gradient_l1[key] <= 0
           for key, value in gradients.items()):
        raise RuntimeError(f"A53 has invalid gradients: {gradient_l1}")

    print(json.dumps({
        "verification": "PASS", "gpu": gpu,
        "architecture": treatment.architecture, **checks,
        "gradient_l1": gradient_l1,
        "control_parameters": sum(p.numel() for p in control.parameters()),
        "treatment_parameters": sum(p.numel() for p in treatment.parameters()),
    }, indent=2))


if __name__ == "__main__":
    main()
