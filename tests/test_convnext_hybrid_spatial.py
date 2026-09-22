import sys
from pathlib import Path
import unittest

import torch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from tn_mammo.loss import MultiTaskLoss
from tn_mammo.model import DensityModel
from tn_mammo.engine import SUPPORTED_ARCHITECTURES


class ConvNeXtHybridSpatialTests(unittest.TestCase):
    def test_hybrid_forward_backward_and_spatial_gradient(self):
        model = DensityModel(
            pretrained=False, backbone="convnext_tiny", dropout=0.4,
            bottleneck=256, fusion="hybrid_relational_spatial_attention",
            primary_head="flat", attention_dim=64, attention_heads=4,
            attention_layers=1, spatial_grid_size=2,
        )
        self.assertEqual(
            model.architecture,
            "convnext_tiny_hybrid_relational_spatial_multitask_v7",
        )
        self.assertIn(model.architecture, SUPPORTED_ARCHITECTURES)
        self.assertAlmostEqual(float(model.spatial_residual_logit.sigmoid()),
                               0.1, places=5)
        outputs = model(torch.randn(1, 4, 3, 64, 64))
        self.assertEqual([tuple(outputs[key].shape) for key in outputs],
                         [(1, 4), (1, 3), (1, 2)])
        loss, _ = MultiTaskLoss([2, 3, 4, 5])(outputs, torch.tensor([2]))
        loss.backward()
        parameters = (
            model.pair_fusion.gate.weight,
            model.spatial_attention_fusion.token_projection[0].weight,
            model.spatial_residual_logit,
            model.flat_head.weight,
        )
        for parameter in parameters:
            self.assertIsNotNone(parameter.grad)
            self.assertTrue(torch.isfinite(parameter.grad).all())
            self.assertGreater(float(parameter.grad.abs().sum()), 0)

    def test_hybrid_requires_convnext(self):
        with self.assertRaisesRegex(ValueError, "requires ConvNeXt"):
            DensityModel(pretrained=False, backbone="densenet121",
                         fusion="hybrid_relational_spatial_attention")


if __name__ == "__main__":
    unittest.main()
