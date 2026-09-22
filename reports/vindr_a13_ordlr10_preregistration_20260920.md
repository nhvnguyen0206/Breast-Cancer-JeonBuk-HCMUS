# A13 preregistration

Parent A5 completed mean selected DEV Macro-F1 .7028282800839902.
Only learning change: ordinal_bias learning-rate multiplier10 (5e-4 initial
versus5e-5 for every other parameter). Same cosine schedule, weight_decay,
loss weights, gamma2/beta.999, dropout.3, augmentation, stretch512 and cache.
AdamW bias decay per update also scales with LR; this is not isolated from
the bias optimizer change. Architecture and scalar ordinal score unchanged.

Hypothesis: faster threshold separation may reduce the fixed-bias ordinal
loss floor identified in the diagnostic. Whether this improves four-class
generalization is unknown; scalar loss magnitude is not gradient dominance.

Immutable A5 deployment copy with only optimizer builder/engine integration
and new config. Fixed fold0, fresh ImageNet, seed42, full50 epochs. Same
grouped density split; RTX5090 assertion and worker2/Vesta exclusion.
Only after completed audit and selected four-class DEV Macro-F1 >=.75,
expand fresh folds1--4 and retain screened fold0. No ensemble. Assess
per-class/BCD, accuracy/QWK, fold variance and epoch50, not A improvement
alone. Goal requires CV5>=.75 plus multiple-seed stability; no independent
test claim. Report every10--20 epochs. Three optimizer unit tests passed.
