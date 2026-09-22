"""Join cached images to density annotations and an existing breast-level split."""
import argparse
import hashlib
import json
from pathlib import Path
import pandas as pd


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def prepare(cache, annotations, protocol, output):
    cache, output = Path(cache).resolve(), Path(output)
    if output.exists() and any(output.iterdir()):
        raise FileExistsError(output)
    records = pd.DataFrame([json.loads(line) for line in (cache / "_images.jsonl").read_text().splitlines()])
    metadata = pd.read_csv(annotations, dtype=str)
    joined = records.merge(metadata, left_on=["study", "image"], right_on=["study_id", "image_id"],
                           how="left", validate="one_to_one", indicator=True)
    if not joined._merge.eq("both").all():
        raise ValueError("Cache has images missing from annotation CSV")
    sets = json.loads(Path(protocol).read_text())["sets"]
    mapping = {}
    for split, ids in sets.items():
        for breast in ids:
            if breast in mapping:
                raise ValueError("Overlapping registered split")
            mapping[breast] = split
    rows, excluded = [], []
    for study, group in joined.groupby("study"):
        views = group.laterality + "_" + group.view_position
        if len(group) != 4 or set(views) != {"L_CC", "L_MLO", "R_CC", "R_MLO"}:
            excluded.append({"case_id": study, "reason": "incomplete_or_duplicate_views"})
            continue
        density = group.breast_density.unique()
        if len(density) != 1 or density[0] not in ["DENSITY " + c for c in "ABCD"]:
            excluded.append({"case_id": study, "reason": "inconsistent_density"})
            continue
        sides = {mapping.get(study + "_" + s) for s in ("L", "R")}
        if len(sides) != 1 or None in sides:
            raise ValueError(f"Missing or inconsistent split for study {study}")
        row = {"case_id": study, "label": density[0][-1], "split": sides.pop()}
        for view, (_, image) in zip(views, group.iterrows()):
            prefix = cache / "tensor_cache" / study / image["image"]
            for suffix in ("_a.npy", "_m.npy", "_s.npy"):
                if not Path(str(prefix) + suffix).is_file():
                    raise FileNotFoundError(str(prefix) + suffix)
            row[view] = str(prefix) + "_a.npy"
        rows.append(row)
    frame = pd.DataFrame(rows)
    output.mkdir(parents=True, exist_ok=True)
    for split, group in frame.groupby("split"):
        group.to_csv(output / f"{split}.csv", index=False)
    pd.DataFrame(excluded).to_csv(output / "excluded.csv", index=False)
    audit = {"cache": str(cache), "cached_images": len(records), "complete_consistent_studies": len(frame),
             "exclusions": pd.Series([r["reason"] for r in excluded]).value_counts().to_dict(),
             "counts": {s: g.label.value_counts().to_dict() for s, g in frame.groupby("split")},
             "source_sha256": {str(p): sha256(p) for p in
                 (Path(annotations), Path(protocol), cache / "_images.jsonl", cache / "_input_provenance.json")},
             "target": "breast_density A/B/C/D; not breast_birads", "split_policy": "existing registered split",
             "preprocessing": "cache float32 + explicit mask validation; area resize; ImageNet normalization"}
    (output / "audit.json").write_text(json.dumps(audit, indent=2))
    print(json.dumps(audit, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--cache-root", required=True)
    parser.add_argument("--annotations", required=True)
    parser.add_argument("--protocol", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    prepare(args.cache_root, args.annotations, args.protocol, args.output_dir)
