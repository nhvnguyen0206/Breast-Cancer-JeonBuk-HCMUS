import unittest

import torch
from torch.nn import functional as F

from tn_mammo.loss import MultiTaskLoss


class BinaryNormalizationTests(unittest.TestCase):
    def setUp(self):
        torch.manual_seed(42)
        self.counts = [5, 156, 1245, 207]
        self.labels = torch.tensor([0, 1, 2, 3, 2])
        self.outputs = {name: torch.randn(5, size, requires_grad=True)
                        for name, size in [('flat_logits', 4), ('ordinal_logits', 3),
                                           ('binary_logits', 2)]}

    def test_legacy_default_and_auxiliary_parity(self):
        old = MultiTaskLoss(self.counts)
        explicit = MultiTaskLoss(self.counts, binary_normalization='batch_weight_mean')
        new = MultiTaskLoss(self.counts, binary_normalization='train_expectation')
        total, parts = old(self.outputs, self.labels)
        explicit_total, _ = explicit(self.outputs, self.labels)
        self.assertTrue(torch.equal(total, explicit_total))
        expected = F.cross_entropy(self.outputs['binary_logits'],
                                   (self.labels >= 2).long(), weight=old.binary_weights)
        self.assertTrue(torch.equal(parts['binary'], expected.detach()))
        new_total, new_parts = new(self.outputs, self.labels)
        for name in ['focal', 'ordinal', 'neighbor']:
            self.assertTrue(torch.equal(parts[name], new_parts[name]))
        torch.testing.assert_close(new_total-total, .3*(new_parts['binary']-parts['binary']))
        new_total.backward()
        for value in self.outputs.values():
            self.assertTrue(torch.isfinite(value.grad).all())

    def test_fixed_objective_partition_invariance_and_formula(self):
        loss = MultiTaskLoss(self.counts, binary_normalization='train_expectation')
        _, full = loss(self.outputs, self.labels)
        chunks = []
        for start, end in [(0, 2), (2, 4), (4, 5)]:
            _, parts = loss({k: v[start:end] for k, v in self.outputs.items()},
                            self.labels[start:end])
            chunks.append((end-start)*parts['binary'])
        torch.testing.assert_close(sum(chunks)/5, full['binary'])
        frequencies = torch.tensor([161., 1452.])/1613
        denominator = (frequencies*loss.binary_weights).sum()
        expected = F.cross_entropy(self.outputs['binary_logits'],
                                   (self.labels >= 2).long(), weight=loss.binary_weights,
                                   reduction='none').mean()/denominator
        torch.testing.assert_close(expected.detach(), full['binary'])

    def test_invalid_mode(self):
        with self.assertRaisesRegex(ValueError, 'binary_normalization'):
            MultiTaskLoss(self.counts, binary_normalization='unknown')


if __name__ == '__main__':
    unittest.main()
