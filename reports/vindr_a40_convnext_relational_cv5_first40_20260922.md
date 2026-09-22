# A40 ConvNeXt-Tiny CV5: common first 40 epochs

At the common first-40 horizon, fold 3 adopts its known epoch-34 checkpoint;
the other four fold selections remain unchanged.

| Fold | Best epoch <=40 | Macro-F1 | Accuracy | QWK | F1 A/B/C/D |
|---|---:|---:|---:|---:|---:|
| 0 | 8 | 0.8212558177 | 0.8688118812 | 0.6972285068 | 1.000000 / 0.701299 / 0.917058 / 0.666667 |
| 1 | 4 | 0.8126870715 | 0.8560794045 | 0.6873629019 | 1.000000 / 0.655172 / 0.907051 / 0.688525 |
| 2 | 3 | 0.5439920998 | 0.8287841191 | 0.6332256150 | 0.000000 / 0.743590 / 0.890323 / 0.542056 |
| 3 | 34 | 0.6936746863 | 0.8316831683 | 0.6251807788 | 0.666667 / 0.647887 / 0.894488 / 0.565657 |
| 4 | 1 | 0.7268438333 | 0.8535980149 | 0.6760494298 | 0.666667 / 0.724638 / 0.908228 / 0.607843 |

Mean Macro-F1 rises slightly to **0.7196907017**, sample SD is
**0.1124297521**, and minimum remains **0.5439920998**. Only the mean gate
passes. Fold 2 has not improved for 37 epochs and is very unlikely to clear
the minimum gate, but all runs must finish the registered 50 epochs and pass
audit before the arm is formally accepted or rejected.

Fold 0 remains strong even at epoch 40 (0.7924361985), whereas folds 1--4
score 0.4952--0.5489 at epoch 40. The persistent trajectory split is evidence
that replacing only the backbone does not solve cross-fold stability.
