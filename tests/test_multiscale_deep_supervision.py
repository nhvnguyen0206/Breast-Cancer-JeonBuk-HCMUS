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


class MultiscaleDeepSupervisionTests(unittest.TestCase):
    @staticmethod
    def build(*, multiscale_deep_supervision=True,
              multiscale_a_replacement=False, **options):
        return DensityModel(
            pretrained=False, backbone="convnext_tiny", dropout=0.4,
            bottleneck=256, fusion="hybrid_relational_spatial_attention",
            primary_head="a_gate_hierarchical", attention_dim=32,
            attention_heads=4, attention_layers=1, spatial_grid_size=2,
            multiscale_deep_supervision=multiscale_deep_supervision,
            multiscale_a_replacement=multiscale_a_replacement,
            **options,
        )

    def test_registered_architecture_and_validation(self):
        model = self.build()
        self.assertEqual(
            model.architecture,
            "convnext_tiny_hybrid_bcd_multiscale_a_gate_deepsup_v21",
        )
        self.assertIn(model.architecture, SUPPORTED_ARCHITECTURES)
        with self.assertRaisesRegex(ValueError, "must be boolean"):
            self.build(multiscale_deep_supervision=1)
        with self.assertRaisesRegex(ValueError, "requires the ConvNeXt"):
            DensityModel(
                pretrained=False, backbone="convnext_tiny",
                fusion="hierarchical_relational", primary_head="flat",
                multiscale_deep_supervision=True,
            )
        for option in ("fine_d_expert", "projection_adapters",
                       "bilateral_spatial_relation", "multiscale_a_expert",
                       "multiscale_a_replacement"):
            with self.assertRaisesRegex(ValueError, "separate arms"):
                self.build(**{option: True})

    def test_a53_shared_state_rng_and_primary_outputs_are_exact(self):
        torch.manual_seed(42)
        control = self.build(
            multiscale_deep_supervision=False,
            multiscale_a_replacement=True,
        ).train()
        control_construction_rng = torch.random.get_rng_state().clone()
        torch.manual_seed(42)
        treatment = self.build().train()
        treatment_construction_rng = torch.random.get_rng_state().clone()
        torch.testing.assert_close(
            control_construction_rng, treatment_construction_rng,
            rtol=0, atol=0,
        )
        control_state, treatment_state = control.state_dict(), treatment.state_dict()
        extra = set(treatment_state) - set(control_state)
        self.assertEqual(extra, {
            "a_multiscale_aux_bcd_head.weight",
            "a_multiscale_aux_bcd_head.bias",
            "a_multiscale_aux_ordinal_score.weight",
            "a_multiscale_aux_ordinal_bias",
            "a_multiscale_aux_binary_head.weight",
            "a_multiscale_aux_binary_head.bias",
        })
        for key, value in control_state.items():
            torch.testing.assert_close(value, treatment_state[key], rtol=0, atol=0)

        views = torch.randn(2, 4, 3, 64, 64)
        torch.manual_seed(123)
        expected = control(views)
        expected_rng = torch.random.get_rng_state().clone()
        torch.manual_seed(123)
        actual = treatment(views)
        actual_rng = torch.random.get_rng_state().clone()
        torch.testing.assert_close(expected_rng, actual_rng, rtol=0, atol=0)
        for key in ("flat_logits", "ordinal_logits", "binary_logits"):
            torch.testing.assert_close(expected[key], actual[key], rtol=0, atol=0)
        self.assertEqual(set(actual) - set(expected), {
            "multiscale_aux_flat_logits",
            "multiscale_aux_ordinal_logits",
            "multiscale_aux_binary_logits",
        })

    def test_auxiliary_loss_and_all_treatment_gradients(self):
        torch.manual_seed(42)
        model = self.build().train()
        views = torch.randn(2, 4, 3, 64, 64)
        labels = torch.tensor([0, 3])
        outputs = model(views)
        primary, _ = MultiTaskLoss([2, 3, 4, 5])(outputs, labels)
        total, parts = MultiTaskLoss(
            [2, 3, 4, 5], multiscale_auxiliary=.5
        )(outputs, labels)
        torch.testing.assert_close(
            total, primary + .5 * parts["multiscale_auxiliary"]
        )
        total.backward()
        gradients = (
            model.a_gate.weight.grad,
            model.a_multiscale_aux_bcd_head.weight.grad,
            model.a_multiscale_aux_ordinal_score.weight.grad,
            model.a_multiscale_aux_ordinal_bias.grad,
            model.a_multiscale_aux_binary_head.weight.grad,
            model.a_multiscale_fusion.fine_projection.weight.grad,
            model.a_multiscale_fusion.coarse_projection.weight.grad,
            model.a_multiscale_fusion.encoder.layers[0]
            .self_attn.in_proj_weight.grad,
        )
        for gradient in gradients:
            self.assertTrue(torch.isfinite(gradient).all())
            self.assertGreater(float(gradient.abs().sum()), 0)
        with self.assertRaisesRegex(ValueError, "outputs are required"):
            MultiTaskLoss(
                [2, 3, 4, 5], multiscale_auxiliary=.5
            )({key: outputs[key] for key in (
                "flat_logits", "ordinal_logits", "binary_logits"
            )}, labels)

    def test_eval_outputs_are_primary_only_and_strict_roundtrip(self):
        torch.manual_seed(42)
        model = self.build().eval()
        views = torch.randn(1, 4, 3, 64, 64)
        with torch.no_grad():
            expected = model(views)
        self.assertEqual(set(expected), {
            "flat_logits", "ordinal_logits", "binary_logits",
        })
        self.assertTrue(all(torch.isfinite(value).all()
                            for value in expected.values()))
        torch.testing.assert_close(
            expected["flat_logits"].softmax(1).sum(1), torch.ones(1)
        )
        stream = io.BytesIO()
        torch.save(model.state_dict(), stream)
        stream.seek(0)
        restored = self.build().eval()
        restored.load_state_dict(
            torch.load(stream, weights_only=True), strict=True
        )
        with torch.no_grad():
            actual = restored(views)
        for key in expected:
            torch.testing.assert_close(expected[key], actual[key], rtol=0, atol=0)

    def test_loss_weight_validation(self):
        for value in (-1, float("inf"), float("nan")):
            with self.assertRaisesRegex(ValueError, "finite and non-negative"):
                MultiTaskLoss([2, 3, 4, 5], multiscale_auxiliary=value)


if __name__ == "__main__":
    unittest.main()
