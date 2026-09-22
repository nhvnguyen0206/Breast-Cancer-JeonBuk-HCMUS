import io
import sys
from pathlib import Path
import unittest

import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from tn_mammo.engine import SUPPORTED_ARCHITECTURES
from tn_mammo.loss import MultiTaskLoss
from tn_mammo.model import DensityModel, ExamMixStyle


class ExamMixStyleTests(unittest.TestCase):
    @staticmethod
    def build(probability=0.5):
        return DensityModel(
            pretrained=False, backbone="convnext_tiny",
            fusion="local_global_view_attention",
            primary_head="a_gate_hierarchical", attention_dim=32,
            attention_heads=4, attention_layers=1, spatial_grid_size=2,
            view_auxiliary=True, mixstyle_probability=probability,
            mixstyle_alpha=0.1,
        )

    def test_training_mixes_different_exams_with_one_lambda_per_exam(self):
        layer = ExamMixStyle(probability=1.0, alpha=0.1).train()
        pattern = torch.tensor([[-1.5, -0.5], [0.5, 1.5]])
        own_means = torch.tensor([
            [[0.0, 1.0], [2.0, 3.0], [4.0, 5.0], [6.0, 7.0]],
            [[10.0, 11.0], [12.0, 13.0], [14.0, 15.0], [16.0, 17.0]],
        ])
        maps = pattern[None, None, None] + own_means[..., None, None]
        torch.manual_seed(42)
        mixed = layer(maps)
        mixed_means = mixed.mean(dim=(-2, -1))
        paired_means = own_means.flip(0)
        inferred = (mixed_means - paired_means) / (own_means - paired_means)
        self.assertGreater(float((mixed - maps).abs().max()), 1e-4)
        for exam in range(2):
            torch.testing.assert_close(
                inferred[exam], inferred[exam, :1, :1].expand_as(inferred[exam]),
                rtol=1e-5, atol=1e-5,
            )
            self.assertTrue(bool(((inferred[exam] >= 0) & (inferred[exam] <= 1)).all()))

    def test_eval_probability_zero_and_single_exam_are_exact_identity(self):
        maps = torch.randn(2, 4, 3, 4, 4)
        for layer, value in (
                (ExamMixStyle(1.0, 0.1).eval(), maps),
                (ExamMixStyle(0.0, 0.1).train(), maps),
                (ExamMixStyle(1.0, 0.1).train(), maps[:1])):
            torch.testing.assert_close(layer(value), value, rtol=0, atol=0)

    def test_shape_and_hyperparameter_validation(self):
        for probability in (-0.1, 1.1, float("nan"), True, "0.5"):
            with self.assertRaisesRegex(ValueError, "probability"):
                ExamMixStyle(probability, 0.1)
        for alpha in (0, -1, float("inf"), True, "0.1"):
            with self.assertRaisesRegex(ValueError, "alpha"):
                ExamMixStyle(0.5, alpha)
        with self.assertRaisesRegex(ValueError, "expects"):
            ExamMixStyle(1.0)(torch.randn(2, 3, 4, 4))
        with self.assertRaisesRegex(ValueError, "requires"):
            DensityModel(mixstyle_probability=0.5)

    def test_v13_forward_backward_and_registered_architecture(self):
        model = self.build()
        self.assertIn(model.architecture, SUPPORTED_ARCHITECTURES)
        self.assertTrue(model.architecture.endswith("_v13"))
        output = model(torch.randn(2, 4, 3, 64, 64))
        loss, parts = MultiTaskLoss(
            [5, 157, 1244, 208], view_auxiliary=0.25
        )(output, torch.tensor([0, 3]))
        self.assertIn("view_auxiliary", parts)
        loss.backward()
        self.assertTrue(torch.isfinite(model.features[0][0].weight.grad).all())
        self.assertGreater(float(model.features[0][0].weight.grad.abs().sum()), 0)

    def test_a45_common_initialization_and_eval_output_are_bit_exact(self):
        torch.manual_seed(42)
        a45 = self.build(probability=0.0).eval()
        torch.manual_seed(42)
        a46 = self.build(probability=0.5).eval()
        self.assertTrue(a45.architecture.endswith("_v12"))
        self.assertEqual(set(a45.state_dict()), set(a46.state_dict()))
        for key, value in a45.state_dict().items():
            torch.testing.assert_close(value, a46.state_dict()[key], rtol=0, atol=0)
        views = torch.randn(1, 4, 3, 64, 64)
        with torch.no_grad():
            expected, actual = a45(views), a46(views)
        self.assertEqual(set(expected), set(actual))
        for key in expected:
            torch.testing.assert_close(expected[key], actual[key], rtol=0, atol=0)

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
