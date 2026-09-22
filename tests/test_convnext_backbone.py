import sys
from pathlib import Path
import unittest

import torch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from tn_mammo.loss import MultiTaskLoss
from tn_mammo.model import DensityModel


class ConvNeXtBackboneTests(unittest.TestCase):
    def test_convnext_relational_forward_and_backward(self):
        model = DensityModel(
            pretrained=False, backbone="convnext_tiny", dropout=0.4,
            bottleneck=256, fusion="hierarchical_relational", primary_head="flat",
        )
        self.assertEqual(model.architecture,
                         "convnext_tiny_hierarchical_bilateral_multitask_v6")
        self.assertEqual(model.feature_dim, 768)
        outputs = model(torch.randn(1, 4, 3, 64, 64))
        self.assertEqual([tuple(outputs[key].shape) for key in outputs],
                         [(1, 4), (1, 3), (1, 2)])
        loss, _ = MultiTaskLoss([2, 3, 4, 5])(outputs, torch.tensor([2]))
        loss.backward()
        for parameter in (model.pair_fusion.gate.weight, model.side_gate.weight,
                          model.flat_head.weight, model.ordinal_score.weight,
                          model.binary_head.weight):
            self.assertIsNotNone(parameter.grad)
            self.assertTrue(torch.isfinite(parameter.grad).all())
            self.assertGreater(float(parameter.grad.abs().sum()), 0)

    def test_convnext_configuration_is_isolated(self):
        with self.assertRaisesRegex(ValueError, "Unknown backbone"):
            DensityModel(pretrained=False, backbone="unknown")
        with self.assertRaisesRegex(ValueError, "requires relational"):
            DensityModel(pretrained=False, backbone="convnext_tiny",
                         fusion="view_token_attention")
        with self.assertRaisesRegex(ValueError, "requires relational"):
            DensityModel(pretrained=False, backbone="convnext_tiny",
                         primary_head="monotonic_ordinal")


if __name__ == "__main__":
    unittest.main()
