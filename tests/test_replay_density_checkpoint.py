import sys
from pathlib import Path
import unittest
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from replay_density_checkpoint import compare_predictions


class ReplayComparisonTests(unittest.TestCase):
    def frame(self):
        return pd.DataFrame([
            dict(case_id='one', true_index=0, pred_index=0, pred_label='A',
                 prob_A=.7, prob_B=.1, prob_C=.1, prob_D=.1),
            dict(case_id='two', true_index=1, pred_index=1, pred_label='B',
                 prob_A=.1, prob_B=.7, prob_C=.1, prob_D=.1)])

    def test_reordering_is_accepted(self):
        a = self.frame()
        result = compare_predictions(a, a.iloc[::-1])
        self.assertEqual(result['max_probability_abs_error'], 0)

    def test_rejects_membership_labels_and_probability_corruption(self):
        a = self.frame()
        for change in ('id', 'duplicate', 'label', 'probabilities', 'nan'):
            b = a.copy()
            if change == 'id':
                b.loc[0, 'case_id'] = 'different'
            elif change == 'duplicate':
                b.loc[0, 'case_id'] = 'two'
            elif change == 'label':
                b.loc[0, 'pred_index'] = 1
            elif change == 'probabilities':
                b.loc[0, ['prob_A', 'prob_B']] = [.6, .2]
            else:
                b.loc[0, 'prob_A'] = float('nan')
            with self.subTest(change=change), self.assertRaises(ValueError):
                compare_predictions(a, b)


if __name__ == '__main__':
    unittest.main()
