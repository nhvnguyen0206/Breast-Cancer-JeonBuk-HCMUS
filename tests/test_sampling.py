import sys
from pathlib import Path
import unittest
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from tn_mammo.sampling import training_sampler


class SamplingTests(unittest.TestCase):
    def test_natural_tempered_and_balanced_probabilities(self):
        counts = np.array([5, 156, 1245, 207])
        labels = np.repeat(np.arange(4), counts)
        natural, p = training_sampler(labels, 0, 42)
        self.assertIsNone(natural)
        np.testing.assert_allclose(p, counts / counts.sum())
        sampler, p = training_sampler(labels, .5, 42)
        np.testing.assert_allclose(p, np.sqrt(counts) / np.sqrt(counts).sum())
        self.assertEqual(sampler.num_samples, len(labels))
        self.assertTrue(sampler.replacement)
        draws = list(sampler)
        other, _ = training_sampler(labels, .5, 42)
        self.assertEqual(draws, list(other))
        self.assertTrue(all(0 <= i < len(labels) for i in draws))
        _, p = training_sampler(labels, 1, 42)
        np.testing.assert_allclose(p, [.25] * 4)

    def test_invalid_configuration(self):
        for labels, power in [([], .5), ([0, 1, 2], .5), ([0, 1, 2, 4], .5),
                              ([0, 1, 2, 3], -1), ([0, 1, 2, 3], float("nan"))]:
            with self.assertRaises(ValueError):
                training_sampler(labels, power, 42)
