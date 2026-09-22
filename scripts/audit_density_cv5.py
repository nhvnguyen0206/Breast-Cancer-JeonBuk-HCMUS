"""Read-only audit of five completed density-CV runs; emit a JSON report."""
import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
import statistics

import torch
from sklearn.metrics import accuracy_score, cohen_kappa_score, confusion_matrix, f1_score


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read_csv(path):
    with Path(path).open(newline="") as stream:
        return list(csv.DictReader(stream))


def metrics(truth, predicted):
    return {
        "num_samples": len(truth),
        "accuracy": float(accuracy_score(truth, predicted)),
        "macro_f1": float(f1_score(truth, predicted, labels=range(4), average="macro", zero_division=0)),
        "per_class_f1": f1_score(truth, predicted, labels=range(4), average=None, zero_division=0).tolist(),
        "qwk": float(cohen_kappa_score(truth, predicted, weights="quadratic")),
        "confusion_matrix": confusion_matrix(truth, predicted, labels=range(4)).tolist(),
        "severe_errors": sum(abs(y - p) >= 2 for y, p in zip(truth, predicted)),
    }


def compare(actual, expected, context):
    require(set(actual) <= set(expected), context + ": missing metrics")
    for key, value in actual.items():
        if isinstance(value, float):
            require(math.isfinite(value) and math.isclose(value, expected[key], abs_tol=1e-10, rel_tol=1e-9),
                    context + ": " + key)
        else:
            require(value == expected[key], context + ": " + key)


def audit(run_dirs, split_root, arm, wandb_project=None):
    require(len(run_dirs) == 5, "Exactly five run directories in fold order are required")
    split_root = Path(split_root)
    protocol = json.loads((split_root / "audit.json").read_text())
    require(protocol["schema"] == "tn_mammo.density_grouped_cv.v1" and protocol["n_splits"] == 5,
            "Unexpected split protocol")
    digest = hashlib.sha256((split_root / "assignments.csv").read_bytes()).hexdigest()
    require(digest == protocol["assignments_sha256"], "Assignment digest mismatch")
    assignments = read_csv(split_root / "assignments.csv")
    expected_all = {r["case_id"] for r in assignments}
    require(len(expected_all) == len(assignments), "Duplicate assignment IDs")
    api = None
    if wandb_project:
        import wandb
        api = wandb.Api(timeout=30)
    folds, all_ids, truth_all, pred_all = [], set(), [], []
    common_config = None
    for fold, directory in enumerate(run_dirs):
        directory = Path(directory)
        history = json.loads((directory / "history.json").read_text())
        require([r["epoch"] for r in history] == list(range(1, 51)), f"Fold {fold}: incomplete epochs")
        best = max(history, key=lambda r: r["valid"]["macro_f1"])
        # Only load trusted checkpoints produced by this campaign.
        checkpoint = torch.load(directory / "best.pt", map_location="cpu", weights_only=False)
        config = checkpoint["config"]
        exp = config["experiment"]
        fusion = config["model"].get("fusion", "hierarchical_relational")
        primary_head = config["model"].get("primary_head", "flat")
        ordinal_gap = float(config["model"].get("ordinal_initial_gap", 1.0))
        backbone = config["model"].get("backbone", "densenet121")
        view_auxiliary = config["model"].get("view_auxiliary", False)
        require(isinstance(view_auxiliary, bool),
                f"Fold {fold}: view_auxiliary must be boolean")
        mixstyle_probability = config["model"].get("mixstyle_probability", 0.0)
        mixstyle_alpha = config["model"].get("mixstyle_alpha", 0.1)
        fine_d_expert = config["model"].get("fine_d_expert", False)
        require(isinstance(fine_d_expert, bool),
                f"Fold {fold}: fine_d_expert must be boolean")
        isolate_fine_d_rng = config["model"].get("isolate_fine_d_rng", False)
        require(isinstance(isolate_fine_d_rng, bool),
                f"Fold {fold}: isolate_fine_d_rng must be boolean")
        projection_adapters = config["model"].get("projection_adapters", False)
        require(isinstance(projection_adapters, bool),
                f"Fold {fold}: projection_adapters must be boolean")
        projection_adapter_dim = config["model"].get("projection_adapter_dim", 96)
        require(isinstance(projection_adapter_dim, int)
                and not isinstance(projection_adapter_dim, bool)
                and projection_adapter_dim > 0,
                f"Fold {fold}: invalid projection_adapter_dim")
        bilateral_spatial_relation = config["model"].get(
            "bilateral_spatial_relation", False
        )
        require(isinstance(bilateral_spatial_relation, bool),
                f"Fold {fold}: bilateral_spatial_relation must be boolean")
        bilateral_relation_dim = config["model"].get(
            "bilateral_relation_dim", 256
        )
        require(isinstance(bilateral_relation_dim, int)
                and not isinstance(bilateral_relation_dim, bool)
                and bilateral_relation_dim > 0,
                f"Fold {fold}: invalid bilateral_relation_dim")
        require(not isinstance(mixstyle_probability, bool)
                and isinstance(mixstyle_probability, (int, float))
                and math.isfinite(float(mixstyle_probability))
                and 0 <= float(mixstyle_probability) <= 1,
                f"Fold {fold}: invalid mixstyle_probability")
        require(not isinstance(mixstyle_alpha, bool)
                and isinstance(mixstyle_alpha, (int, float))
                and math.isfinite(float(mixstyle_alpha))
                and float(mixstyle_alpha) > 0,
                f"Fold {fold}: invalid mixstyle_alpha")
        expected_architecture = {
            ("densenet121", "hierarchical_relational", "flat", 1.0): "densenet121_hierarchical_bilateral_multitask_v1",
            ("densenet121", "view_token_attention", "flat", 1.0): "densenet121_view_token_attention_multitask_v2",
            ("densenet121", "spatial_token_attention", "flat", 1.0): "densenet121_spatial_view_attention_multitask_v3",
            ("densenet121", "hierarchical_relational", "monotonic_ordinal", 1.0): "densenet121_hierarchical_bilateral_ordinalprimary_v4",
            ("densenet121", "hierarchical_relational", "monotonic_ordinal", 2.0): "densenet121_hierarchical_bilateral_ordinalprimary_wide_v5",
            ("convnext_tiny", "hierarchical_relational", "flat", 1.0): "convnext_tiny_hierarchical_bilateral_multitask_v6",
            ("convnext_tiny", "hybrid_relational_spatial_attention", "flat", 1.0): "convnext_tiny_hybrid_relational_spatial_multitask_v7",
            ("convnext_tiny", "hybrid_relational_spatial_attention", "a_gate_hierarchical", 1.0): "convnext_tiny_hybrid_spatial_a_gate_multitask_v8",
            ("convnext_tiny", "hybrid_relational_spatial_attention", "dual_endpoint_hierarchical", 1.0): "convnext_tiny_hybrid_spatial_dual_endpoint_gate_multitask_v14",
            ("convnext_tiny", "multiscale_view_token_attention", "flat", 1.0): "convnext_tiny_multiscale_view_transformer_multitask_v9",
            ("convnext_tiny", "multiscale_view_token_attention", "a_gate_hierarchical", 1.0): "convnext_tiny_multiscale_view_transformer_a_gate_v10",
            ("convnext_tiny", "local_global_view_attention", "a_gate_hierarchical", 1.0): "convnext_tiny_local_global_view_transformer_a_gate_v11",
        }.get((backbone, fusion, primary_head, ordinal_gap))
        if view_auxiliary:
            require((backbone, fusion, primary_head, ordinal_gap)
                    == ("convnext_tiny", "local_global_view_attention",
                        "a_gate_hierarchical", 1.0),
                    f"Fold {fold}: per-view auxiliary architecture mismatch")
            expected_architecture = "convnext_tiny_local_global_view_transformer_perview_aux_v12"
        if float(mixstyle_probability) > 0:
            require(view_auxiliary and float(mixstyle_probability) == .5
                    and float(mixstyle_alpha) == .1,
                    f"Fold {fold}: MixStyle contract mismatch")
            expected_architecture = "convnext_tiny_local_global_view_transformer_perview_aux_mixstyle_v13"
        if fine_d_expert:
            require((backbone, fusion, primary_head, ordinal_gap)
                    == ("convnext_tiny", "hybrid_relational_spatial_attention",
                        "a_gate_hierarchical", 1.0),
                    f"Fold {fold}: fine-scale D expert architecture mismatch")
            expected_architecture = "convnext_tiny_hybrid_spatial_a_gate_fine_d_expert_v15"
        if isolate_fine_d_rng:
            require(fine_d_expert,
                    f"Fold {fold}: Fine-D RNG isolation requires fine_d_expert")
            expected_architecture = (
                "convnext_tiny_hybrid_spatial_a_gate_fine_d_expert_rngisolated_v16"
            )
        if projection_adapters:
            require(not fine_d_expert and projection_adapter_dim == 96,
                    f"Fold {fold}: projection adapter screening contract mismatch")
            require((backbone, fusion, primary_head, ordinal_gap)
                    == ("convnext_tiny", "hybrid_relational_spatial_attention",
                        "a_gate_hierarchical", 1.0),
                    f"Fold {fold}: projection adapter architecture mismatch")
            expected_architecture = (
                "convnext_tiny_hybrid_spatial_a_gate_projection_adapters_v17"
            )
        if bilateral_spatial_relation:
            require(not fine_d_expert and not projection_adapters
                    and bilateral_relation_dim == 256,
                    f"Fold {fold}: bilateral relation screening contract mismatch")
            require((backbone, fusion, primary_head, ordinal_gap)
                    == ("convnext_tiny", "hybrid_relational_spatial_attention",
                        "a_gate_hierarchical", 1.0),
                    f"Fold {fold}: bilateral relation architecture mismatch")
            expected_architecture = (
                "convnext_tiny_hybrid_spatial_a_gate_bilateral_relation_v18"
            )
        require(expected_architecture is not None
                and checkpoint["architecture"] == expected_architecture,
                f"Fold {fold}: architecture mismatch")
        require(exp["split_seed"] == protocol["seed"] and exp["n_folds"] == 5
                and exp["independent_test"] is False and exp["initialization"] == "fresh_imagenet",
                f"Fold {fold}: protocol metadata mismatch")
        require(exp["fold"] == fold and exp["arm"] == arm and exp["assignments_sha256"] == digest,
                f"Fold {fold}: experiment provenance mismatch")
        require(config["training"]["epochs"] == config["training"]["min_epochs"] == 50,
                f"Fold {fold}: epoch contract mismatch")
        comparable = {k: v for k, v in config.items() if k not in {"experiment", "wandb"}}
        if common_config is None:
            common_config = comparable
        require(comparable == common_config, f"Fold {fold}: learning config differs")
        require(checkpoint["epoch"] == best["epoch"], f"Fold {fold}: wrong selected epoch")
        compare(best["valid"], checkpoint["valid_metrics"], f"Fold {fold}: checkpoint")
        expected = {r["case_id"]: r for r in assignments if int(r["fold"]) == fold}
        for role, select in (("dev", True), ("fit", False)):
            manifest = read_csv(split_root / f"fold_{fold}" / f"{role}.csv")
            registered = {r["case_id"]: r for r in assignments if (int(r["fold"]) == fold) == select}
            require(len(manifest) == len(registered) and {r["case_id"] for r in manifest} == set(registered),
                    f"Fold {fold}: {role} membership mismatch")
            for row in manifest:
                require(all(row[k] == registered[row["case_id"]][k]
                            for k in ("label", "L_CC", "L_MLO", "R_CC", "R_MLO")),
                        f"Fold {fold}: {role} manifest content mismatch")
        predictions = read_csv(directory / "valid_predictions.csv")
        ids = {r["case_id"] for r in predictions}
        require(len(ids) == len(predictions) == len(expected) and ids == set(expected),
                f"Fold {fold}: prediction membership mismatch")
        require(not (ids & all_ids), "DEV folds overlap")
        all_ids.update(ids)
        truth, predicted, max_error = [], [], 0.0
        for row in predictions:
            y, p = int(row["true_index"]), int(row["pred_index"])
            probabilities = [float(row["prob_" + c]) for c in "ABCD"]
            require(all(math.isfinite(v) and 0 <= v <= 1 for v in probabilities), "Invalid probabilities")
            error = abs(sum(probabilities) - 1)
            require(error <= 1e-5, "Probabilities do not sum to one")
            max_error = max(max_error, error)
            require(y == "ABCD".index(expected[row["case_id"]]["label"]), "Wrong true label")
            require(p == max(range(4), key=probabilities.__getitem__) and row["pred_label"] == "ABCD"[p],
                    "Prediction differs from argmax")
            truth.append(y)
            predicted.append(p)
        recomputed = metrics(truth, predicted)
        compare(recomputed, best["valid"], f"Fold {fold}: predictions")
        result = {"fold": fold, "best_epoch": best["epoch"], "best": recomputed,
                  "epoch50": history[-1]["valid"], "max_probability_sum_error": max_error}
        if api:
            metadata = json.loads(directory.with_name(directory.name + "_wandb.json").read_text())
            run = api.run(wandb_project + "/" + metadata["id"])
            require(run.state == "finished" and run.summary.get("completed_epochs") == 50,
                    f"Fold {fold}: W&B not complete")
            require(run.summary.get("best_epoch") == best["epoch"], "W&B selected epoch mismatch")
            require(math.isclose(run.summary["best/macro_f1"], recomputed["macro_f1"], abs_tol=1e-9),
                    "W&B score mismatch")
            result.update(wandb_id=run.id, wandb_url=run.url, wandb_state=run.state)
        folds.append(result)
        truth_all.extend(truth)
        pred_all.extend(predicted)
    require(all_ids == expected_all, "CV union differs from assignments")
    aggregate = {}
    for name in ("macro_f1", "accuracy", "qwk"):
        values = [r["best"][name] for r in folds]
        aggregate[name + "_mean"] = statistics.mean(values)
        aggregate[name + "_sample_sd"] = statistics.stdev(values)
    aggregate["per_class_f1_mean"] = [statistics.mean(r["best"]["per_class_f1"][k] for r in folds) for k in range(4)]
    aggregate["per_class_f1_sample_sd"] = [statistics.stdev(r["best"]["per_class_f1"][k] for r in folds) for k in range(4)]
    aggregate["bcd_f1_mean"] = statistics.mean(aggregate["per_class_f1_mean"][1:])
    aggregate["epoch50_macro_f1_mean"] = statistics.mean(r["epoch50"]["macro_f1"] for r in folds)
    aggregate["epoch50_macro_f1_sample_sd"] = statistics.stdev(r["epoch50"]["macro_f1"] for r in folds)
    return {"audit": "PASS", "arm": arm, "assignments_sha256": digest,
            "independent_test": False, "folds": folds, "aggregate": aggregate,
            "pooled_descriptive": metrics(truth_all, pred_all), "unique_cases": len(all_ids),
            "support": [truth_all.count(k) for k in range(4)]}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dirs", nargs=5, required=True, help="Trusted run directories in fold order")
    parser.add_argument("--split-root", required=True)
    parser.add_argument("--arm", required=True)
    parser.add_argument("--wandb-project", help="Optional entity/project; additionally require finished W&B runs")
    args = parser.parse_args()
    print(json.dumps(audit(args.run_dirs, args.split_root, args.arm, args.wandb_project), indent=2))
