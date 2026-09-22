# A25 diagnostic: marginal neighbor risk (FIT only)

Computed directly from frozen FIT manifests and the implemented cost matrix.
Expected neighbor loss for constant hard predictions A/B/C/D:

| Fold | A | B | C | D |
| --- | --- | --- | --- | --- |
| 0 | 3.053937 | 1.481711 | .539368 | 2.572846 |
| 1 | 3.053903 | 1.481413 | .541822 | 2.570942 |
| 2 | 3.052664 | 1.480793 | .539963 | 2.572800 |
| 3 | 3.054557 | 1.481091 | .538438 | 2.571296 |
| 4 | 3.052664 | 1.480793 | .539963 | 2.572800 |

This is sum_y FIT_frequency(y)*cost(y,prediction), not measured model
performance. Every fold's feature-independent optimum is C. For fold0,
the constant-C term contributes .107874 at coefficient .2 versus .053937
at coefficient .1. Lowering the coefficient changes its relative strength,
not its preferred constant class. This supports testing objective interaction
but does not establish that neighbor loss causes actual D->C errors: a
feature-dependent classifier can minimize this loss with correct predictions.
Near-identical risks across folds also do not explain fold dispersion alone.

Interpret A25 using completed audited four-class Macro-F1 plus B/C/D F1 and
confusion counts, not training loss magnitude (which necessarily decreases
for fixed outputs when the coefficient is halved). Do not modify the fixed
selection rule or .75 screening gate in response to this diagnostic.
