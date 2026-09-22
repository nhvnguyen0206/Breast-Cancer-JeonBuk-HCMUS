# A40 ConvNeXt-Tiny CV5: common first 30 epochs

At the matched first-30 horizon, no fold improves its selected checkpoint.

| Fold | Best epoch <=30 | Macro-F1 | Accuracy | QWK | F1 A/B/C/D |
|---|---:|---:|---:|---:|---:|
| 0 | 8 | 0.8212558177 | 0.8688118812 | 0.6972285068 | 1.000000 / 0.701299 / 0.917058 / 0.666667 |
| 1 | 4 | 0.8126870715 | 0.8560794045 | 0.6873629019 | 1.000000 / 0.655172 / 0.907051 / 0.688525 |
| 2 | 3 | 0.5439920998 | 0.8287841191 | 0.6332256150 | 0.000000 / 0.743590 / 0.890323 / 0.542056 |
| 3 | 2 | 0.6822455124 | 0.8440594059 | 0.6206403148 | 0.666667 / 0.740741 / 0.904908 / 0.416667 |
| 4 | 1 | 0.7268438333 | 0.8535980149 | 0.6760494298 | 0.666667 / 0.724638 / 0.908228 / 0.607843 |

Mean Macro-F1 remains **0.7174048669**, sample SD **0.1132044396**, and
minimum **0.5439920998**. Fold 2 has now gone 27 epochs without improving its
epoch-3 selection, making final stability failure increasingly likely.

Fold 0 remains qualitatively different: epoch 30 itself scores 0.7864934019,
while folds 1--4 score 0.5096--0.5498 at epoch 30. This suggests the backbone
replacement can be strong but is highly sensitive to fold-specific training
dynamics. Continue unchanged to full50/audit. Do not tune or stop selectively.
