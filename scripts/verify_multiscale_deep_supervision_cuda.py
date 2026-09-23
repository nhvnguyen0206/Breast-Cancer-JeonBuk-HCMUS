#!/usr/bin/env python3
"""Verify A54 is A53-exact at inference and learns through every auxiliary head."""

import json

import torch

from tn_mammo.loss import MultiTaskLoss
from tn_mammo.model import DensityModel


def build(*, multiscale_a_replacement=False,
          multiscale_deep_supervision=False):
    return DensityModel(
        pretrained=False, backbone="convnext_tiny", dropout=0.4,
        bottleneck=256, fusion="hybrid_relational_spatial_attention",
        primary_head="a_gate_hierarchical", attention_dim=256,
        attention_heads=8, attention_layers=2, attention_dropout=0.1,
        spatial_grid_size=4,
        multiscale_a_replacement=multiscale_a_replacement,
        multiscale_deep_supervision=multiscale_deep_supervision,
    )


def main():
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA allocation is required")
    device = torch.device("cuda")
    gpu = torch.cuda.get_device_name(device)
    if "5090" not in gpu:
        raise RuntimeError(f"Expected RTX 5090, received {gpu}")

    torch.manual_seed(42)
    control = build(multiscale_a_replacement=True).to(device).train()
    control_construction_rng = torch.random.get_rng_state().clone()
    torch.manual_seed(42)
    treatment = build(multiscale_deep_supervision=True).to(device).train()
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
        "primary_flat_exact": torch.equal(
            expected["flat_logits"], actual["flat_logits"]
        ),
        "primary_ordinal_exact": torch.equal(
            expected["ordinal_logits"], actual["ordinal_logits"]
        ),
        "primary_binary_exact": torch.equal(
            expected["binary_logits"], actual["binary_logits"]
        ),
        "auxiliary_outputs_present": set(actual) - set(expected) == {
            "multiscale_aux_flat_logits",
            "multiscale_aux_ordinal_logits",
            "multiscale_aux_binary_logits",
        },
    }
    if not all(checks.values()):
        raise RuntimeError(f"A54 parity failed: {checks}")

    treatment.zero_grad(set_to_none=True)
    torch.manual_seed(321)
    outputs = treatment(views)
    loss, parts = MultiTaskLoss(
        [2, 3, 4, 5], multiscale_auxiliary=.5
    ).to(device)(outputs, torch.tensor([0, 3], device=device))
    loss.backward()
    gradients = {
        "a_gate": treatment.a_gate.weight.grad,
        "aux_bcd": treatment.a_multiscale_aux_bcd_head.weight.grad,
        "aux_ordinal": treatment.a_multiscale_aux_ordinal_score.weight.grad,
        "aux_binary": treatment.a_multiscale_aux_binary_head.weight.grad,
        "fine_projection": treatment.a_multiscale_fusion.fine_projection.weight.grad,
        "coarse_projection": treatment.a_multiscale_fusion.coarse_projection.weight.grad,
        "attention": treatment.a_multiscale_fusion.encoder.layers[0]
        .self_attn.in_proj_weight.grad,
    }
    gradient_l1 = {key: float(value.abs().sum())
                   for key, value in gradients.items()}
    if any(not torch.isfinite(value).all() or gradient_l1[key] <= 0
           for key, value in gradients.items()):
        raise RuntimeError(f"A54 has invalid gradients: {gradient_l1}")

    print(json.dumps({
        "verification": "PASS", "gpu": gpu,
        "architecture": treatment.architecture, **checks,
        "loss": float(loss.detach()),
        "auxiliary_loss": float(parts["multiscale_auxiliary"]),
        "gradient_l1": gradient_l1,
        "control_parameters": sum(p.numel() for p in control.parameters()),
        "treatment_parameters": sum(p.numel() for p in treatment.parameters()),
    }, indent=2))


if __name__ == "__main__":
    main()
