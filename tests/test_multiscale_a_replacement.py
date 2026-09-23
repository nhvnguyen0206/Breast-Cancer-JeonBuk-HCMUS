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


class MultiscaleAReplacementTests(unittest.TestCase):
    @staticmethod
    def build(multiscale_a_replacement=True, **options):
        return DensityModel(
            pretrained=False, backbone="convnext_tiny", dropout=0.4,
            bottleneck=256, fusion="hybrid_relational_spatial_attention",
            primary_head="a_gate_hierarchical", attention_dim=32,
            attention_heads=4, attention_layers=1, spatial_grid_size=2,
            multiscale_a_replacement=multiscale_a_replacement, **options,
        )

    def test_registered_architecture_and_validation(self):
        model = self.build()
        self.assertEqual(
            model.architecture,
            "convnext_tiny_hybrid_bcd_multiscale_a_gate_v20",
        )
        self.assertIn(model.architecture, SUPPORTED_ARCHITECTURES)
        with self.assertRaisesRegex(ValueError, "must be boolean"):
            self.build(multiscale_a_replacement=1)
        with self.assertRaisesRegex(ValueError, "requires the ConvNeXt"):
            DensityModel(
                pretrained=False, backbone="convnext_tiny",
                fusion="hierarchical_relational", primary_head="flat",
                multiscale_a_replacement=True,
            )
        for option in ("fine_d_expert", "projection_adapters",
                       "bilateral_spatial_relation", "multiscale_a_expert"):
            with self.assertRaisesRegex(ValueError, "separate arms"):
                self.build(**{option: True})

    def test_shared_state_and_rng_exact_with_intentional_a_change(self):
        torch.manual_seed(42)
        control = self.build(multiscale_a_replacement=False).train()
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
            key.startswith(("a_multiscale_fusion.", "a_expert_norm."))
            for key in set(treatment_state) - set(control_state)
        ))
        for key, value in control_state.items():
            torch.testing.assert_close(value, treatment_state[key], rtol=0, atol=0)

        views = torch.randn(2, 4, 3, 64, 64)
        torch.manual_seed(123)
        expected = control(views)
        expected_rng = torch.random.get_rng_state().clone()
        torch.manual_seed(123)
        actual = treatment(views)
        actual_rng = torch.random.get_rng_state().clone()
        torch.testing.assert_close(expected_rng, actual_rng, rtol=0, atol=0)
        self.assertFalse(torch.equal(expected["flat_logits"], actual["flat_logits"]))
        for key in ("ordinal_logits", "binary_logits"):
            torch.testing.assert_close(expected[key], actual[key], rtol=0, atol=0)
        expected_prob = expected["flat_logits"].exp()
        actual_prob = actual["flat_logits"].exp()
        torch.testing.assert_close(
            expected_prob[:, 1:] / expected_prob[:, 1:].sum(1, keepdim=True),
            actual_prob[:, 1:] / actual_prob[:, 1:].sum(1, keepdim=True),
            rtol=1e-6, atol=1e-6,
        )

    def test_a_gate_and_multiscale_path_receive_first_step_gradient(self):
        torch.manual_seed(42)
        model = self.build().train()
        views = torch.randn(2, 4, 3, 64, 64)
        labels = torch.tensor([0, 3])
        loss, _ = MultiTaskLoss([2, 3, 4, 5])(model(views), labels)
        loss.backward()
        for gradient in (
                model.a_gate.weight.grad,
                model.a_multiscale_fusion.fine_projection.weight.grad,
                model.a_multiscale_fusion.coarse_projection.weight.grad,
                model.a_multiscale_fusion.encoder.layers[0]
                .self_attn.in_proj_weight.grad):
            self.assertTrue(torch.isfinite(gradient).all())
            self.assertGreater(float(gradient.abs().sum()), 0)

    def test_outputs_are_finite_normalized_and_strict_roundtrip(self):
        torch.manual_seed(42)
        model = self.build().eval()
        views = torch.randn(1, 4, 3, 64, 64)
        with torch.no_grad():
            expected = model(views)
        self.assertEqual([tuple(expected[key].shape) for key in expected],
                         [(1, 4), (1, 3), (1, 2)])
        self.assertTrue(all(torch.isfinite(value).all()
                            for value in expected.values()))
        torch.testing.assert_close(
            expected["flat_logits"].softmax(1).sum(1), torch.ones(1)
        )
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
