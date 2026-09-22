import io
import sys
from pathlib import Path
import unittest

import torch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from tn_mammo.engine import SUPPORTED_ARCHITECTURES
from tn_mammo.loss import MultiTaskLoss
from tn_mammo.model import DensityModel, ProjectionFeatureAdapter


class ProjectionAdapterTests(unittest.TestCase):
    @staticmethod
    def build(projection_adapters=True, projection_adapter_dim=24,
              fine_d_expert=False):
        return DensityModel(
            pretrained=False, backbone="convnext_tiny", dropout=0.4,
            bottleneck=256, fusion="hybrid_relational_spatial_attention",
            primary_head="a_gate_hierarchical", attention_dim=32,
            attention_heads=4, attention_layers=1, spatial_grid_size=2,
            projection_adapters=projection_adapters,
            projection_adapter_dim=projection_adapter_dim,
            fine_d_expert=fine_d_expert,
        )

    def test_validation_and_registered_architecture(self):
        model = self.build()
        self.assertEqual(
            model.architecture,
            "convnext_tiny_hybrid_spatial_a_gate_projection_adapters_v17",
        )
        self.assertIn(model.architecture, SUPPORTED_ARCHITECTURES)
        with self.assertRaisesRegex(ValueError, "projection_adapters must be boolean"):
            self.build(projection_adapters=1)
        with self.assertRaisesRegex(ValueError, "positive integer"):
            self.build(projection_adapter_dim=0)
        with self.assertRaisesRegex(ValueError, "Projection adapters require"):
            DensityModel(
                pretrained=False, backbone="convnext_tiny",
                fusion="hierarchical_relational", primary_head="flat",
                projection_adapters=True,
            )
        with self.assertRaisesRegex(ValueError, "separate arms"):
            self.build(fine_d_expert=True)

    def test_adapter_shape_and_zero_initialization(self):
        adapter = ProjectionFeatureAdapter(channels=16, bottleneck=4)
        features = torch.randn(2, 16, 5, 7)
        residual = adapter(features)
        self.assertEqual(tuple(residual.shape), tuple(features.shape))
        torch.testing.assert_close(residual, torch.zeros_like(residual), rtol=0, atol=0)

    def test_a42_state_output_and_rng_are_bit_exact(self):
        torch.manual_seed(42)
        control = self.build(projection_adapters=False).train()
        control_construction_rng = torch.random.get_rng_state().clone()
        torch.manual_seed(42)
        treatment = self.build(projection_adapters=True).train()
        treatment_construction_rng = torch.random.get_rng_state().clone()
        torch.testing.assert_close(
            control_construction_rng, treatment_construction_rng, rtol=0, atol=0
        )
        control_state, treatment_state = control.state_dict(), treatment.state_dict()
        self.assertTrue(set(treatment_state) - set(control_state))
        self.assertTrue(all(
            key.startswith("projection_feature_adapters.")
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
        for key in expected:
            torch.testing.assert_close(expected[key], actual[key], rtol=0, atol=0)
        torch.testing.assert_close(expected_rng, actual_rng, rtol=0, atol=0)

    def test_output_projection_then_bottleneck_receives_gradient(self):
        torch.manual_seed(42)
        model = self.build().train()
        optimizer = torch.optim.SGD(model.parameters(), lr=0.1)
        views = torch.randn(2, 4, 3, 64, 64)
        labels = torch.tensor([0, 3])
        adapter = model.projection_feature_adapters[0]

        loss, _ = MultiTaskLoss([2, 3, 4, 5])(model(views), labels)
        loss.backward()
        self.assertGreater(float(adapter.up.weight.grad.abs().sum()), 0)
        torch.testing.assert_close(
            adapter.down.weight.grad, torch.zeros_like(adapter.down.weight.grad),
            rtol=0, atol=0,
        )
        optimizer.step()
        optimizer.zero_grad(set_to_none=True)

        loss, _ = MultiTaskLoss([2, 3, 4, 5])(model(views), labels)
        loss.backward()
        self.assertTrue(torch.isfinite(adapter.down.weight.grad).all())
        self.assertGreater(float(adapter.down.weight.grad.abs().sum()), 0)

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
