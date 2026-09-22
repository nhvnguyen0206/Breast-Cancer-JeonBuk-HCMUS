import sys
from pathlib import Path
import unittest

import torch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from tn_mammo.loss import MultiTaskLoss
from tn_mammo.model import DensityModel, MonotonicOrdinalHead


class OrdinalPrimaryTests(unittest.TestCase):
    def test_monotonic_head_produces_valid_class_distribution(self):
        model = DensityModel(
            pretrained=False, dropout=0.4, fusion="hierarchical_relational",
            primary_head="monotonic_ordinal",
        )
        self.assertEqual(model.architecture,
                         "densenet121_hierarchical_bilateral_ordinalprimary_v4")
        self.assertFalse(hasattr(model, "flat_head"))
        outputs = model(torch.randn(2, 4, 3, 64, 64))
        self.assertEqual([tuple(outputs[key].shape) for key in outputs],
                         [(2, 4), (2, 3), (2, 2)])
        ordinal = outputs["ordinal_logits"]
        self.assertTrue(torch.all(ordinal[:, :-1] > ordinal[:, 1:]))
        probabilities = outputs["flat_logits"].softmax(1)
        torch.testing.assert_close(probabilities.sum(1), torch.ones(2))
        self.assertTrue(torch.all(probabilities > 0))

        loss, _ = MultiTaskLoss([2, 3, 4, 5])(outputs, torch.tensor([0, 3]))
        loss.backward()
        for parameter in (model.ordinal_head.score.weight,
                          model.ordinal_head.threshold_start,
                          model.ordinal_head.threshold_deltas):
            self.assertIsNotNone(parameter.grad)
            self.assertTrue(torch.isfinite(parameter.grad).all())
            self.assertGreater(float(parameter.grad.abs().sum()), 0)

    def test_ordinal_primary_configuration_validation(self):
        with self.assertRaisesRegex(ValueError, "Unknown primary"):
            DensityModel(pretrained=False, primary_head="unknown")
        with self.assertRaisesRegex(ValueError, "requires hierarchical"):
            DensityModel(pretrained=False, fusion="view_token_attention",
                         primary_head="monotonic_ordinal")

    def test_wide_threshold_initialization_gives_every_class_an_argmax_region(self):
        head = MonotonicOrdinalHead(input_dim=1, initial_gap=2.0)
        with torch.no_grad():
            head.score.weight.fill_(1.0)
        scores = torch.tensor([[-5.0], [-1.0], [1.0], [5.0]])
        flat_logits, ordinal_logits = head(scores)
        self.assertEqual(flat_logits.argmax(1).tolist(), [0, 1, 2, 3])
        self.assertTrue(torch.all(ordinal_logits[:, :-1] > ordinal_logits[:, 1:]))
        torch.testing.assert_close(flat_logits.softmax(1).sum(1), torch.ones(4))
        model = DensityModel(
            pretrained=False, fusion="hierarchical_relational",
            primary_head="monotonic_ordinal", ordinal_initial_gap=2.0,
        )
        self.assertEqual(model.architecture,
                         "densenet121_hierarchical_bilateral_ordinalprimary_wide_v5")
        with self.assertRaisesRegex(ValueError, "ordinal_initial_gap"):
            DensityModel(pretrained=False, primary_head="monotonic_ordinal",
                         ordinal_initial_gap=1.5)


if __name__ == "__main__":
    unittest.main()
