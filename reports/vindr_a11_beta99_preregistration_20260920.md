# A11 preregistration

Submission update: after A10 completed and passed its audit, A11 fixed
fold0 was submitted as830_0. Startup confirms RTX5090 on master with
worker2 excluded. Original preregistration below predates submission.

Prepared while A10 array808 remains RUNNING. Finish and audit A10 before
deciding whether to launch this candidate. No new training job is started.

Parent: A5, not A10. Only learning-config change: loss.beta .999 -> .99.
Local parsed-config comparison confirms only loss.beta and experiment.arm
differ. The same beta controls both flat and binary effective-number weights;
this is a class-weight-group experiment, not an isolated flat-head change.
No label smoothing. Preserve architecture, split/seed42, cache, augmentation,
natural sampling, dropout .3, optimizer and 50-epoch protocol.

Motivation: in fold1 FIT counts [5,157,1244,208], observed-class weight ratios
A/B decrease from 29.1308 to 16.1925 and A/C from 142.6751 to 20.4039.
These ratios are not aggregate loss or gradient contributions. Test whether
less extreme weighting improves B/C/D generalization without unacceptable
A degradation. A3 tried beta .99 on A1, not A5; the interaction with A5's
dropout remains untested. No guaranteed improvement is claimed.

Screen fixed fold0 for full50 with fresh ImageNet initialization on RTX5090,
exclude Vesta/worker2. Record W&B HCMUS-paper1. Audit selected checkpoint,
predictions, frozen split and finished50 before expansion; expand only if
selected four-class DEV Macro-F1 >=.75. Report A and B/C/D separately,
accuracy, QWK, severe errors and epoch50 score. Passing this numeric gate
does not establish substantive improvement or independent-test performance.

If expanded, compare mean per-fold Macro-F1/sample SD against A5 and A10.
Do not cherry-pick folds, move rare cases or ensemble. The goal remains
mean >=.75 plus stability across seeds, not a successful fold0 screen.
