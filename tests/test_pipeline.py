import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import numpy as np
import pandas as pd
import pydicom
from pydicom.dataset import FileDataset, FileMetaDataset
from pydicom.uid import ExplicitVRLittleEndian, SecondaryCaptureImageStorage, generate_uid
import torch
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from tn_mammo.data import FourViewDataset, VIEWS, assert_disjoint
from tn_mammo.engine import load_model, metrics, train
from tn_mammo.model import DensityModel
from tn_mammo.loss import MultiTaskLoss

torch.set_num_threads(2)


def make_manifest(root, name, labeled=True):
    rows = []
    for index, label in enumerate("ABCD"):
        row = {"case_id": f"{name}-{index}"}
        if labeled:
            row["label"] = label
        for view in VIEWS:
            path = root / f"{name}-{index}-{view}.dcm"
            meta = FileMetaDataset()
            meta.TransferSyntaxUID = ExplicitVRLittleEndian
            meta.MediaStorageSOPClassUID = SecondaryCaptureImageStorage
            meta.MediaStorageSOPInstanceUID = generate_uid()
            ds = FileDataset(str(path), {}, file_meta=meta, preamble=b"\0" * 128)
            ds.SOPClassUID = meta.MediaStorageSOPClassUID
            ds.SOPInstanceUID = meta.MediaStorageSOPInstanceUID
            ds.Rows, ds.Columns = 64, 48
            ds.SamplesPerPixel = 1
            ds.PhotometricInterpretation = "MONOCHROME1" if view.startswith("R") else "MONOCHROME2"
            ds.BitsAllocated, ds.BitsStored, ds.HighBit, ds.PixelRepresentation = 16, 12, 11, 0
            pixels = np.random.default_rng(index).integers(0, 4096, (64, 48), dtype=np.uint16)
            ds.PixelData = pixels.tobytes()
            ds.save_as(path, enforce_file_format=True)
            row[view] = path.name
        rows.append(row)
    manifest = root / f"{name}.csv"
    pd.DataFrame(rows).to_csv(manifest, index=False)
    return manifest


class PipelineTests(unittest.TestCase):
    def test_model_heads_loss_backward_and_512_forward(self):
        model = DensityModel(pretrained=False)
        outputs = model(torch.randn(1, 4, 3, 64, 64))
        self.assertEqual([tuple(outputs[k].shape) for k in outputs], [(1, 4), (1, 3), (1, 2)])
        loss, parts = MultiTaskLoss([2, 3, 4, 5])(outputs, torch.tensor([2]))
        self.assertTrue(torch.isfinite(loss))
        self.assertEqual(set(parts), {"focal", "ordinal", "binary", "neighbor"})
        loss.backward()
        for name in ("flat_head", "ordinal_score", "binary_head", "side_gate"):
            grad = getattr(model, name).weight.grad
            self.assertTrue(torch.isfinite(grad).all())
            self.assertGreater(float(grad.abs().sum()), 0)
        model.eval()
        with torch.inference_mode():
            result = model(torch.randn(1, 4, 3, 512, 512))
        self.assertTrue(torch.isfinite(result["flat_logits"]).all())
        # Flat-head decoder and all four classes remain defined even on a tiny subset.
        self.assertEqual(metrics([0, 0], [0, 1])["macro_f1"], 1 / 6)

    def test_manifest_validation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = make_manifest(root, "train")
            data = FourViewDataset(manifest, 64)
            self.assertEqual(tuple(data[0]["views"].shape), (4, 3, 64, 64))
            self.assertTrue(torch.isfinite(data[0]["views"]).all())
            with self.assertRaisesRegex(ValueError, "case overlap"):
                assert_disjoint(data, data)
            frame = pd.read_csv(manifest)
            frame.case_id = [f"renamed-{i}" for i in range(4)]
            other = root / "other.csv"
            frame.to_csv(other, index=False)
            with self.assertRaisesRegex(ValueError, "image overlap"):
                assert_disjoint(data, FourViewDataset(other, 64))
            frame.loc[0, "label"] = "invalid"
            frame.to_csv(other, index=False)
            with self.assertRaisesRegex(ValueError, "label"):
                FourViewDataset(other, 64)

    def test_training_checkpoint_and_inference_cli(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            config = yaml.safe_load((ROOT / "configs/train.yaml").read_text())
            config = copy.deepcopy(config)
            config["image_size"] = 64
            config["model"]["pretrained"] = False
            config["training"].update(epochs=1, batch_size=2, num_workers=0, amp=False)
            train_manifest = make_manifest(root, "train")
            valid_manifest = make_manifest(root, "valid")
            output = root / "run"
            train(config, train_manifest, valid_manifest, output, torch.device("cpu"))
            model, saved_config = load_model(output / "best.pt", torch.device("cpu"))
            self.assertEqual(saved_config, config)
            self.assertEqual(len(json.loads((output / "history.json").read_text())), 1)
            checkpoint = torch.load(output / "best.pt", weights_only=True)
            self.assertEqual(checkpoint["class_counts"], [1, 1, 1, 1])
            x = FourViewDataset(valid_manifest, 64)[0]["views"].unsqueeze(0)
            with torch.inference_mode():
                expected = model(x)["flat_logits"].softmax(1)[0].numpy()
            unlabeled = root / "unlabeled.csv"
            pd.read_csv(valid_manifest).drop(columns="label").to_csv(unlabeled, index=False)
            # Execute the public inference entrypoint with and without labels.
            for manifest, name in ((valid_manifest, "labeled"), (unlabeled, "unlabeled")):
                result = subprocess.run([
                    sys.executable, str(ROOT / "inference.py"), "--checkpoint", str(output / "best.pt"),
                    "--manifest", str(manifest), "--output-dir", str(root / name), "--device", "cpu",
                ], capture_output=True, text=True, timeout=90,
                    env={**__import__("os").environ, "OMP_NUM_THREADS": "2", "MKL_NUM_THREADS": "2"})
                self.assertEqual(result.returncode, 0, result.stderr)
                frame = pd.read_csv(root / name / "predictions.csv")
                probabilities = frame[[f"prob_{c}" for c in "ABCD"]].to_numpy()
                np.testing.assert_allclose(probabilities.sum(1), 1, atol=1e-6)
                np.testing.assert_allclose(probabilities[0], expected, atol=1e-6)
                self.assertEqual((root / name / "metrics.json").exists(), name == "labeled")


if __name__ == "__main__":
    unittest.main()
