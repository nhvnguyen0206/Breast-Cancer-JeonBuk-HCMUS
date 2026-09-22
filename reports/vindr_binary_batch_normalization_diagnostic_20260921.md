# Binary weighted CE: batch2 normalization diagnostic

Read immutable A5 implementation and frozen FIT manifests; no training active
at this check after A25 completion. Binary CE uses default weighted mean:
sum_i w[y_i]*CE_i / sum_i w[y_i]. Thus weights cancel in homogeneous batches.
This is the implemented objective, not a library bug.

Fold0/3 binary FIT counts AB/CD=161/1452, weights
[1.6747503280639648,.32524967193603516]. Fold1/2/4 counts162/1452,
weights[1.6731934547424316,.32680651545524597]. Under uniformly shuffled
sampling without replacement, homogeneous pairs have probability .82018617
or .81929352. For full pairs the expected AB loss-coefficient mass is
.16047873 or .16119696, compared with .36343950 or .36355212 when
normalizing by a fixed FIT expected weight. These are objective coefficients,
not measured gradient norms or expected F1. The possible final singleton is
excluded from the pair calculation and has negligible but nonzero effect.

Formula: P(AB,AB)+P(mixed)*w_AB/(w_AB+w_CD). PyTorch backward check with
zero logits confirms homogeneous pairs give per-example gradient magnitude
.25 irrespective of weight; mixed pair gives .41829836 vs .08170163 for
fold4 weights. No DEV labels were used to calculate these coefficients.

Implication: current binary class weighting is considerably weaker than a
dataset-normalized weighted objective with this tiny batch. This does not
prove it causes poor multiclass F1 or fold dispersion. All folds have nearly
identical exposure, and binary AB/CD supervision cannot distinguish A from B
or C from D. Further increasing rare-A sampling alone cannot resolve that.

Next controlled candidate: A26, immutable A5 parent, change only binary loss
normalization to fixed FIT expectation. Preserve coefficient .3, all other
losses, heads, architecture, batch2, seed42 and split. Add an opt-in setting
with backward-compatible default; test exact legacy parity, finite gradients,
and partition invariance of the new per-case objective before launch.
Candidate is NOT implemented or submitted by this diagnostic. Preregister
before submission; fold0 full50 first, completed audited>=.75 for expansion,
unchanged CV5 acceptance mean>=.70/sampleSD<=.05/min>=.65. Selected DEV is
not independent test. Do not claim that normalization guarantees improvement.
