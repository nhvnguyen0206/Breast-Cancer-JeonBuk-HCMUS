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


class FineDExpertTests(unittest.TestCase):
    @staticmethod
    def build(fine_d_expert=True, isolate_fine_d_rng=False):
        return DensityModel(
            pretrained=False, backbone="convnext_tiny", dropout=0.4,
            bottleneck=256, fusion="hybrid_relational_spatial_attention",
            primary_head="a_gate_hierarchical", attention_dim=32,
            attention_heads=4, attention_layers=1, spatial_grid_size=2,
            fine_d_expert=fine_d_expert,
            isolate_fine_d_rng=isolate_fine_d_rng,
        )

    def test_distribution_backward_and_registered_architecture(self):
        model = self.build()
        self.assertEqual(
            model.architecture,
            "convnext_tiny_hybrid_spatial_a_gate_fine_d_expert_v15",
        )
        self.assertIn(model.architecture, SUPPORTED_ARCHITECTURES)
        outputs = model(torch.randn(2, 4, 3, 64, 64))
        self.assertEqual([tuple(outputs[key].shape) for key in outputs],
                         [(2, 4), (2, 3), (2, 2)])
        probabilities = outputs["flat_logits"].softmax(1)
        torch.testing.assert_close(probabilities.sum(1), torch.ones(2))
        self.assertTrue(torch.isfinite(outputs["flat_logits"]).all())
        loss, _ = MultiTaskLoss([2, 3, 4, 5])(
            outputs, torch.tensor([2, 3])
        )
        loss.backward()
        for parameter in (
                model.a_gate.weight, model.bcd_head.weight,
                model.spatial_attention_fusion.token_projection[0].weight,
                model.d_fine_head.weight):
            self.assertIsNotNone(parameter.grad)
            self.assertTrue(torch.isfinite(parameter.grad).all())
            self.assertGreater(float(parameter.grad.abs().sum()), 0)

    def test_zero_initialized_adapter_preserves_a42_exactly(self):
        torch.manual_seed(42)
        a42 = self.build(fine_d_expert=False).eval()
        torch.manual_seed(42)
        a48 = self.build(fine_d_expert=True).eval()

        a42_state, a48_state = a42.state_dict(), a48.state_dict()
        self.assertEqual(
            set(a48_state) - set(a42_state),
            {key for key in a48_state if key.startswith("d_fine_")},
        )
        self.assertEqual(set(a42_state) - set(a48_state), set())
        for key, value in a42_state.items():
            torch.testing.assert_close(value, a48_state[key], rtol=0, atol=0)
        torch.testing.assert_close(
            a48.d_fine_head.weight, torch.zeros_like(a48.d_fine_head.weight),
            rtol=0, atol=0,
        )
        torch.testing.assert_close(
            a48.d_fine_head.bias, torch.zeros_like(a48.d_fine_head.bias),
            rtol=0, atol=0,
        )

        views = torch.randn(1, 4, 3, 64, 64)
        with torch.no_grad():
            expected, actual = a42(views), a48(views)
        for key in expected:
            torch.testing.assert_close(expected[key], actual[key], rtol=0, atol=0)

    def test_fine_fusion_receives_gradient_after_head_first_update(self):
        torch.manual_seed(42)
        model = self.build()
        optimizer = torch.optim.SGD(model.parameters(), lr=0.1)
        views = torch.randn(2, 4, 3, 64, 64)
        labels = torch.tensor([2, 3])

        loss, _ = MultiTaskLoss([2, 3, 4, 5])(model(views), labels)
        loss.backward()
        head_gradient = model.d_fine_head.weight.grad
        upstream_gradient = model.d_fine_fusion.token_projection[0].weight.grad
        self.assertGreater(float(head_gradient.abs().sum()), 0)
        torch.testing.assert_close(
            upstream_gradient, torch.zeros_like(upstream_gradient), rtol=0, atol=0
        )
        optimizer.step()
        optimizer.zero_grad(set_to_none=True)

        loss, _ = MultiTaskLoss([2, 3, 4, 5])(model(views), labels)
        loss.backward()
        upstream_gradient = model.d_fine_fusion.token_projection[0].weight.grad
        self.assertTrue(torch.isfinite(upstream_gradient).all())
        self.assertGreater(float(upstream_gradient.abs().sum()), 0)

    def test_d_residual_changes_only_conditional_distribution(self):
        torch.manual_seed(42)
        model = self.build().eval()
        views = torch.randn(1, 4, 3, 64, 64)
        with torch.no_grad():
            model.d_fine_head.weight.zero_()
            model.d_fine_head.bias.fill_(-8)
            negative = model(views)["flat_logits"].exp()
            model.d_fine_head.bias.fill_(8)
            positive = model(views)["flat_logits"].exp()
        torch.testing.assert_close(negative[:, 0], positive[:, 0], rtol=0, atol=0)
        self.assertGreater(float(positive[:, 3]), float(negative[:, 3]))
        torch.testing.assert_close(negative.sum(1), torch.ones(1))
        torch.testing.assert_close(positive.sum(1), torch.ones(1))

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

    def test_requires_boolean_and_a42_representation(self):
        with self.assertRaisesRegex(ValueError, "fine_d_expert must be boolean"):
            self.build(fine_d_expert=1)
        with self.assertRaisesRegex(ValueError, "Fine-scale D expert requires"):
            DensityModel(
                pretrained=False, backbone="convnext_tiny",
                fusion="hierarchical_relational", primary_head="flat",
                fine_d_expert=True,
            )
        with self.assertRaisesRegex(ValueError, "isolate_fine_d_rng must be boolean"):
            self.build(isolate_fine_d_rng=1)
        with self.assertRaisesRegex(ValueError, "RNG isolation requires"):
            self.build(fine_d_expert=False, isolate_fine_d_rng=True)

    def test_rng_isolated_arm_preserves_a42_rng_and_initial_train_output(self):
        torch.manual_seed(42)
        a42 = self.build(fine_d_expert=False).train()
        a42_construction_rng = torch.random.get_rng_state().clone()
        torch.manual_seed(42)
        a49 = self.build(
            fine_d_expert=True, isolate_fine_d_rng=True
        ).train()
        a49_construction_rng = torch.random.get_rng_state().clone()
        self.assertEqual(
            a49.architecture,
            "convnext_tiny_hybrid_spatial_a_gate_fine_d_expert_rngisolated_v16",
        )
        self.assertIn(a49.architecture, SUPPORTED_ARCHITECTURES)
        torch.testing.assert_close(
            a42_construction_rng, a49_construction_rng, rtol=0, atol=0
        )
        for key, value in a42.state_dict().items():
            torch.testing.assert_close(value, a49.state_dict()[key], rtol=0, atol=0)

        views = torch.randn(2, 4, 3, 64, 64)
        torch.manual_seed(123)
        expected = a42(views)
        expected_rng = torch.random.get_rng_state().clone()
        torch.manual_seed(123)
        actual = a49(views)
        actual_rng = torch.random.get_rng_state().clone()
        for key in expected:
            torch.testing.assert_close(expected[key], actual[key], rtol=0, atol=0)
        torch.testing.assert_close(expected_rng, actual_rng, rtol=0, atol=0)

        loss, _ = MultiTaskLoss([2, 3, 4, 5])(
            actual, torch.tensor([2, 3])
        )
        loss.backward()
        self.assertGreater(float(a49.d_fine_head.weight.grad.abs().sum()), 0)


if __name__ == "__main__":
    unittest.main()
