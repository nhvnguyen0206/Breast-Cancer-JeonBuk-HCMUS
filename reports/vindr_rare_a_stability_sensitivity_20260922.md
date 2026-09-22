# Sensitivity of the CV5 stability gate to rare density A

The frozen split is balanced as far as the data permit, but it contains only
six density-A exams: folds 0/1/2/4 contain one each and fold 3 contains two.
Every fold otherwise contains about 39--40 B, 311--312 C and 51--52 D exams.
Consequently, one A decision can move a fold's four-class Macro-F1 by roughly
0.17--0.25, far more than ordinary B/C/D errors.

## A41 fold-2 counterfactual

A41 fold 2 has B/C/D F1 `0.732394 / 0.904762 / 0.596154` and A F1 `0`, giving
Macro-F1 `0.5583275`. Holding every B/C/D prediction and every other fold
fixed, only the fold-2 A F1 is varied below.

| Fold-2 A F1 | Fold-2 Macro-F1 | CV5 mean | CV5 sample SD | CV5 minimum |
|---:|---:|---:|---:|---:|
| 0.0000 | 0.558328 | 0.752309 | 0.118742 | 0.558328 |
| 0.4000 | 0.658328 | 0.772309 | 0.080003 | 0.658328 |
| 0.5000 | 0.683328 | 0.777309 | 0.071420 | 0.683328 |
| 0.6667 | 0.724994 | 0.785642 | 0.059077 | 0.717096 |
| 1.0000 | 0.808328 | 0.802309 | 0.048497 | 0.717096 |

With all other A41 outputs frozen, the registered SD <= `0.05` gate passes
only when the single fold-2 A case has F1 `1.0`, which requires predicting it
correctly without an A false positive. A plausible A F1 of `0.6667` repairs
the minimum and raises the mean, but still leaves SD at `0.0591`.

## Interpretation rule

The stability gate is retained and must not be weakened after observing DEV.
However, passing or failing it is highly sensitive to one sample and therefore
cannot by itself establish robust density-A generalization. Every A42/A43
decision must report the A confusion contribution separately, alongside
B/C/D F1, accuracy and QWK. Architecture changes should be accepted only when
they preserve substantive B/C/D performance and do not merely memorize or
flip the six A exams.
