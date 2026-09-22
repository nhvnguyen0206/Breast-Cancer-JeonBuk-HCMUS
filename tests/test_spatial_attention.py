import sys
from pathlib import Path
import unittest

import torch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from tn_mammo.loss import MultiTaskLoss
from tn_mammo.model import DensityModel


class SpatialAttentionTests(unittest.TestCase):
    def test_spatial_token_attention_preserves_regional_tokens(self):
        model = DensityModel(
            pretrained=False, dropout=0.4, fusion="spatial_token_attention",
            attention_dim=64, attention_heads=4, attention_layers=2,
            attention_dropout=0.1, spatial_grid_size=4,
        )
        self.assertEqual(model.architecture,
                         "densenet121_spatial_view_attention_multitask_v3")
        self.assertFalse(hasattr(model, "pair_fusion"))
        outputs = model(torch.randn(2, 4, 3, 64, 64))
        self.assertEqual([tuple(outputs[key].shape) for key in outputs],
                         [(2, 4), (2, 3), (2, 2)])
        loss, _ = MultiTaskLoss([2, 3, 4, 5])(outputs, torch.tensor([0, 3]))
        loss.backward()
        fusion = model.spatial_attention_fusion
        for parameter in (fusion.exam_token, fusion.view_type_embedding,
                          fusion.laterality_embedding, fusion.spatial_embedding):
            self.assertIsNotNone(parameter.grad)
            self.assertTrue(torch.isfinite(parameter.grad).all())
            self.assertGreater(float(parameter.grad.abs().sum()), 0)
        self.assertEqual(tuple(fusion.spatial_embedding.shape), (16, 64))
        self.assertTrue(all(torch.isfinite(value).all() for value in outputs.values()))

    def test_spatial_attention_configuration_validation(self):
        with self.assertRaisesRegex(ValueError, "grid_size"):
            DensityModel(pretrained=False, fusion="spatial_token_attention",
                         spatial_grid_size=0)
        with self.assertRaisesRegex(ValueError, "divisible"):
            DensityModel(pretrained=False, fusion="spatial_token_attention",
                         attention_dim=63, attention_heads=8)


if __name__ == "__main__":
    unittest.main()
