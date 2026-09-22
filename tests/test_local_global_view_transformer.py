import io
import sys
from pathlib import Path
import unittest

import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from tn_mammo.model import DensityModel, LocalGlobalViewTokenFusion
from tn_mammo.engine import SUPPORTED_ARCHITECTURES
from tn_mammo.loss import MultiTaskLoss


class LocalGlobalTests(unittest.TestCase):
    def fusion(self):
        return LocalGlobalViewTokenFusion(
            fine_dim=8, coarse_dim=16, token_dim=16, heads=4, layers=1,
            fine_grid_size=2, coarse_grid_size=1,
        )

    def maps(self):
        return torch.randn(2, 4, 8, 4, 4), torch.randn(2, 4, 16, 2, 2)

    def test_local_independence_and_global_sensitivity(self):
        torch.manual_seed(42)
        fusion = self.fusion().eval()
        fine, coarse = self.maps()
        changed = fine.clone()
        changed[:, 1] += 10
        with torch.no_grad():
            a = fusion.summarize_views(fine, coarse)
            b = fusion.summarize_views(changed, coarse)
            torch.testing.assert_close(a[:, [0, 2, 3]], b[:, [0, 2, 3]], rtol=0, atol=0)
            self.assertGreater(float((a[:, 1] - b[:, 1]).abs().max()), 1e-5)
            self.assertGreater(float((fusion(fine, coarse) - fusion(changed, coarse)).abs().max()), 1e-5)

    def test_masked_views_cannot_change_output(self):
        fusion = self.fusion().eval()
        fine, coarse = self.maps()
        mask = torch.tensor([[1, 0, 1, 0], [0, 1, 0, 0]], dtype=torch.bool)
        with torch.no_grad():
            expected = fusion(fine, coarse, mask)
            changed_fine, changed_coarse = fine.clone(), coarse.clone()
            changed_fine[~mask] = float('nan')
            changed_coarse[~mask] = 10000
            torch.testing.assert_close(expected, fusion(changed_fine, changed_coarse, mask), rtol=0, atol=0)
        with self.assertRaisesRegex(ValueError, 'at least one view'):
            fusion(fine, coarse, torch.zeros_like(mask))
        with self.assertRaisesRegex(ValueError, 'shape'):
            fusion(fine, coarse, mask[:, :3])
        with self.assertRaisesRegex(ValueError, 'aligned'):
            fusion(fine[:, :3], coarse)

    def test_gradients_and_adapter_warm_start(self):
        fusion = self.fusion()
        fine, coarse = self.maps()
        optimizer = torch.optim.SGD(fusion.parameters(), lr=0.01)
        fusion(fine, coarse).square().mean().backward()
        parameters = [fusion.fine_projection.weight, fusion.coarse_projection.weight,
                      fusion.local_encoder.layers[0].self_attn.in_proj_weight,
                      fusion.encoder.layers[0].self_attn.in_proj_weight,
                      fusion.view_token, fusion.exam_token]
        adapters = list(fusion.type_adapters) + list(fusion.side_adapters)
        parameters += [adapter[-1].weight for adapter in adapters]
        for parameter in parameters:
            self.assertIsNotNone(parameter.grad)
            self.assertTrue(torch.isfinite(parameter.grad).all())
            self.assertGreater(float(parameter.grad.abs().sum()), 0)
        # Zero output weights intentionally block the down projection only on
        # the first backward. It must start learning after the first update.
        optimizer.step()
        optimizer.zero_grad()
        fusion(fine, coarse).square().mean().backward()
        for adapter in adapters:
            self.assertGreater(float(adapter[0].weight.grad.abs().sum()), 0)

    def test_full_model_roundtrip_and_output(self):
        def build():
            return DensityModel(pretrained=False, backbone='convnext_tiny',
                                fusion='local_global_view_attention',
                                primary_head='a_gate_hierarchical', attention_dim=32,
                                attention_heads=4, attention_layers=1, spatial_grid_size=2)
        model = build()
        self.assertIn(model.architecture, SUPPORTED_ARCHITECTURES)
        self.assertTrue(model.architecture.endswith('_v11'))
        self.assertFalse(hasattr(model, 'pair_fusion'))
        views = torch.randn(2, 4, 3, 64, 64)
        output = model(views)
        torch.testing.assert_close(output['flat_logits'].softmax(1).sum(1), torch.ones(2))
        loss, _ = MultiTaskLoss([5, 157, 1244, 208])(output, torch.tensor([0, 3]))
        loss.backward()
        self.assertGreater(float(model.features[0][0].weight.grad.abs().sum()), 0)
        self.assertGreater(float(model.a_gate.weight.grad.abs().sum()), 0)
        model.eval()
        stream = io.BytesIO()
        torch.save(model.state_dict(), stream)
        stream.seek(0)
        restored = build().eval()
        restored.load_state_dict(torch.load(stream, weights_only=True), strict=True)
        with torch.no_grad():
            expected = model(views)
            for key, value in expected.items():
                torch.testing.assert_close(value, model(views)[key], rtol=0, atol=0)
                torch.testing.assert_close(value, restored(views)[key], rtol=0, atol=0)


if __name__ == '__main__':
    unittest.main()
