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
