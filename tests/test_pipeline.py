import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import numpy as np
import pandas as pd
import pydicom
from pydicom.dataset import FileDataset, FileMetaDataset
from pydicom.uid import ExplicitVRLittleEndian, SecondaryCaptureImageStorage, generate_uid
import torch
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from tn_mammo.data import (FourViewDataset, VIEWS, assert_disjoint, augment_views,
                           read_cache, resize_cache)
from tn_mammo.engine import load_model, metrics, predict, set_training_phase, train
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
    def test_geometric_augmentation_is_shared_across_four_views(self):
        image = torch.linspace(0, 1, 64 * 64).reshape(1, 1, 64, 64)
        views = image.repeat(4, 3, 1, 1)
        torch.manual_seed(42)
        result = augment_views(views, {"brightness_min": 1.0, "brightness_max": 1.0,
                                       "rotation_degrees": 5.0,
                                       "translation_fraction": 0.03})
        self.assertEqual(result.shape, views.shape)
        self.assertTrue(torch.isfinite(result).all())
        self.assertGreaterEqual(float(result.min()), 0.0)
        self.assertLessEqual(float(result.max()), 1.0)
        for index in range(1, 4):
            torch.testing.assert_close(result[0], result[index])
        self.assertFalse(torch.equal(result, views))
        with self.assertRaisesRegex(ValueError, "Unknown augmentation"):
            augment_views(views, {"horizontal_flip": True})
        with self.assertRaisesRegex(ValueError, "Invalid augmentation"):
            augment_views(views, {"rotation_degrees": 20})

    def test_backbone_warmup_freezes_weights_and_bn_then_unfreezes(self):
        model = DensityModel(pretrained=False)
        optimizer = torch.optim.AdamW(model.parameters(), lr=1e-4)
        before = {k: v.clone() for k, v in model.features.state_dict().items()}
        head_before = model.flat_head.weight.detach().clone()
        self.assertTrue(set_training_phase(model, 1, 1))
        self.assertFalse(model.features.training)
        self.assertTrue(model.flat_head.training)
        batch = torch.randn(2, 4, 3, 64, 64)
        model(batch)["flat_logits"].square().mean().backward()
        self.assertTrue(all(p.grad is None for p in model.features.parameters()))
        optimizer.step()
        self.assertTrue(all(torch.equal(before[k], v) for k, v in model.features.state_dict().items()))
        self.assertFalse(torch.equal(head_before, model.flat_head.weight))
        optimizer.zero_grad(set_to_none=True)
        self.assertFalse(set_training_phase(model, 2, 1))
        self.assertTrue(model.features.training)
        model(batch)["flat_logits"].square().mean().backward()
        self.assertTrue(all(p.grad is not None and torch.isfinite(p.grad).all()
                            for p in model.features.parameters()))
        optimizer.step()
        self.assertFalse(torch.equal(before["conv0.weight"], model.features.conv0.weight))
        self.assertFalse(torch.equal(before["norm0.running_mean"], model.features.norm0.running_mean))
        self.assertFalse(set_training_phase(model, 1))

    def test_backbone_batchnorm_statistics_can_stay_fixed_during_finetuning(self):
        model = DensityModel(pretrained=False)
        optimizer = torch.optim.AdamW(model.parameters(), lr=1e-4)
        conv_before = model.features.conv0.weight.detach().clone()
        mean_before = model.features.norm0.running_mean.detach().clone()
        self.assertFalse(set_training_phase(
            model, 1, freeze_backbone_batchnorm=True))
        self.assertTrue(model.features.training)
        batchnorms = [module for module in model.features.modules()
                      if isinstance(module, torch.nn.modules.batchnorm._BatchNorm)]
        self.assertEqual(len(batchnorms), 121)
        self.assertTrue(all(not module.training for module in batchnorms))
        self.assertTrue(model.features.norm0.weight.requires_grad)
        batch = torch.randn(2, 4, 3, 64, 64)
        model(batch)["flat_logits"].square().mean().backward()
        optimizer.step()
        self.assertFalse(torch.equal(conv_before, model.features.conv0.weight))
        self.assertTrue(torch.equal(mean_before, model.features.norm0.running_mean))

    def test_focal_fit_expectation_normalization(self):
        counts = [5, 156, 1245, 207]
        old = MultiTaskLoss(counts)
        new = MultiTaskLoss(counts, focal_normalization="train_expectation")
        outputs = {"flat_logits": torch.randn(4, 4, requires_grad=True),
                   "ordinal_logits": torch.randn(4, 3, requires_grad=True),
                   "binary_logits": torch.randn(4, 2, requires_grad=True)}
        labels = torch.arange(4)
        a, pa = old(outputs, labels)
        b, pb = new(outputs, labels)
        denominator = (old.weights * torch.tensor(counts) / sum(counts)).sum()
        torch.testing.assert_close(pb["focal"], pa["focal"] / denominator)
        for key in ("ordinal", "binary", "neighbor"):
            torch.testing.assert_close(pa[key], pb[key])
        torch.testing.assert_close(b - a, pb["focal"] - pa["focal"])
        b.backward()
        self.assertTrue(torch.isfinite(outputs["flat_logits"].grad).all())
        self.assertEqual(old.focal_denominator, 1.0)
        with self.assertRaises(ValueError):
            MultiTaskLoss(counts, focal_normalization="batch")

    def test_focal_label_smoothing_is_opt_in_and_finite(self):
        counts = [5, 156, 1245, 207]
        outputs = {"flat_logits": torch.tensor([
                       [12.0, -4.0, -4.0, -4.0], [-5.0, 8.0, 1.0, -3.0]],
                       requires_grad=True),
                   "ordinal_logits": torch.randn(2, 3, requires_grad=True),
                   "binary_logits": torch.randn(2, 2, requires_grad=True)}
        labels = torch.tensor([0, 1])
        default = MultiTaskLoss(counts)
        explicit_zero = MultiTaskLoss(counts, label_smoothing=0.0)
        smoothed = MultiTaskLoss(counts, label_smoothing=0.05)
        loss_default, parts_default = default(outputs, labels)
        loss_zero, parts_zero = explicit_zero(outputs, labels)
        loss_smooth, parts_smooth = smoothed(outputs, labels)
        torch.testing.assert_close(loss_default, loss_zero, rtol=0, atol=0)
        for key in parts_default:
            torch.testing.assert_close(parts_default[key], parts_zero[key], rtol=0, atol=0)
        self.assertFalse(torch.equal(parts_default["focal"], parts_smooth["focal"]))
        for key in ("ordinal", "binary", "neighbor"):
            torch.testing.assert_close(parts_default[key], parts_smooth[key])
        self.assertTrue(torch.isfinite(loss_smooth))
        loss_smooth.backward()
        self.assertTrue(torch.isfinite(outputs["flat_logits"].grad).all())
        for invalid in (-0.01, 1.0):
            with self.assertRaisesRegex(ValueError, "label_smoothing"):
                MultiTaskLoss(counts, label_smoothing=invalid)

    def test_focal_scale_is_opt_in_and_scales_only_primary_loss(self):
        counts = [5, 156, 1245, 207]
        outputs = {"flat_logits": torch.randn(4, 4, requires_grad=True),
                   "ordinal_logits": torch.randn(4, 3, requires_grad=True),
                   "binary_logits": torch.randn(4, 2, requires_grad=True)}
        labels = torch.arange(4)
        default = MultiTaskLoss(counts)
        explicit = MultiTaskLoss(counts, focal_scale=1.0)
        doubled = MultiTaskLoss(counts, focal_scale=2.0)
        base_loss, base_parts = default(outputs, labels)
        explicit_loss, explicit_parts = explicit(outputs, labels)
        scaled_loss, scaled_parts = doubled(outputs, labels)
        torch.testing.assert_close(base_loss, explicit_loss, rtol=0, atol=0)
        for key in base_parts:
            torch.testing.assert_close(base_parts[key], explicit_parts[key], rtol=0, atol=0)
        torch.testing.assert_close(scaled_parts["focal"], 2 * base_parts["focal"])
        for key in ("ordinal", "binary", "neighbor"):
            torch.testing.assert_close(base_parts[key], scaled_parts[key])
        torch.testing.assert_close(scaled_loss - base_loss, base_parts["focal"])
        scaled_loss.backward()
        self.assertTrue(torch.isfinite(outputs["flat_logits"].grad).all())
        for invalid in (0, -1, float("inf"), float("nan")):
            with self.assertRaisesRegex(ValueError, "focal_scale"):
                MultiTaskLoss(counts, focal_scale=invalid)

    def test_letterbox_geometry_and_backward_compatibility(self):
        import cv2
        image = np.arange(8, dtype=np.float32).reshape(4, 2) / 8
        padded = resize_cache(image, 8, "letterbox")
        self.assertEqual(padded.shape, (8, 8))
        np.testing.assert_array_equal(padded[:, :2], 0)
        np.testing.assert_array_equal(padded[:, 6:], 0)
        np.testing.assert_array_equal(padded[:, 2:6], cv2.resize(image, (4, 8), interpolation=cv2.INTER_AREA))
        np.testing.assert_array_equal(resize_cache(image, 8), cv2.resize(image, (8, 8), interpolation=cv2.INTER_AREA))
        np.testing.assert_array_equal(resize_cache(image.T, 8, "letterbox"), padded.T)

    def test_letterbox_cache_train_and_inference(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for split in ("fit", "dev"):
                rows = []
                for i, c in enumerate("ABCD"):
                    row = {"case_id": f"{split}_{c}", "label": c}
                    for view in VIEWS:
                        prefix = root / f"{split}_{c}_{view}"
                        values = np.random.default_rng(i).uniform(.1, .9, (64, 32)).astype(np.float32)
                        np.save(str(prefix) + "_a.npy", values)
                        np.save(str(prefix) + "_s.npy", np.array(values.shape, dtype=np.int32))
                        np.save(str(prefix) + "_m.npy", np.packbits(np.ones(values.shape, dtype=bool)))
                        row[view] = str(prefix) + "_a.npy"
                    rows.append(row)
                pd.DataFrame(rows).to_csv(root / f"{split}.csv", index=False)
            config = yaml.safe_load((ROOT / "configs/vindr_density_letterbox.yaml").read_text())
            config["image_size"] = 64
            config["model"]["pretrained"] = False
            config["training"].update(epochs=1, min_epochs=1, num_workers=0, amp=False,
                                      sampling_power=0.5)
            train(config, root / "fit.csv", root / "dev.csv", root / "run", torch.device("cpu"))
            history = json.loads((root / "run/history.json").read_text())
            self.assertEqual(sum(history[0]["sampled_class_counts"]), 4)
            self.assertEqual(history[0]["valid"]["num_samples"], 4)
            result = subprocess.run([sys.executable, str(ROOT / "inference.py"),
                "--checkpoint", str(root / "run/best.pt"), "--manifest", str(root / "dev.csv"),
                "--output-dir", str(root / "pred"), "--device", "cpu"],
                capture_output=True, text=True, timeout=90,
                env={**__import__("os").environ, "OMP_NUM_THREADS": "2", "MKL_NUM_THREADS": "2"})
            self.assertEqual(result.returncode, 0, result.stderr)
            a = pd.read_csv(root / "run/valid_predictions.csv")
            b = pd.read_csv(root / "pred/predictions.csv")
            np.testing.assert_allclose(a[[f"prob_{c}" for c in "ABCD"]],
                                       b[[f"prob_{c}" for c in "ABCD"]], atol=1e-6)
            model, _ = load_model(root / "run/best.pt", torch.device("cpu"))
            dataset = FourViewDataset(root / "dev.csv", 64,
                                      input_mode="window16_cache", resize_mode="letterbox")
            results, rng_states = [], []
            for workers in (0, 2):
                torch.manual_seed(42)
                results.append(predict(model, torch.utils.data.DataLoader(
                    dataset, batch_size=2, num_workers=workers), torch.device("cpu")))
                rng_states.append(torch.get_rng_state())
            pd.testing.assert_frame_equal(results[0], results[1])
            self.assertTrue(torch.equal(*rng_states))

    def test_early_stopping_respects_min_epochs(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            config = yaml.safe_load((ROOT / "configs/train.yaml").read_text())
            config["image_size"] = 64
            config["model"]["pretrained"] = False
            config["training"].update(epochs=4, min_epochs=3, patience=1,
                                        batch_size=2, num_workers=0, amp=False)
            fixed = metrics([0, 1, 2, 3], [0, 1, 2, 3])
            with patch("tn_mammo.engine.metrics", return_value=fixed):
                train(config, make_manifest(root, "fit"), make_manifest(root, "dev"),
                      root / "run", torch.device("cpu"))
            history = json.loads((root / "run/history.json").read_text())
            self.assertEqual(len(history), 3)
            self.assertEqual(torch.load(root / "run/best.pt", weights_only=True)["epoch"], 1)

    def test_vindr_preparation_preserves_density_and_split(self):
        spec = importlib.util.spec_from_file_location("prepare_vindr", ROOT / "scripts/prepare_vindr.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            records, annotations = [], []
            for study in ("complete", "conflicting", "incomplete"):
                folder = root / "tensor_cache" / study
                folder.mkdir(parents=True)
                for view in (VIEWS[:2] if study == "incomplete" else VIEWS):
                    side, position = view.split("_")
                    records.append({"study": study, "image": view})
                    annotations.append({"study_id": study, "image_id": view,
                                        "laterality": side, "view_position": position,
                                        "breast_density": "DENSITY D" if study == "conflicting" and side == "R" else "DENSITY B",
                                        "breast_birads": "BI-RADS 5"})
                    for suffix in ("_a.npy", "_m.npy", "_s.npy"):
                        np.save(folder / (view + suffix), np.array([0]))
            (root / "_images.jsonl").write_text("\n".join(json.dumps(r) for r in records))
            (root / "_input_provenance.json").write_text("{}")
            annotation_path = root / "annotations.csv"
            pd.DataFrame(annotations).to_csv(annotation_path, index=False)
            protocol = root / "protocol.json"
            protocol.write_text(json.dumps({"sets": {"fit": ["complete_L", "complete_R"]}}))
            module.prepare(root, annotation_path, protocol, root / "prepared")
            result = pd.read_csv(root / "prepared/fit.csv")
            self.assertEqual(result.label.tolist(), ["B"])
            self.assertEqual(result.case_id.tolist(), ["complete"])
            audit = json.loads((root / "prepared/audit.json").read_text())
            self.assertEqual(audit["complete_consistent_studies"], 1)
            self.assertEqual(sum(audit["exclusions"].values()), 2)
            protocol.write_text(json.dumps({"sets": {"fit": ["complete_L"], "dev": ["complete_R"]}}))
            with self.assertRaisesRegex(ValueError, "inconsistent split"):
                module.prepare(root, annotation_path, protocol, root / "invalid")

    def test_frozen_cache_scale_and_explicit_mask(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            pixels = np.array([[0., .5], [1., 0.]], dtype=np.float32)
            mask = np.array([[True, True], [True, False]])
            np.save(root / "image_a.npy", pixels)
            np.save(root / "image_s.npy", np.array([2, 2], dtype=np.int32))
            np.save(root / "image_m.npy", np.packbits(mask, bitorder="big"))
            actual = read_cache(root / "image_a.npy", 2)
            np.testing.assert_array_equal(actual[0].numpy(), pixels)
            self.assertEqual(tuple(actual.shape), (3, 2, 2))
            pixels[1, 1] = .2
            np.save(root / "image_a.npy", pixels)
            with self.assertRaisesRegex(ValueError, "Invalid cache pixels"):
                read_cache(root / "image_a.npy", 2)
            np.save(root / "image_m.npy", np.array([], dtype=np.uint8))
            with self.assertRaisesRegex(ValueError, "Invalid packed mask"):
                read_cache(root / "image_a.npy", 2)

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

    def test_view_token_attention_fusion_shapes_gradients_and_identity(self):
        model = DensityModel(
            pretrained=False, dropout=0.4, fusion="view_token_attention",
            attention_dim=64, attention_heads=4, attention_layers=2,
            attention_dropout=0.1,
        )
        self.assertEqual(model.architecture,
                         "densenet121_view_token_attention_multitask_v2")
        self.assertFalse(hasattr(model, "pair_fusion"))
        outputs = model(torch.randn(2, 4, 3, 64, 64))
        self.assertEqual([tuple(outputs[k].shape) for k in outputs],
                         [(2, 4), (2, 3), (2, 2)])
        loss, _ = MultiTaskLoss([2, 3, 4, 5])(outputs, torch.tensor([0, 3]))
        loss.backward()
        for parameter in (model.attention_fusion.exam_token,
                          model.attention_fusion.view_type_embedding,
                          model.attention_fusion.laterality_embedding):
            self.assertIsNotNone(parameter.grad)
            self.assertTrue(torch.isfinite(parameter.grad).all())
            self.assertGreater(float(parameter.grad.abs().sum()), 0)
        self.assertTrue(all(torch.isfinite(value).all() for value in outputs.values()))
        with self.assertRaisesRegex(ValueError, "divisible"):
            DensityModel(pretrained=False, fusion="view_token_attention",
                         attention_dim=63, attention_heads=8)
        with self.assertRaisesRegex(ValueError, "Unknown fusion"):
            DensityModel(pretrained=False, fusion="unknown")

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
