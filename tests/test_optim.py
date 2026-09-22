import copy
import sys
import unittest
from pathlib import Path

import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from tn_mammo.optim import build_optimizer


class OptimizerTests(unittest.TestCase):
    def model(self):
        model = torch.nn.Linear(3, 2)
        model.register_parameter("ordinal_bias", torch.nn.Parameter(torch.tensor([1., 0., -1.])))
        return model

    def test_default_is_exact_legacy_optimizer(self):
        a = self.model()
        b = copy.deepcopy(a)
        settings = dict(learning_rate=5e-5, weight_decay=1e-4)
        actual = build_optimizer(a, settings)
        legacy = torch.optim.AdamW(b.parameters(), lr=5e-5, weight_decay=1e-4)
        self.assertEqual(len(actual.param_groups), 1)
        for _ in range(3):
            for p, q in zip(a.parameters(), b.parameters()):
                p.grad = torch.ones_like(p)
                q.grad = torch.ones_like(q)
            actual.step()
            legacy.step()
        for p, q in zip(a.parameters(), b.parameters()):
            self.assertTrue(torch.equal(p, q))

    def test_only_bias_has_scaled_lr_and_cosine_preserves_ratio(self):
        model = self.model()
        opt = build_optimizer(model, dict(learning_rate=5e-5, weight_decay=1e-4,
                                         ordinal_bias_lr_multiplier=10))
        groups = opt.param_groups
        self.assertIs(groups[1]["params"][0], model.ordinal_bias)
        ids = [id(p) for g in groups for p in g["params"]]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(set(ids), {id(p) for p in model.parameters()})
        self.assertTrue(all(g["weight_decay"] == 1e-4 for g in groups))
        scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(opt, T_max=50)
        for _ in range(50):
            self.assertAlmostEqual(groups[1]["lr"], 10 * groups[0]["lr"])
            opt.step()
            scheduler.step()
        self.assertEqual(groups[0]["lr"], 0)
        self.assertEqual(groups[1]["lr"], 0)

    def test_invalid_multiplier_rejected(self):
        for value in [0, -1, float("nan"), float("inf")]:
            with self.assertRaises(ValueError):
                build_optimizer(self.model(), dict(learning_rate=5e-5,
                    weight_decay=1e-4, ordinal_bias_lr_multiplier=value))

    def test_only_backbone_has_lower_lr_and_cosine_preserves_ratio(self):
        class Model(torch.nn.Module):
            def __init__(self):
                super().__init__()
                self.features = torch.nn.Linear(3, 3)
                self.head = torch.nn.Linear(3, 2)
                self.ordinal_bias = torch.nn.Parameter(torch.tensor([1., 0., -1.]))

        model = Model()
        opt = build_optimizer(model, dict(learning_rate=5e-5, weight_decay=1e-4,
                                         backbone_lr_multiplier=0.1))
        groups = opt.param_groups
        backbone_ids = {id(p) for p in model.features.parameters()}
        self.assertEqual({id(p) for p in groups[1]["params"]}, backbone_ids)
        self.assertTrue(all(id(p) not in backbone_ids for p in groups[0]["params"]))
        ids = [id(p) for g in groups for p in g["params"]]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(set(ids), {id(p) for p in model.parameters()})
        scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(opt, T_max=50)
        for _ in range(50):
            self.assertAlmostEqual(groups[1]["lr"], 0.1 * groups[0]["lr"])
            opt.step()
            scheduler.step()
        self.assertEqual(groups[0]["lr"], 0)
        self.assertEqual(groups[1]["lr"], 0)

    def test_invalid_backbone_multiplier_rejected(self):
        for value in [0, -1, float("nan"), float("inf")]:
            with self.assertRaises(ValueError):
                build_optimizer(self.model(), dict(learning_rate=5e-5,
                    weight_decay=1e-4, backbone_lr_multiplier=value))
        with self.assertRaisesRegex(ValueError, "model.features"):
            build_optimizer(self.model(), dict(learning_rate=5e-5,
                weight_decay=1e-4, backbone_lr_multiplier=0.1))


if __name__ == "__main__":
    unittest.main()
