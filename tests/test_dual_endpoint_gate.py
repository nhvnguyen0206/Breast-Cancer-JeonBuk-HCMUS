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


class DualEndpointGateTests(unittest.TestCase):
    @staticmethod
    def build(primary_head="dual_endpoint_hierarchical"):
        return DensityModel(
            pretrained=False, backbone="convnext_tiny", dropout=0.4,
            bottleneck=256, fusion="hybrid_relational_spatial_attention",
            primary_head=primary_head, attention_dim=32,
            attention_heads=4, attention_layers=1, spatial_grid_size=2,
        )

    def test_distribution_backward_and_registered_architecture(self):
        model = self.build()
        self.assertEqual(
            model.architecture,
            "convnext_tiny_hybrid_spatial_dual_endpoint_gate_multitask_v14",
        )
        self.assertIn(model.architecture, SUPPORTED_ARCHITECTURES)
        outputs = model(torch.randn(4, 4, 3, 64, 64))
        probabilities = outputs["flat_logits"].softmax(1)
        torch.testing.assert_close(probabilities.sum(1), torch.ones(4))
        self.assertTrue(torch.isfinite(outputs["flat_logits"]).all())
        loss, _ = MultiTaskLoss([2, 3, 4, 5])(
            outputs, torch.tensor([0, 1, 2, 3])
        )
        loss.backward()
        for parameter in (
                model.a_gate.weight, model.bcd_head.weight,
                model.spatial_attention_fusion.token_projection[0].weight):
            self.assertIsNotNone(parameter.grad)
            self.assertTrue(torch.isfinite(parameter.grad).all())
            self.assertGreater(float(parameter.grad.abs().sum()), 0)
        for row in model.bcd_head.weight.grad:
            self.assertGreater(float(row.abs().sum()), 0)

    def test_two_gates_and_bc_head_cover_all_argmax_classes(self):
        model = self.build().eval()
        with torch.no_grad():
            model.a_gate.weight.zero_()
            model.bcd_head.weight.zero_()
            views = torch.zeros(1, 4, 3, 64, 64)

            model.a_gate.bias.fill_(8)
            model.bcd_head.bias.zero_()
            self.assertEqual(int(model(views)["flat_logits"].argmax(1)), 0)

            model.a_gate.bias.fill_(-8)
            model.bcd_head.bias.copy_(torch.tensor([-8.0, 8.0, -8.0]))
            self.assertEqual(int(model(views)["flat_logits"].argmax(1)), 1)

            model.bcd_head.bias.copy_(torch.tensor([-8.0, -8.0, 8.0]))
            self.assertEqual(int(model(views)["flat_logits"].argmax(1)), 2)

            model.bcd_head.bias.copy_(torch.tensor([8.0, 0.0, 0.0]))
            self.assertEqual(int(model(views)["flat_logits"].argmax(1)), 3)

    def test_a42_and_a47_initialization_and_parameter_count_are_exact(self):
        torch.manual_seed(42)
        a42 = self.build(primary_head="a_gate_hierarchical")
        torch.manual_seed(42)
        a47 = self.build()
        self.assertEqual(sum(p.numel() for p in a42.parameters()),
                         sum(p.numel() for p in a47.parameters()))
        self.assertEqual(set(a42.state_dict()), set(a47.state_dict()))
        for key, value in a42.state_dict().items():
            torch.testing.assert_close(value, a47.state_dict()[key], rtol=0, atol=0)

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

    def test_requires_a42_representation(self):
        with self.assertRaisesRegex(ValueError, "Dual-endpoint head requires"):
            DensityModel(
                pretrained=False, backbone="convnext_tiny",
                fusion="hierarchical_relational",
                primary_head="dual_endpoint_hierarchical",
            )


if __name__ == "__main__":
    unittest.main()
