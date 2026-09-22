# A12 preregistration

Parent: completed A5, mean selected DEV Macro-F1 .7028282800839902.
Only learning change: focal gamma2 ->1; beta remains .999.
Arm metadata: auggeo_dropout30_gamma1. No label smoothing or ensemble.
Use an immutable copy of the A5 deployment, not the modified worktree.

A11 beta reduction failed CV5 (.6181916009106782), with D-F1 mean
.60017 versus A5 .63572. Retain A5 weights and test focal modulation
separately. Hypothesis: weaker suppression of confident examples may
improve the observed adjacent-class boundary errors. This is unproven;
neither gradient dominance nor improved calibration has been established.

Fixed fold0 screen, fresh ImageNet, seed42, full50 epochs. Freeze existing
grouped density assignments and all preprocessing, augmentation, model,
optimizer and auxiliary-loss settings. RTX5090 only, exclude worker2/Vesta.
After completed screen audit, expand fresh folds1--4 only if selected
four-class DEV Macro-F1 >=.75. Retain screen fold0. Report class F1, BCD,
accuracy, QWK, variability and epoch50 metrics. A gain on the single A case
alone is not broad improvement. No independent test or multi-seed claim.
