import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("density_folds", ROOT / "scripts/prepare_density_folds.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class DensitySplitTests(unittest.TestCase):
    def test_balance_groups_and_reproducibility(self):
        rows = [{"case_id": f"{c}{i:04d}", "label": c, "component_id": f"{c}{i:04d}"}
                for c, n in zip("ABCD", [6, 196, 1556, 259]) for i in range(n)]
        frame = pd.DataFrame(rows)
        # Mixed-label and same-label duplicate components must remain indivisible.
        frame.loc[frame.case_id.isin(["B0000", "C0000"]), "component_id"] = "mixed"
        frame.loc[frame.case_id.isin(["D0000", "D0001"]), "component_id"] = "pair"
        result = module.assign_folds(frame)
        shuffled = module.assign_folds(frame.sample(frac=1, random_state=8))
        pd.testing.assert_frame_equal(result, shuffled)
        self.assertEqual(result.groupby("component_id").fold.nunique().max(), 1)
        counts = pd.crosstab(result.fold, result.label)
        self.assertTrue(((counts.max() - counts.min()) <= 1).all())
        self.assertLessEqual(counts.sum(axis=1).max() - counts.sum(axis=1).min(), 1)
        self.assertTrue((counts > 0).all().all())
        self.assertEqual(len(result), 2017)

    def test_reject_insufficient_A_and_duplicate_cases(self):
        frame = pd.DataFrame([{"case_id": f"{c}{i}", "label": c, "component_id": f"{c}{i}"}
                              for c in "ABCD" for i in range(4)])
        with self.assertRaisesRegex(ValueError, "Every validation fold"):
            module.assign_folds(frame)
        with self.assertRaisesRegex(ValueError, "Unique cases"):
            module.assign_folds(pd.concat([frame, frame.iloc[:1]]))

    def test_outputs_preserve_sources_and_partition(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            mapping = {}
            for index, split in enumerate(module.SPLITS):
                rows = []
                for j in range(10):
                    case = f"s{index}_{j}"
                    mapping[case + "_L"] = mapping[case + "_R"] = case
                    row = {"case_id": case, "label": "ABCD"[index]}
                    for view in module.VIEWS:
                        path = root / f"{case}_{view}_a.npy"
                        path.touch()
                        row[view] = path.name
                    rows.append(row)
                pd.DataFrame(rows).to_csv(root / f"{split}.csv", index=False)
            before = {s: module.digest(root / f"{s}.csv") for s in module.SPLITS}
            registry = root / "registry.json"
            registry.write_text(json.dumps({"breast_to_component": mapping, "algorithm": "test"}))
            output = root / "new"
            assigned = module.prepare(root, registry, output)
            dev_ids = []
            for fold in range(5):
                fit = pd.read_csv(output / f"fold_{fold}/fit.csv")
                dev = pd.read_csv(output / f"fold_{fold}/dev.csv")
                self.assertFalse(set(fit.case_id) & set(dev.case_id))
                self.assertEqual(set(fit.case_id) | set(dev.case_id), set(assigned.case_id))
                self.assertEqual(dev.label.value_counts().to_dict(), dict.fromkeys("ABCD", 2))
                dev_ids.extend(dev.case_id)
            self.assertEqual(len(dev_ids), len(set(dev_ids)))
            self.assertEqual(before, {s: module.digest(root / f"{s}.csv") for s in module.SPLITS})
            with self.assertRaises(FileExistsError):
                module.prepare(root, registry, output)
            launch_spec = importlib.util.spec_from_file_location(
                "density_launch", ROOT / "scripts/train_density_fold.py")
            launch = importlib.util.module_from_spec(launch_spec)
            launch_spec.loader.exec_module(launch)
            config, paths = launch.configure(ROOT / "configs/vindr_cache_5090_full50.yaml", output, 0)
            self.assertEqual(config["experiment"]["fold"], 0)
            self.assertEqual(config["training"]["min_epochs"], 50)
            self.assertEqual(config["wandb"]["group"], "vindr-densityCV5-v1-seed42-full50")
            dev = pd.read_csv(paths[1])
            dev.loc[0, "label"] = "D" if dev.loc[0, "label"] != "D" else "A"
            dev.to_csv(paths[1], index=False)
            with self.assertRaisesRegex(ValueError, "manifest differs"):
                launch.configure(ROOT / "configs/vindr_cache_5090_full50.yaml", output, 0)
