import io
import sys
from pathlib import Path
import unittest

import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from tn_mammo.engine import SUPPORTED_ARCHITECTURES
from tn_mammo.loss import MultiTaskLoss
from tn_mammo.model import DensityModel


class PerViewAuxiliaryTests(unittest.TestCase):
    def build(self, enabled=True):
        return DensityModel(
            pretrained=False, backbone="convnext_tiny",
            fusion="local_global_view_attention",
            primary_head="a_gate_hierarchical", attention_dim=32,
            attention_heads=4, attention_layers=1, spatial_grid_size=2,
            view_auxiliary=enabled,
        )

    def test_output_architecture_and_gradients(self):
        model = self.build()
        self.assertIn(model.architecture, SUPPORTED_ARCHITECTURES)
        self.assertTrue(model.architecture.endswith("_v12"))
        output = model(torch.randn(2, 4, 3, 64, 64))
        self.assertEqual(tuple(output["view_logits"].shape), (2, 4, 4))
        torch.testing.assert_close(
            output["flat_logits"].softmax(1).sum(1), torch.ones(2))
        loss, parts = MultiTaskLoss(
            [5, 157, 1244, 208], view_auxiliary=0.25
        )(output, torch.tensor([0, 3]))
        self.assertIn("view_auxiliary", parts)
        loss.backward()
        self.assertGreater(float(model.view_aux_head.weight.grad.abs().sum()), 0)
        local = model.multiscale_attention_fusion.local_encoder
        self.assertGreater(
            float(local.layers[0].self_attn.in_proj_weight.grad.abs().sum()), 0)

    def test_loss_contract_and_shape_validation(self):
        outputs = {
            "flat_logits": torch.randn(2, 4),
            "ordinal_logits": torch.randn(2, 3),
            "binary_logits": torch.randn(2, 2),
        }
        criterion = MultiTaskLoss([5, 157, 1244, 208], view_auxiliary=0.25)
        with self.assertRaisesRegex(ValueError, "view_logits"):
            criterion(outputs, torch.tensor([0, 3]))
        outputs["view_logits"] = torch.randn(2, 3, 4)
        with self.assertRaisesRegex(ValueError, "shape"):
            criterion(outputs, torch.tensor([0, 3]))
        with self.assertRaisesRegex(ValueError, "non-negative"):
            MultiTaskLoss([5, 157, 1244, 208], view_auxiliary=-0.1)

    def test_auxiliary_disabled_preserves_v11_contract(self):
        model = self.build(enabled=False)
        output = model(torch.randn(1, 4, 3, 64, 64))
        self.assertTrue(model.architecture.endswith("_v11"))
        self.assertNotIn("view_logits", output)
        self.assertFalse(hasattr(model, "view_aux_head"))

    def test_common_initialization_is_identical_to_v11(self):
        torch.manual_seed(42)
        baseline = self.build(enabled=False)
        torch.manual_seed(42)
        auxiliary = self.build(enabled=True)
        baseline_state = baseline.state_dict()
        auxiliary_state = auxiliary.state_dict()
        self.assertEqual(set(auxiliary_state) - set(baseline_state),
                         {"view_aux_head.weight", "view_aux_head.bias"})
        for key, value in baseline_state.items():
            torch.testing.assert_close(
                value, auxiliary_state[key], rtol=0, atol=0,
                msg=lambda message: f"{key}: {message}")

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
        self.assertEqual(set(expected), set(actual))
        for key in expected:
            torch.testing.assert_close(expected[key], actual[key], rtol=0, atol=0)

    def test_invalid_model_combination(self):
        with self.assertRaisesRegex(ValueError, "local-global"):
            DensityModel(view_auxiliary=True)
        with self.assertRaisesRegex(ValueError, "boolean"):
            self.build(enabled=1)


if __name__ == "__main__":
    unittest.main()
