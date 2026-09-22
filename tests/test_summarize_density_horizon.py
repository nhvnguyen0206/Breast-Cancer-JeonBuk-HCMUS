import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from summarize_density_horizon import read_history, summarize


def record(epoch, score):
    return {"epoch": epoch, "valid": {
        "macro_f1": score, "accuracy": score + 0.1, "qwk": score - 0.1,
        "per_class_f1": [score] * 4,
        "confusion_matrix": [[1, 0, 0, 0]] * 4,
    }}


class HorizonSummaryTests(unittest.TestCase):
    def test_json_history_and_log_have_same_common_horizon_summary(self):
        with tempfile.TemporaryDirectory() as directory:
            directory = Path(directory)
            history = [record(1, 0.6), record(2, 0.72), record(3, 0.5)]
            json_path = directory / "history.json"
            json_path.write_text(json.dumps(history))
            log_path = directory / "train.log"
            log_path.write_text("startup\n" + "\n".join(json.dumps(row) for row in history))
            result = summarize({0: json_path, 1: log_path}, 2)
            self.assertEqual([row["selected_epoch"] for row in result["folds"]], [2, 2])
            self.assertAlmostEqual(result["aggregate"]["macro_f1_mean"], 0.72)
            self.assertAlmostEqual(result["aggregate"]["accuracy_mean"], 0.82)
            self.assertAlmostEqual(result["aggregate"]["qwk_mean"], 0.62)
            self.assertEqual(result["aggregate"]["per_class_f1_mean"], [0.72] * 4)
            self.assertAlmostEqual(result["aggregate"]["bcd_f1_mean"], 0.72)
            self.assertTrue(result["aggregate"]["mean_gate_met"])
            self.assertTrue(result["aggregate"]["minimum_gate_met"])

    def test_rejects_incomplete_epoch_sequence_or_horizon(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "history.json"
            path.write_text(json.dumps([record(1, 0.5), record(3, 0.7)]))
            with self.assertRaisesRegex(ValueError, "incomplete"):
                read_history(path)
            path.write_text(json.dumps([record(1, 0.5)]))
            with self.assertRaisesRegex(ValueError, "has not completed"):
                summarize({0: path, 1: path}, 2)

    def test_current_and_historical_thresholds_are_explicit(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "history.json"
            path.write_text(json.dumps([record(1, 0.71)]))
            current = summarize({0: path, 1: path}, 1)
            self.assertFalse(current["aggregate"]["mean_gate_met"])
            self.assertTrue(current["aggregate"]["sample_sd_gate_met"])
            old = summarize({0: path, 1: path}, 1, mean_threshold=.70, sd_threshold=.05)
            self.assertTrue(old["aggregate"]["mean_gate_met"])
            self.assertEqual(current["criteria"]["sample_sd_threshold"], .03)
            self.assertEqual(old["criteria"]["mean_threshold"], .70)
            other = Path(directory) / "other.log"
            other.write_text(json.dumps(record(1, .79)))
            result = summarize({0: path, 1: other}, 1)
            self.assertTrue(result["aggregate"]["mean_gate_met"])
            self.assertFalse(result["aggregate"]["sample_sd_gate_met"])
            with self.assertRaisesRegex(ValueError, "Thresholds"):
                summarize({0: path, 1: path}, 1, sd_threshold=float('nan'))


if __name__ == "__main__":
    unittest.main()
