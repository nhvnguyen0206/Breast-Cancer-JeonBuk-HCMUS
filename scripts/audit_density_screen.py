"""Read-only audit of a completed fixed-fold density screening run."""
import argparse
import csv
import hashlib
import json
import math
from pathlib import Path

import torch
from sklearn.metrics import accuracy_score, cohen_kappa_score, confusion_matrix, f1_score


def require(condition, message):
    if not condition:
        raise ValueError(message)


def rows(path):
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


def audit(run_dir, split_root, arm, fold, wandb_project=None):
    run_dir, split_root = Path(run_dir), Path(split_root)
    protocol = json.loads((split_root / "audit.json").read_text())
    require(protocol["schema"] == "tn_mammo.density_grouped_cv.v1" and protocol["n_splits"] == 5,
            "Unexpected split protocol")
    digest = hashlib.sha256((split_root / "assignments.csv").read_bytes()).hexdigest()
    require(digest == protocol["assignments_sha256"], "Assignment digest mismatch")
    assignments = rows(split_root / "assignments.csv")
    require(len({r["case_id"] for r in assignments}) == len(assignments), "Duplicate assignment IDs")
    # Validate all frozen fold manifests before a possible expansion.
    for candidate in range(5):
        for role, selected in (("dev", True), ("fit", False)):
            manifest = rows(split_root / f"fold_{candidate}" / f"{role}.csv")
            expected = {r["case_id"]: r for r in assignments
                        if (int(r["fold"]) == candidate) == selected}
            require(len(manifest) == len(expected) and {r["case_id"] for r in manifest} == set(expected),
                    f"Fold {candidate}: {role} membership mismatch")
            for row in manifest:
                require(all(row[k] == expected[row["case_id"]][k]
                            for k in ("label", "L_CC", "L_MLO", "R_CC", "R_MLO")),
                        f"Fold {candidate}: {role} manifest content mismatch")
    history = json.loads((run_dir / "history.json").read_text())
    require([r["epoch"] for r in history] == list(range(1, 51)), "Incomplete epochs")
    require(all(math.isfinite(v) for record in history for v in record["train"].values()),
            "Non-finite training history")
    best = max(history, key=lambda r: r["valid"]["macro_f1"])
    checkpoint = torch.load(run_dir / "best.pt", map_location="cpu", weights_only=False)
    config, exp = checkpoint["config"], checkpoint["config"]["experiment"]
    fusion = config["model"].get("fusion", "hierarchical_relational")
    primary_head = config["model"].get("primary_head", "flat")
    ordinal_gap = float(config["model"].get("ordinal_initial_gap", 1.0))
    backbone = config["model"].get("backbone", "densenet121")
    view_auxiliary = config["model"].get("view_auxiliary", False)
    require(isinstance(view_auxiliary, bool), "view_auxiliary must be boolean")
    mixstyle_probability = config["model"].get("mixstyle_probability", 0.0)
    mixstyle_alpha = config["model"].get("mixstyle_alpha", 0.1)
    fine_d_expert = config["model"].get("fine_d_expert", False)
    require(isinstance(fine_d_expert, bool), "fine_d_expert must be boolean")
    isolate_fine_d_rng = config["model"].get("isolate_fine_d_rng", False)
    require(isinstance(isolate_fine_d_rng, bool),
            "isolate_fine_d_rng must be boolean")
    projection_adapters = config["model"].get("projection_adapters", False)
    require(isinstance(projection_adapters, bool),
            "projection_adapters must be boolean")
    projection_adapter_dim = config["model"].get("projection_adapter_dim", 96)
    require(isinstance(projection_adapter_dim, int)
            and not isinstance(projection_adapter_dim, bool)
            and projection_adapter_dim > 0,
            "projection_adapter_dim must be a positive integer")
    bilateral_spatial_relation = config["model"].get(
        "bilateral_spatial_relation", False
    )
    require(isinstance(bilateral_spatial_relation, bool),
            "bilateral_spatial_relation must be boolean")
    bilateral_relation_dim = config["model"].get("bilateral_relation_dim", 256)
    require(isinstance(bilateral_relation_dim, int)
            and not isinstance(bilateral_relation_dim, bool)
            and bilateral_relation_dim > 0,
            "bilateral_relation_dim must be a positive integer")
    multiscale_a_expert = config["model"].get("multiscale_a_expert", False)
    require(isinstance(multiscale_a_expert, bool),
            "multiscale_a_expert must be boolean")
    multiscale_a_replacement = config["model"].get(
        "multiscale_a_replacement", False
    )
    require(isinstance(multiscale_a_replacement, bool),
            "multiscale_a_replacement must be boolean")
    require(not isinstance(mixstyle_probability, bool)
            and isinstance(mixstyle_probability, (int, float))
            and math.isfinite(float(mixstyle_probability))
            and 0 <= float(mixstyle_probability) <= 1,
            "mixstyle_probability must be finite and in [0,1]")
    require(not isinstance(mixstyle_alpha, bool)
            and isinstance(mixstyle_alpha, (int, float))
            and math.isfinite(float(mixstyle_alpha)) and float(mixstyle_alpha) > 0,
            "mixstyle_alpha must be finite and positive")
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
                "Per-view auxiliary architecture mismatch")
        expected_architecture = "convnext_tiny_local_global_view_transformer_perview_aux_v12"
    if float(mixstyle_probability) > 0:
        require(view_auxiliary and float(mixstyle_probability) == .5
                and float(mixstyle_alpha) == .1,
                "MixStyle screening contract mismatch")
        expected_architecture = "convnext_tiny_local_global_view_transformer_perview_aux_mixstyle_v13"
    if fine_d_expert:
        require((backbone, fusion, primary_head, ordinal_gap)
                == ("convnext_tiny", "hybrid_relational_spatial_attention",
                    "a_gate_hierarchical", 1.0),
                "Fine-scale D expert architecture mismatch")
        expected_architecture = "convnext_tiny_hybrid_spatial_a_gate_fine_d_expert_v15"
    if isolate_fine_d_rng:
        require(fine_d_expert,
                "Fine-D RNG isolation requires fine_d_expert")
        expected_architecture = (
            "convnext_tiny_hybrid_spatial_a_gate_fine_d_expert_rngisolated_v16"
        )
    if projection_adapters:
        require(not fine_d_expert and projection_adapter_dim == 96,
                "Projection adapter screening contract mismatch")
        require((backbone, fusion, primary_head, ordinal_gap)
                == ("convnext_tiny", "hybrid_relational_spatial_attention",
                    "a_gate_hierarchical", 1.0),
                "Projection adapter architecture mismatch")
        expected_architecture = (
            "convnext_tiny_hybrid_spatial_a_gate_projection_adapters_v17"
        )
    if bilateral_spatial_relation:
        require(not fine_d_expert and not projection_adapters
                and bilateral_relation_dim == 256,
                "Bilateral relation screening contract mismatch")
        require((backbone, fusion, primary_head, ordinal_gap)
                == ("convnext_tiny", "hybrid_relational_spatial_attention",
                    "a_gate_hierarchical", 1.0),
                "Bilateral relation architecture mismatch")
        expected_architecture = (
            "convnext_tiny_hybrid_spatial_a_gate_bilateral_relation_v18"
        )
    if multiscale_a_expert:
        require(not fine_d_expert and not projection_adapters
                and not bilateral_spatial_relation,
                "Multi-scale A expert screening contract mismatch")
        require((backbone, fusion, primary_head, ordinal_gap)
                == ("convnext_tiny", "hybrid_relational_spatial_attention",
                    "a_gate_hierarchical", 1.0),
                "Multi-scale A expert architecture mismatch")
        expected_architecture = (
            "convnext_tiny_hybrid_spatial_a_gate_multiscale_a_expert_v19"
        )
    if multiscale_a_replacement:
        require(not fine_d_expert and not projection_adapters
                and not bilateral_spatial_relation and not multiscale_a_expert,
                "Multi-scale A replacement screening contract mismatch")
        require((backbone, fusion, primary_head, ordinal_gap)
                == ("convnext_tiny", "hybrid_relational_spatial_attention",
                    "a_gate_hierarchical", 1.0),
                "Multi-scale A replacement architecture mismatch")
        expected_architecture = "convnext_tiny_hybrid_bcd_multiscale_a_gate_v20"
    require(expected_architecture is not None
            and checkpoint["architecture"] == expected_architecture,
            "Architecture mismatch")
    require(exp["fold"] == fold and exp["arm"] == arm and exp["split_seed"] == protocol["seed"]
            and exp["n_folds"] == 5 and exp["assignments_sha256"] == digest
            and exp["initialization"] == "fresh_imagenet" and exp["independent_test"] is False,
            "Experiment provenance mismatch")
    require(config["seed"] == 42 and config["training"]["epochs"] == 50
            and config["training"]["min_epochs"] == 50, "Training contract mismatch")
    require(checkpoint["epoch"] == best["epoch"], "Wrong selected checkpoint epoch")
    compare(best["valid"], checkpoint["valid_metrics"], "Checkpoint")
    expected = {r["case_id"]: r for r in assignments if int(r["fold"]) == fold}
    predictions = rows(run_dir / "valid_predictions.csv")
    require(len(predictions) == len(expected) == len({r["case_id"] for r in predictions})
            and {r["case_id"] for r in predictions} == set(expected), "Prediction membership mismatch")
    truth, predicted, max_error = [], [], 0.0
    for row in predictions:
        y, p = int(row["true_index"]), int(row["pred_index"])
        probabilities = [float(row["prob_" + label]) for label in "ABCD"]
        require(all(math.isfinite(v) and 0 <= v <= 1 for v in probabilities), "Invalid probabilities")
        error = abs(sum(probabilities) - 1)
        require(error <= 1e-5, "Probabilities do not sum to one")
        max_error = max(max_error, error)
        require(y == "ABCD".index(expected[row["case_id"]]["label"]), "Wrong true label")
        require(p == max(range(4), key=probabilities.__getitem__) and row["pred_label"] == "ABCD"[p],
                "Prediction differs from argmax")
        truth.append(y); predicted.append(p)
    recomputed = metrics(truth, predicted)
    compare(recomputed, best["valid"], "Predictions")
    result = {"audit": "PASS", "arm": arm, "fold": fold, "assignments_sha256": digest,
              "independent_test": False, "epochs": len(history), "best_epoch": best["epoch"],
              "best": recomputed, "epoch50": history[-1]["valid"],
              "epochs_at_or_above_075": sum(r["valid"]["macro_f1"] >= .75 for r in history),
              "amp_skipped_updates_total": sum(r.get("amp_skipped_updates", 0) for r in history),
              "max_probability_sum_error": max_error, "all_fold_manifests_validated": True}
    if wandb_project:
        import wandb
        metadata = json.loads(run_dir.with_name(run_dir.name + "_wandb.json").read_text())
        run = wandb.Api(timeout=30).run(wandb_project + "/" + metadata["id"])
        require(run.state == "finished" and run.summary.get("completed_epochs") == 50,
                "W&B run not complete")
        require(run.summary.get("best_epoch") == best["epoch"]
                and math.isclose(run.summary["best/macro_f1"], recomputed["macro_f1"], abs_tol=1e-9),
                "W&B selection mismatch")
        result.update(wandb_id=run.id, wandb_url=run.url, wandb_state=run.state)
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--split-root", required=True)
    parser.add_argument("--arm", required=True)
    parser.add_argument("--fold", type=int, default=0)
    parser.add_argument("--wandb-project")
    args = parser.parse_args()
    print(json.dumps(audit(args.run_dir, args.split_root, args.arm, args.fold, args.wandb_project), indent=2))
