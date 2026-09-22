# TN-Mammo: four-view hierarchical relational fusion

One examination contains `L_CC, L_MLO, R_CC, R_MLO`, in that order.
The target is breast density A/B/C/D, not cancer diagnosis or severity.

The architecture follows the original diagram:

1. Shared ImageNet-pretrained DenseNet121, input 512×512, global average pooling.
2. Shared ipsilateral fusion of CC/MLO per breast: gated combination, absolute
   difference, elementwise product, residual projection and LayerNorm.
3. Bilateral fusion of left/right representations using gates and a bottleneck MLP.
4. Flat four-class head, CORAL ordinal head (shared score and three biases),
   binary head (A+B versus C+D).
5. Inference uses only `argmax(softmax(flat_logits))`.

Training loss: class-balanced focal + 0.5 CORAL + 0.3 binary CE + 0.2 expected
neighbor cost. Class weights are calculated from the current training manifest.
The ordinal and binary heads provide auxiliary supervision.

## Install and run

Use Python 3.10+ and a compatible PyTorch/torchvision installation.

```bash
pip install -r requirements.txt
python train.py --train-manifest data/train.csv --valid-manifest data/valid.csv --output-dir outputs/run1
python inference.py --checkpoint outputs/run1/best.pt --manifest data/holdout.csv --output-dir outputs/predictions1
python -m unittest discover -s tests -v
```

Training downloads ImageNet weights on first use. Set `model.pretrained: false`
for an offline smoke run. CLI supports `--device cpu` or `--device cuda`.

CSV schema (one case per row, paths absolute or relative to the CSV):

```csv
case_id,label,L_CC,L_MLO,R_CC,R_MLO
example,A,example/L_CC.dcm,example/L_MLO.dcm,example/R_CC.dcm,example/R_MLO.dcm
```

Inference accepts a manifest without `label`. All four views must be present.
DICOM decoding uses VOI LUT, MONOCHROME1 inversion, min/max to uint8, Otsu
foreground crop, CLAHE, square resize and ImageNet normalization. Training
uses mild shared brightness augmentation and preserves view orientation.
Compressed DICOM may require a decoder such as pylibjpeg for its transfer syntax.

The training entrypoint rejects overlapping case IDs or resolved image paths.
Use patient-disjoint manifests if a patient has multiple examinations: case/path
checks alone cannot establish patient independence. Validation selects the best
epoch by four-class Macro-F1. Training writes `best.pt`, `history.json` and
`valid_predictions.csv`. Use an empty output directory for each run.

## Frozen VinDR cache

Use `scripts/prepare_vindr.py --cache-root CACHE --annotations ANNOTATIONS.csv
--protocol inner_fold0_seed42.json --output-dir data/vindr_cache_fold0` to join
the frozen cache to original **density** labels and an existing registered
breast-level split. Only complete four-view studies with consistent density
labels are included; both breasts must belong to the same split. Exclusions,
class counts and source hashes are saved in `audit.json` and `excluded.csv`.

```bash
python train.py --config configs/vindr_cache.yaml --train-manifest data/vindr_cache_fold0/fit.csv --valid-manifest data/vindr_cache_fold0/dev.csv --output-dir outputs/vindr_cache_fold0_pilot5
```

The cache mode reads `_a.npy` float32 values directly, validates the explicit
big-endian packed `_m.npy` mask using `_s.npy`, and does not repeat windowing,
CLAHE, cropping or division by 65535. It applies area resize to 512×512,
shared brightness augmentation during training, and ImageNet normalization.
Inference selects this loader automatically from the saved checkpoint config.
The source cache is read-only throughout this workflow.

`configs/vindr_cache.yaml` is a **five-epoch pilot**, not a converged benchmark.
Fold 0 of the supplied cache has FIT 1,035 / DEV 324 / CAL 254 / OUTER 404
eligible studies. FIT has only two class-A studies and DEV has none; four-class
Macro-F1 therefore includes a zero A component and cannot establish A-class
performance. CAL and OUTER are not used in the pilot. These are registered
campaign partitions, not necessarily the original VinDR train/test split.

Pilot results and limitations: [VinDR fold-0 report](reports/vindr_cache_fold0_pilot5_20260918.md).

### Density-balanced five-fold protocol (v1)

The new split is `data/vindr_density_cv5_seed42_v1`, separate from the old
binary-label campaign split. Build it with:

```bash
python scripts/prepare_density_folds.py --source-dir data/vindr_cache_fold0 --component-registry /path/to/vindr_exact_content_components.json --output-dir data/vindr_density_cv5_seed42_v1
```

For CV iteration `i`, use `fold_i/fit.csv` (other four folds) and `fold_i/dev.csv`
(the held-out fold). Every study appears in DEV exactly once across five
iterations. Grouping inherits the supplied patient/source-UID/content registry.
Per-class counts and total fold sizes differ by at most one across folds.
This balances **distributions across folds**, not the numbers of A/B/C/D within
each fold. Only six A studies exist. No resampling, new cases or relabeling
are introduced. `assignments.csv` and `audit.json` record the reproducible split.

This is a new development-CV protocol without a separate CAL/OUTER partition.
The old manifests and completed runs remain unchanged. DEV-selected results
are not independent final-test estimates; some cases have already been used
in earlier development runs. Existing Slurm launchers still point to the old
manifests unless explicitly changed. No training was launched by split creation.
See [split audit](reports/vindr_density_cv5_seed42_v1.md).

`scripts/train_density_cv5_5090.sbatch` now defaults to fixed fold 0 for screening.
Only after screening Macro-F1 reaches 0.75, explicitly submit with
`sbatch --array=0-4%5` for five-fold confirmation. Each task runs
`scripts/train_density_fold.py` and verifies
the split hash and exact FIT/DEV payloads, trains from ImageNet for 50 epochs,
and logs under a shared W&B group with a distinct fold name. This is separate
from the old single-fold launchers. See the
[CV5 launch record](reports/vindr_density_cv5_launch_20260918.md).
Completed metrics and limitations: [CV5 results](reports/vindr_density_cv5_results_20260918.md).

Active improvement experiments: [experiment ledger](reports/density_improvement_ledger.md).
The first controlled ablation uses `configs/vindr_density_letterbox.yaml`:
area resize preserving aspect ratio, centered zero padding, then the unchanged
brightness augmentation and ImageNet normalization. Existing configs default
to the original stretch resize. Inference restores the checkpoint's resize mode.
Pass the ablation config as the second argument to the CV5 Slurm launcher.

Optional `training.sampling_power` controls FIT-only class-aware sampling:
0 (default) retains natural shuffle, 0.5 tempers imbalance, 1 balances expected
class counts. Nonzero settings draw with replacement for the original FIT-size
epoch budget; they do not add independent cases or alter DEV. Expected class
probabilities and realized epoch counts are logged. This option is prepared
for controlled screening, not yet an established improvement.

### W&B and Atlas RTX 5090

`configs/vindr_cache_5090.yaml` starts a fresh ImageNet-initialized fold-0 run:
minimum 20 epochs, maximum 50, patience 10, cosine schedule over 50 epochs.
The minimum only gates early stopping; model selection considers every epoch.
Architecture, loss, batch size and data partitions are unchanged from the pilot.
For a full 50-epoch run without early stopping, use
`configs/vindr_cache_5090_full50.yaml` (`min_epochs: 50`, `epochs: 50`).
The Slurm script accepts the config path as its optional second argument.
Install `requirements-wandb.txt` for optional W&B logging. The project is
`TN_Mammo_BreastDensity/HCMUS-paper1`; credentials must come from the environment
or an existing netrc, never from committed source.

`scripts/train_atlas_5090.sbatch DEPLOYED_REPO` requests one GPU, 8 CPUs,
48 GiB RAM and six hours. It validates that the allocated GPU is an RTX 5090.
It uses the cluster's existing CUDA-12.8 PyTorch environment; missing pydicom
and OpenCV dependencies can be installed under the deployment's `.deps/` to
avoid modifying the shared environment. Generate manifests against the remote
cache root using the same annotations and registered protocol before submission.

W&B receives epoch loss components, DEV metrics, per-class F1, aggregate
confusion matrices, learning rate, elapsed time and selected-checkpoint metrics.
Images, case IDs, prediction CSVs and checkpoint weights are not uploaded.
`scripts/publish_history.py` imports a previous local run's aggregate history
as a separately labeled historical run. Run details are recorded in the
[cluster launch note](reports/vindr_5090_wandb_20260918.md).

## Cleanup and checkpoint status

This branch contains a single DenseNet pipeline. Region attention, ConvNeXt,
ensembles, segmentation and duplicated experimental packages were removed.
Code and old weights can be recovered from commit
`00f7e0fc8006318a697eba2c47642e48226e3a68` (Git LFS required for LFS weights).
No old checkpoint is claimed compatible with this implementation; train a new
checkpoint. The previous ensemble score 0.7496 does not apply to this model.
`papers/` is retained as research documentation.

Tests use synthetic DICOM and random initialization. They establish that data,
training and inference execute, not accuracy on TN-Mammo. This checkout does
not include the clinical dataset. Keep the historically reused Test-132 out of
model selection; use an independent holdout for a new final performance claim.
