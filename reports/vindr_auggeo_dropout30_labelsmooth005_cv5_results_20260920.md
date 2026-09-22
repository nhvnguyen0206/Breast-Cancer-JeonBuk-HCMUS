# A10: completed CV5, selected DEV

All five folds completed50. Full audit PASS: frozen manifest membership,
checkpoint/config consistency, recomputed prediction metrics and finished
W&B source runs. No independent test and no multi-seed verification.

- Mean four-class Macro-F1: 0.689215343247612
- Sample SD: 0.09759107813789597
- Mean accuracy: 0.8314387145910621
- Mean QWK: 0.6398358961418336
- Mean class F1 A/B/C/D: .6133333 / .6476420 / .8928492 / .6030368
- Mean BCD F1: .7145093466
- Mean epoch50 Macro-F1: .5752920922
- Selected fold scores: .7743056 / .5605285 / .7777575 / .7189234 / .6145617

A10 is 1.3613 percentage points below A5's .7028282801. Its BCD mean is
also below A5's .7371043734. Do not promote smoothing .05; retain A5 as
best substantive parent. Next candidate A11 changes beta only on A5,
screening fixed fold0 first under the preregistered protocol.

Summary: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/jjjwj8l0
Exact audit is in the adjacent JSON report. This audit does not redo image
inference or establish anatomical crop/label correctness.
