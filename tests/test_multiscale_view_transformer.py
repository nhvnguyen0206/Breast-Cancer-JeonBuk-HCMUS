import sys
from pathlib import Path
import unittest

import torch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from tn_mammo.engine import SUPPORTED_ARCHITECTURES
from tn_mammo.loss import MultiTaskLoss
from tn_mammo.model import DensityModel, MultiScaleViewTokenFusion


class MultiScaleViewTransformerTests(unittest.TestCase):
    def model(self, primary_head="flat"):
        return DensityModel(
            pretrained=False, backbone="convnext_tiny", dropout=0.4,
            fusion="multiscale_view_token_attention",
            primary_head=primary_head, attention_dim=64, attention_heads=4,
            attention_layers=1, spatial_grid_size=2,
        )

    def test_replaces_handcrafted_fusion_and_backpropagates_both_scales(self):
        model = self.model()
        self.assertEqual(
            model.architecture,
            "convnext_tiny_multiscale_view_transformer_multitask_v9",
        )
        self.assertIn(model.architecture, SUPPORTED_ARCHITECTURES)
        self.assertFalse(hasattr(model, "pair_fusion"))
        outputs = model(torch.randn(1, 4, 3, 64, 64))
        self.assertEqual([tuple(outputs[key].shape) for key in outputs],
                         [(1, 4), (1, 3), (1, 2)])
        loss, _ = MultiTaskLoss([2, 3, 4, 5])(outputs, torch.tensor([2]))
        loss.backward()
        fusion = model.multiscale_attention_fusion
        for parameter in (fusion.fine_projection.weight,
                          fusion.coarse_projection.weight,
                          fusion.exam_token, model.flat_head.weight):
            self.assertIsNotNone(parameter.grad)
            self.assertTrue(torch.isfinite(parameter.grad).all())
            self.assertGreater(float(parameter.grad.abs().sum()), 0)

    def test_a_gate_variant_is_registered_and_normalized(self):
        model = self.model(primary_head="a_gate_hierarchical")
        self.assertEqual(
            model.architecture,
            "convnext_tiny_multiscale_view_transformer_a_gate_v10",
        )
        self.assertIn(model.architecture, SUPPORTED_ARCHITECTURES)
        probabilities = model(torch.randn(2, 4, 3, 64, 64))["flat_logits"].softmax(1)
        self.assertTrue(torch.allclose(probabilities.sum(1), torch.ones(2), atol=1e-6))

    def test_view_mask_validation_and_missing_view_support(self):
        fusion = MultiScaleViewTokenFusion(
            fine_dim=8, coarse_dim=16, token_dim=16, heads=4, layers=1,
            fine_grid_size=2, coarse_grid_size=1,
        )
        fine = torch.randn(2, 4, 8, 4, 4)
        coarse = torch.randn(2, 4, 16, 2, 2)
        mask = torch.tensor([[1, 1, 1, 1], [1, 0, 1, 0]], dtype=torch.bool)
        self.assertEqual(tuple(fusion(fine, coarse, mask).shape), (2, 16))
        with self.assertRaisesRegex(ValueError, "at least one view"):
            fusion(fine, coarse, torch.zeros(2, 4, dtype=torch.bool))

    def test_requires_convnext(self):
        with self.assertRaisesRegex(ValueError, "requires ConvNeXt"):
            DensityModel(pretrained=False, backbone="densenet121",
                         fusion="multiscale_view_token_attention")


if __name__ == "__main__":
    unittest.main()
