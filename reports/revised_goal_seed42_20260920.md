# Revised acceptance criterion

User updated explicit success criterion to mean four-class CV5 Macro-F1 >=.70,
using training seed42 only; .75 remains aspirational in the objective heading.
Do not require multiple seeds under this revision or claim cross-seed stability.

Re-ran scripts/audit_density_cv5.py against original A5 runs770-fold0 and
771-fold1--4 with frozen split and live W&B verification: PASS, exit0.
All five source runs finished50; prediction-derived mean .7028282800839902,
sample SD .1172888127211152, accuracy .8373756234184212,
QWK .6707563557578502. Unique DEV union2017; frozen assignment digest
43daa86936ee7b1bae1b200836fb1afdfe0c8294c7c865d8f5758bf989f12a9a.
Local A5 config explicitly specifies seed42.

A5 meets the revised numerical threshold, not a claim of low fold variance.
Fold1/3 remain below .60; A F1 varies0--1 with only6 A cases total.
These are selected DEV scores used in tuning, not an independent test.
The auditor checks stored predictions/checkpoints, not fresh inference.

A13 remains in flight under its registered50-epoch protocol. Do not submit
additional confirmation merely to pursue the superseded acceptance threshold.
Finish and audit the current screen before the next campaign decision; no job
cancelled or new training submitted by this review. Goal remains active.

## Subsequent user-approved stability criteria

The user requested updating the goal to the proposed stability criteria.
All must hold simultaneously: four-class CV5 mean Macro-F1 >=.70,
sample SD <=.05, minimum fold Macro-F1 >=.65, training seed42 only.
Mean >=.75 remains aspirational. A5 fails SD and minimum-fold requirements;
the earlier numerical-threshold result is not campaign completion.
These thresholds are experimental acceptance choices, not universal standards.

Keep architecture, frozen grouped splits, checkpoint selection and four-class
metric definition unchanged. No ensemble, resplitting or dropping weak folds.
Screen fixed fold0 for full50, audit, and expand only if selected DEV >=.75;
one fold cannot establish cross-fold stability. Report class-wise F1, accuracy,
QWK, mean/sample SD/minimum across folds and rare-A limitations. Use only
RTX5090, never Vesta; W&B HCMUS-paper1; updates every10--20 epochs or events.
Continue controlled preprocessing/sampling/weighting/loss/augmentation/LR/
freeze-unfreeze/regularization studies. Selected DEV is not independent test.

The application's goal description could not be edited with exposed tools;
this file records the accepted conversation instructions, not an application
state update. No success declaration while stability requirements are unmet.
