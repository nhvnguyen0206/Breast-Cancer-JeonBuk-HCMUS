import sys
from pathlib import Path
import unittest

import torch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from tn_mammo.engine import SUPPORTED_ARCHITECTURES
from tn_mammo.loss import MultiTaskLoss
from tn_mammo.model import DensityModel


class AGateHeadTests(unittest.TestCase):
    def model(self):
        return DensityModel(
            pretrained=False, backbone="convnext_tiny", dropout=0.4,
            bottleneck=256, fusion="hybrid_relational_spatial_attention",
            primary_head="a_gate_hierarchical", attention_dim=64,
            attention_heads=4, attention_layers=1, spatial_grid_size=2,
        )

    def test_distribution_backward_and_architecture(self):
        model = self.model()
        self.assertEqual(model.architecture,
                         "convnext_tiny_hybrid_spatial_a_gate_multitask_v8")
        self.assertIn(model.architecture, SUPPORTED_ARCHITECTURES)
        outputs = model(torch.randn(2, 4, 3, 64, 64))
        probabilities = outputs["flat_logits"].softmax(1)
        self.assertTrue(torch.allclose(probabilities.sum(1), torch.ones(2)))
        loss, _ = MultiTaskLoss([2, 3, 4, 5])(
            outputs, torch.tensor([0, 3]))
        loss.backward()
        for parameter in (model.a_gate.weight, model.bcd_head.weight,
                          model.spatial_attention_fusion.token_projection[0].weight):
            self.assertIsNotNone(parameter.grad)
            self.assertTrue(torch.isfinite(parameter.grad).all())
            self.assertGreater(float(parameter.grad.abs().sum()), 0)

    def test_gate_and_conditional_head_cover_all_four_argmax_classes(self):
        model = self.model().eval()
        with torch.no_grad():
            model.a_gate.weight.zero_()
            model.bcd_head.weight.zero_()
            model.a_gate.bias.fill_(8)
            model.bcd_head.bias.zero_()
            exam = torch.zeros(1, model.feature_dim)
            a = torch.cat((torch.nn.functional.logsigmoid(model.a_gate(exam)),
                           torch.nn.functional.logsigmoid(-model.a_gate(exam))
                           + torch.nn.functional.log_softmax(model.bcd_head(exam), 1)), 1)
            self.assertEqual(int(a.argmax(1)), 0)
            model.a_gate.bias.fill_(-8)
            for expected in range(1, 4):
                model.bcd_head.bias.fill_(-8)
                model.bcd_head.bias[expected - 1] = 8
                bcd = torch.cat((torch.nn.functional.logsigmoid(model.a_gate(exam)),
                                 torch.nn.functional.logsigmoid(-model.a_gate(exam))
                                 + torch.nn.functional.log_softmax(model.bcd_head(exam), 1)), 1)
                self.assertEqual(int(bcd.argmax(1)), expected)

    def test_requires_registered_representation(self):
        with self.assertRaisesRegex(ValueError, "A-gate head requires"):
            DensityModel(pretrained=False, backbone="convnext_tiny",
                         fusion="hierarchical_relational",
                         primary_head="a_gate_hierarchical")


if __name__ == "__main__":
    unittest.main()
