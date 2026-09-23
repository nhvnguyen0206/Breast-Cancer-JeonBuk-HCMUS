import io
import sys
from pathlib import Path
import unittest

import torch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from tn_mammo.engine import SUPPORTED_ARCHITECTURES
from tn_mammo.loss import MultiTaskLoss
from tn_mammo.model import DensityModel


class MultiscaleAExpertTests(unittest.TestCase):
    @staticmethod
    def build(multiscale_a_expert=True, **options):
        return DensityModel(
            pretrained=False, backbone="convnext_tiny", dropout=0.4,
            bottleneck=256, fusion="hybrid_relational_spatial_attention",
            primary_head="a_gate_hierarchical", attention_dim=32,
            attention_heads=4, attention_layers=1, spatial_grid_size=2,
            multiscale_a_expert=multiscale_a_expert, **options,
        )

    def test_registered_architecture_and_validation(self):
        model = self.build()
        self.assertEqual(
            model.architecture,
            "convnext_tiny_hybrid_spatial_a_gate_multiscale_a_expert_v19",
        )
        self.assertIn(model.architecture, SUPPORTED_ARCHITECTURES)
        with self.assertRaisesRegex(ValueError, "must be boolean"):
            self.build(multiscale_a_expert=1)
        with self.assertRaisesRegex(ValueError, "requires the ConvNeXt"):
            DensityModel(
                pretrained=False, backbone="convnext_tiny",
                fusion="hierarchical_relational", primary_head="flat",
                multiscale_a_expert=True,
            )
        for option in ("fine_d_expert", "projection_adapters",
                       "bilateral_spatial_relation"):
            with self.assertRaisesRegex(ValueError, "separate arms"):
                self.build(**{option: True})

    def test_a42_state_output_and_rng_are_bit_exact(self):
        torch.manual_seed(42)
        control = self.build(multiscale_a_expert=False).train()
        control_construction_rng = torch.random.get_rng_state().clone()
        torch.manual_seed(42)
        treatment = self.build().train()
        treatment_construction_rng = torch.random.get_rng_state().clone()
        torch.testing.assert_close(
            control_construction_rng, treatment_construction_rng, rtol=0, atol=0
        )
        control_state, treatment_state = control.state_dict(), treatment.state_dict()
        self.assertTrue(set(treatment_state) - set(control_state))
        self.assertTrue(all(
            key.startswith(("a_multiscale_fusion.", "a_expert_norm.",
                            "a_expert_head."))
            for key in set(treatment_state) - set(control_state)
        ))
        for key, value in control_state.items():
            torch.testing.assert_close(value, treatment_state[key], rtol=0, atol=0)
        torch.testing.assert_close(
            treatment.a_expert_head.weight,
            torch.zeros_like(treatment.a_expert_head.weight), rtol=0, atol=0,
        )

        views = torch.randn(2, 4, 3, 64, 64)
        torch.manual_seed(123)
        expected = control(views)
        expected_rng = torch.random.get_rng_state().clone()
        torch.manual_seed(123)
        actual = treatment(views)
        actual_rng = torch.random.get_rng_state().clone()
        for key in expected:
            torch.testing.assert_close(expected[key], actual[key], rtol=0, atol=0)
        torch.testing.assert_close(expected_rng, actual_rng, rtol=0, atol=0)

    def test_head_then_multiscale_path_receives_gradient(self):
        torch.manual_seed(42)
        model = self.build().train()
        optimizer = torch.optim.SGD(model.parameters(), lr=0.1)
        views = torch.randn(2, 4, 3, 64, 64)
        labels = torch.tensor([0, 3])

        loss, _ = MultiTaskLoss([2, 3, 4, 5])(model(views), labels)
        loss.backward()
        head_gradient = model.a_expert_head.weight.grad
        upstream = model.a_multiscale_fusion.fine_projection.weight.grad
        self.assertTrue(torch.isfinite(head_gradient).all())
        self.assertGreater(float(head_gradient.abs().sum()), 0)
        torch.testing.assert_close(
            upstream, torch.zeros_like(upstream), rtol=0, atol=0
        )
        optimizer.step()
        optimizer.zero_grad(set_to_none=True)

        loss, _ = MultiTaskLoss([2, 3, 4, 5])(model(views), labels)
        loss.backward()
        for gradient in (
                model.a_multiscale_fusion.fine_projection.weight.grad,
                model.a_multiscale_fusion.coarse_projection.weight.grad,
                model.a_multiscale_fusion.encoder.layers[0]
                .self_attn.in_proj_weight.grad):
            self.assertTrue(torch.isfinite(gradient).all())
            self.assertGreater(float(gradient.abs().sum()), 0)

    def test_residual_changes_only_a_gate(self):
        torch.manual_seed(42)
        model = self.build().eval()
        views = torch.randn(1, 4, 3, 64, 64)
        with torch.no_grad():
            model.a_expert_head.weight.zero_()
            model.a_expert_head.bias.fill_(-8)
            negative = model(views)
            model.a_expert_head.bias.fill_(8)
            positive = model(views)
        negative_prob = negative["flat_logits"].exp()
        positive_prob = positive["flat_logits"].exp()
        self.assertGreater(float(positive_prob[:, 0]), float(negative_prob[:, 0]))
        torch.testing.assert_close(
            negative_prob[:, 1:] / negative_prob[:, 1:].sum(1, keepdim=True),
            positive_prob[:, 1:] / positive_prob[:, 1:].sum(1, keepdim=True),
            rtol=1e-6, atol=1e-6,
        )
        torch.testing.assert_close(
            negative["ordinal_logits"], positive["ordinal_logits"], rtol=0, atol=0
        )
        torch.testing.assert_close(
            negative["binary_logits"], positive["binary_logits"], rtol=0, atol=0
        )

    def test_strict_state_roundtrip(self):
        torch.manual_seed(42)
        model = self.build().eval()
        views = torch.randn(1, 4, 3, 64, 64)
        with torch.no_grad():
            expected = model(views)
        stream = io.BytesIO()
        torch.save(model.state_dict(), stream)
        stream.seek(0)
        restored = self.build().eval()
        restored.load_state_dict(torch.load(stream, weights_only=True), strict=True)
        with torch.no_grad():
            actual = restored(views)
        for key in expected:
            torch.testing.assert_close(expected[key], actual[key], rtol=0, atol=0)


if __name__ == "__main__":
    unittest.main()
