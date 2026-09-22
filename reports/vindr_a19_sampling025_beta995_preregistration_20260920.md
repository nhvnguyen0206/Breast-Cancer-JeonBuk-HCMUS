# A19 preregistration — sampling .25 with beta .995

## Parent and single treatment

A19 uses completed A6 (`auggeo_dropout30_sampling025`) as its parent. The only
configuration change is effective-number class-weight beta from .999 to .995.
Sampling power remains .25. Architecture, preprocessing, augmentation,
dropout, optimizer, LR, all loss coefficients, AMP, seed and inference remain
unchanged. This is still one DenseNet121 hierarchical-fusion model with the
flat four-class head at inference; no ensemble is used.

## Rationale

A6 improved rare-A consistency and reduced Macro-F1 sample SD from A5's
.11729 to .06445, but reduced mean Macro-F1 to .67655 and lowered every mean
class F1. A17 weakened sampling to .10, but completed at only .64102 mean and
.10282 SD, also lowering every mean class F1. The issue is therefore not
solved by simply lowering sampling exposure.

For fold0 FIT counts `[5,156,1245,207]`, A6's power .25 plus beta .999 makes
the static expected focal pressure approximately
`[.4291,.1956,.1885,.1868]` for A/B/C/D. The rare A class receives about
42.9%, showing strong double compensation. Keeping sampling .25 but changing
beta to .995 changes this static pressure to approximately
`[.2644,.1592,.4110,.1654]`: A retains more draw exposure than natural
sampling, while the primary focal weights no longer suppress C as strongly.
This calculation ignores the dynamic focal factor and auxiliary losses, so it
is a hypothesis rather than a promised gain.

## Fixed protocol and decision rule

- Cache: `/slurmshared/Ngoc/datasets/VinDR_dicom_window16_cvatmask_v1`
- Split: `vindr_density_cv5_seed42_v1`
- Assignment SHA256:
  `43daa86936ee7b1bae1b200836fb1afdfe0c8294c7c865d8f5758bf989f12a9a`
- Seed: 42
- Hardware: RTX 5090 only; worker2 and Vesta excluded; no requeue
- Screen: fresh ImageNet fixed fold0 for exactly 50 epochs
- Expansion gate: completed audited selected DEV four-class Macro-F1 >= .75
- If the gate passes, retain fold0 and launch fresh folds1--4 from the same
  immutable snapshot. Otherwise reject without confirmation.
- No resplitting, fold replacement, favorable-fold screening, ensemble or
  per-fold early stopping.

Full audited CV5 mean/SD/minimum, class F1, accuracy and QWK determine final
utility. A fold0 gain dominated by its single A case is insufficient. DEV is
used for checkpoint selection and is not an independent test.
