import io
import sys
from pathlib import Path
import unittest

import torch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from tn_mammo.engine import SUPPORTED_ARCHITECTURES
from tn_mammo.loss import MultiTaskLoss
from tn_mammo.model import BilateralSpatialRelation, DensityModel


class BilateralSpatialRelationTests(unittest.TestCase):
    @staticmethod
    def build(bilateral_spatial_relation=True, bilateral_relation_dim=24,
              fine_d_expert=False, projection_adapters=False):
        return DensityModel(
            pretrained=False, backbone="convnext_tiny", dropout=0.4,
            bottleneck=256, fusion="hybrid_relational_spatial_attention",
            primary_head="a_gate_hierarchical", attention_dim=32,
            attention_heads=4, attention_layers=1, spatial_grid_size=2,
            bilateral_spatial_relation=bilateral_spatial_relation,
            bilateral_relation_dim=bilateral_relation_dim,
            fine_d_expert=fine_d_expert,
            projection_adapters=projection_adapters,
        )

    def test_validation_and_registered_architecture(self):
        model = self.build()
        self.assertEqual(
            model.architecture,
            "convnext_tiny_hybrid_spatial_a_gate_bilateral_relation_v18",
        )
        self.assertIn(model.architecture, SUPPORTED_ARCHITECTURES)
        with self.assertRaisesRegex(ValueError, "must be boolean"):
            self.build(bilateral_spatial_relation=1)
        with self.assertRaisesRegex(ValueError, "positive integer"):
            self.build(bilateral_relation_dim=0)
        with self.assertRaisesRegex(ValueError, "requires the ConvNeXt"):
            DensityModel(
                pretrained=False, backbone="convnext_tiny",
                fusion="hierarchical_relational", primary_head="flat",
                bilateral_spatial_relation=True,
            )
        with self.assertRaisesRegex(ValueError, "separate arms"):
            self.build(fine_d_expert=True)
        with self.assertRaisesRegex(ValueError, "separate arms"):
            self.build(projection_adapters=True)

    def test_zero_initialization_shape_and_side_symmetry(self):
        torch.manual_seed(42)
        relation = BilateralSpatialRelation(
            channels=16, hidden_dim=4, grid_size=3
        ).eval()
        maps = torch.randn(2, 4, 16, 5, 7)
        output = relation(maps)
        self.assertEqual(tuple(output.shape), (2, 16))
        torch.testing.assert_close(output, torch.zeros_like(output), rtol=0, atol=0)

        torch.nn.init.normal_(relation.to_exam.weight)
        swapped = torch.stack((
            torch.flip(maps[:, 2], dims=(-1,)),
            torch.flip(maps[:, 3], dims=(-1,)),
            torch.flip(maps[:, 0], dims=(-1,)),
            torch.flip(maps[:, 1], dims=(-1,)),
        ), dim=1)
        torch.testing.assert_close(
            relation(maps), relation(swapped), rtol=1e-6, atol=1e-6
        )

    def test_a42_state_output_and_rng_are_bit_exact(self):
        torch.manual_seed(42)
        control = self.build(bilateral_spatial_relation=False).train()
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
            key.startswith("bilateral_spatial_relation.")
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

    def test_output_projection_then_spatial_path_receives_gradient(self):
        torch.manual_seed(42)
        model = self.build().train()
        optimizer = torch.optim.SGD(model.parameters(), lr=0.1)
        views = torch.randn(2, 4, 3, 64, 64)
        labels = torch.tensor([0, 3])
        relation = model.bilateral_spatial_relation

        loss, _ = MultiTaskLoss([2, 3, 4, 5])(model(views), labels)
        loss.backward()
        self.assertGreater(float(relation.to_exam.weight.grad.abs().sum()), 0)
        torch.testing.assert_close(
            relation.relation_projection.weight.grad,
            torch.zeros_like(relation.relation_projection.weight.grad),
            rtol=0, atol=0,
        )
        optimizer.step()
        optimizer.zero_grad(set_to_none=True)

        loss, _ = MultiTaskLoss([2, 3, 4, 5])(model(views), labels)
        loss.backward()
        for gradient in (relation.relation_projection.weight.grad,
                         relation.depthwise.weight.grad):
            self.assertTrue(torch.isfinite(gradient).all())
            self.assertGreater(float(gradient.abs().sum()), 0)

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
