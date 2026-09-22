# A37 spatial-token attention common first-20 review

Both fixed stress folds reached epoch 20 normally. Neither selected score
improved after epoch 10.

| Fold | Best epoch | Macro-F1 | Accuracy | F1 A/B/C/D | QWK |
|---|---:|---:|---:|---|---:|
| 1 | 1 | 0.570846 | 0.863524 | 0.0000 / 0.6667 / 0.9140 / 0.7027 | 0.693358 |
| 3 | 3 | 0.619532 | 0.811881 | 0.3636 / 0.6154 / 0.8837 / 0.6154 | 0.670562 |

Mean remains 0.595189, sample SD 0.034426 and minimum 0.570846. The absence
of improvement over ten additional epochs weakens the slow-convergence
hypothesis. A37 remains materially below A36 and fails both expansion gates.

Continue unchanged to epoch 50 for audit; do not expand. If final A37 fails,
the next structural hypothesis should target the prediction head rather than
add more fusion capacity: replace flat four-class inference with a proper
ordinal-primary head whose thresholds are monotonically constrained, while
keeping one model and one inference path.

