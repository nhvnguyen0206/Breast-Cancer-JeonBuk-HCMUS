#!/usr/bin/env python3
"""Verify A51 starts bit-exact to A42 and learns on an RTX 5090."""

import json

import torch

from tn_mammo.loss import MultiTaskLoss
from tn_mammo.model import DensityModel


def build(*, bilateral_spatial_relation=False):
    return DensityModel(
        pretrained=False, backbone="convnext_tiny", dropout=0.4,
        bottleneck=256, fusion="hybrid_relational_spatial_attention",
        primary_head="a_gate_hierarchical", attention_dim=256,
        attention_heads=8, attention_layers=2, attention_dropout=0.1,
        spatial_grid_size=4,
        bilateral_spatial_relation=bilateral_spatial_relation,
        bilateral_relation_dim=256,
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
    treatment = build(bilateral_spatial_relation=True).to(device).train()
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
    output_exact = {key: torch.equal(expected[key], actual[key])
                    for key in expected}
    checks = {
        "construction_cpu_rng_exact": torch.equal(
            control_construction_rng, treatment_construction_rng
        ),
        "shared_state_exact": shared_state_exact,
        "forward_cpu_rng_exact": torch.equal(expected_cpu_rng, actual_cpu_rng),
        "forward_cuda_rng_exact": torch.equal(expected_cuda_rng, actual_cuda_rng),
        "outputs_exact": all(output_exact.values()),
    }
    if not all(checks.values()):
        raise RuntimeError(f"A51 parity failed: {checks}; {output_exact}")

    treatment.zero_grad(set_to_none=True)
    torch.manual_seed(321)
    outputs = treatment(views)
    loss, _ = MultiTaskLoss([2, 3, 4, 5]).to(device)(
        outputs, torch.tensor([0, 3], device=device)
    )
    loss.backward()
    gradient = treatment.bilateral_spatial_relation.to_exam.weight.grad
    gradient_sum = float(gradient.abs().sum())
    if not torch.isfinite(gradient).all() or gradient_sum <= 0:
        raise RuntimeError("Bilateral output projection has no finite gradient")

    print(json.dumps({
        "verification": "PASS", "gpu": gpu,
        "architecture": treatment.architecture, **checks,
        "output_keys_exact": output_exact,
        "bilateral_output_gradient_l1": gradient_sum,
        "control_parameters": sum(p.numel() for p in control.parameters()),
        "treatment_parameters": sum(p.numel() for p in treatment.parameters()),
    }, indent=2))


if __name__ == "__main__":
    main()
