# A18 preregistration — fixed DenseNet BatchNorm statistics

## Parent and single treatment

A18 uses the completed best-mean A5 arm as its parent. The only intended
learning-behavior change is `training.freeze_backbone_batchnorm: true`:
all 121 DenseNet121 BatchNorm modules use fixed ImageNet running means and
variances throughout fine-tuning. DenseNet convolution weights, BatchNorm
affine parameters, hierarchical bilateral fusion and all three heads remain
trainable. The model architecture and single flat-head inference path are
unchanged; no ensemble or weight averaging is used.

Everything else remains A5: stretch resize at 512, window16 cache, geometric
and brightness augmentation, dropout .3, bottleneck256, beta .999, gamma2,
loss coefficients .5/.3/.2, natural sampling, AdamW LR 5e-5, weight decay
1e-4, full50 epochs and seed42.

## Rationale

A17 sampling power .10 completed at mean Macro-F1 .6410178898, sample SD
.1028187513 and minimum .5376961279, lowering every mean class F1 relative to
A5. It is rejected. Reweighting exposure again is therefore not the next
step.

A read-only A5 diagnostic found material selected-checkpoint drift in all 121
DenseNet BatchNorm running-stat buffers. Mean standardized running-mean drift
across folds ranged .1262--.2287 and mean absolute log variance ratio ranged
.3172--.4181. With batch size two and four correlated views per exam, fixing
pretrained running statistics is a plausible variance-control intervention.
This observation is motivation only and does not imply improvement.

## Fixed protocol and decision rule

- Dataset/cache: `/slurmshared/Ngoc/datasets/VinDR_dicom_window16_cvatmask_v1`
- Split: `vindr_density_cv5_seed42_v1`
- Assignment SHA256:
  `43daa86936ee7b1bae1b200836fb1afdfe0c8294c7c865d8f5758bf989f12a9a`
- Training seed: 42
- Hardware: RTX 5090 only; exclude worker2 and do not use Vesta
- Screen: fresh ImageNet initialization on fixed fold0 for exactly 50 epochs
- Expansion gate: completed audited selected DEV four-class Macro-F1 >= .75
- If the gate passes, retain that fold0 and launch fresh folds1--4 from the
  identical snapshot. Otherwise reject A18 and do not launch confirmation.
- Do not resplit, replace folds, stop an unfavorable fold, or select a
  favorable screening fold.

Final success remains a full audited CV5 result, not the fold0 screen. Report
mean and sample SD of Macro-F1, minimum fold, per-class F1, accuracy and QWK.
Class A has only six studies, so a fold0 gain driven by its single A case is
not sufficient evidence. DEV is used for selection and is not an independent
test.
