# Density-stratified grouped CV5 — seed 42, v1

Created on user request to balance density distributions **between folds**.
The prior 2,017 eligible four-view studies are unchanged: A 6, B 196, C 1,556,
D 259. No oversampling, downsampling, augmentation or label reconciliation
was used to construct the folds.

| DEV fold | A | B | C | D | Total | FIT total |
|---|---:|---:|---:|---:|---:|---:|
| 0 | 1 | 40 | 311 | 52 | 404 | 1,613 |
| 1 | 1 | 39 | 312 | 51 | 403 | 1,614 |
| 2 | 1 | 39 | 311 | 52 | 403 | 1,614 |
| 3 | 2 | 39 | 311 | 52 | 404 | 1,613 |
| 4 | 1 | 39 | 311 | 52 | 403 | 1,614 |

Each CV iteration uses one fold as DEV and all other folds as FIT. FIT contains
4–5 A studies. Every class is present in each FIT and DEV partition. Total size
and each class count differ by at most one between DEV folds.

## Grouping and checks

The supplied `vindr_exact_content_components.json` groups breasts by patient,
source UID and canonical crop hash. Both breasts must resolve to the same
component; the generator fails on unknown or inconsistent mappings. In the
eligible population, 2,009 components represent 2,017 studies: 2,001 singleton
components and eight two-study components, including three mixed-density groups.
Those groups remain indivisible. Components with multiple studies are assigned
first, followed by rarity-ordered singleton balancing with seeded tie-breaking.
Model outputs or validation performance are never used to choose the split.

Verified:

- Every study appears in exactly one DEV fold; all studies are retained.
- No component, case ID or resolved input path crosses FIT/DEV within a fold.
- Local and cluster assignments match exactly, ignoring location-dependent paths.
- Prior local source manifests and registry hashes remain unchanged.
- Nine unit/integration tests pass, including balance, grouping, reproducibility,
  rejection of missing classes and preservation of input manifests.

Registry SHA256:
`1acad026ff40e653caa6347dde9452063567f1755b300ae4791217a545cc3ddf`.
Grouping inherits that registry; this is not a new raw-patient/content audit.

## Files and limitations

Local root: `data/vindr_density_cv5_seed42_v1/`.
Cluster root:
`/slurmshared/Ngoc/code/hcmus-paper1-vindr-20260918-e50/data/vindr_density_cv5_seed42_v1/`.
Each contains `assignments.csv`, `audit.json`, and `fold_0` through `fold_4`,
each with `fit.csv` and `dev.csv`. Manifests remain Git-ignored.

Old FIT/DEV/CAL/OUTER manifests were not overwritten. This new CV protocol
repartitions the old population, so it does not preserve a separately sealed
CAL/OUTER role. DEV is for development/selection, not independent final testing.
Prior development has already exposed some of these cases. Existing scores
cannot be relabeled as results on this split; fresh training is required.

Balancing between folds does not fix the underlying class imbalance: C remains
dominant, and 1–2 A studies per DEV fold cannot support a stable A performance
estimate. No training jobs were submitted as part of this split change.
