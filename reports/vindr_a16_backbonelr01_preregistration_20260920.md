# A16: 0.1x DenseNet-backbone learning rate on A5

Only optimization change from A5: DenseNet121 `features` use 0.1 times the
base learning rate throughout training. The hierarchical fusion and all three
prediction heads retain the A5 base learning rate. AdamW, weight decay and the
cosine schedule are otherwise unchanged; the schedule preserves the 0.1 ratio.

This tests whether slower pretrained-feature adaptation reduces destructive
fine-tuning while allowing the randomly initialized fusion/heads to learn at
the established rate. A15's hard freeze/unfreeze improved B/C/D-oriented
metrics but did not reach the gate; A16 avoids the abrupt epoch-6 transition.
An improvement is uncertain and is not assumed.

Same stretch512 cache input, augmentation, dropout, losses, natural sampling,
architecture, fixed grouped split and seed42 as A5. Fixed fold0 only, fresh
ImageNet initialization, full50. Only a completed audited selected DEV
Macro-F1 >=.75 permits fresh folds1--4 while retaining fold0. No ensemble,
resplit or independent-test claim. RTX5090 only; worker2/Vesta excluded.
Final joint criteria remain mean>=.70, sample SD<=.05 and minimum fold>=.65.

Immutable deployment:
`/slurmshared/Ngoc/code/hcmus-density-auggeo-dropout30-backbonelr01-20260920-v1`.
Config SHA256:
`443a5e9128022c8de60960ef948c0094b50dea492e7f57f5af8c831a156b4d06`.
The cluster suite passes 22/22 tests. Preflight validates all five frozen
manifests, reads a finite real FIT tensor with shape `[4,3,512,512]`, and
proves complete/disjoint optimizer coverage: 362/362 backbone parameters at
5e-6 and 20 non-backbone parameters at 5e-5. Parsed config differs from A5
only by arm identity and `backbone_lr_multiplier: 0.1`.
