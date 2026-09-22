# A40 ConvNeXt-Tiny CV5: common first 10 epochs

This preliminary aggregate restricts every fold to the same first-10 horizon.
Job1022 supplies the preserved screen folds 1/3 and job1024 supplies expansion
folds 0/2/4. All tasks use the same immutable model/config/split/seed and run
on permitted RTX 5090 nodes. These are selected DEV results, not independent
test estimates and not final audited CV5 results.

| Fold | Best epoch <=10 | Macro-F1 | Accuracy | QWK | F1 A/B/C/D |
|---|---:|---:|---:|---:|---:|
| 0 | 8 | 0.8212558177 | 0.8688118812 | 0.6972285068 | 1.000000 / 0.701299 / 0.917058 / 0.666667 |
| 1 | 4 | 0.8126870715 | 0.8560794045 | 0.6873629019 | 1.000000 / 0.655172 / 0.907051 / 0.688525 |
| 2 | 3 | 0.5439920998 | 0.8287841191 | 0.6332256150 | 0.000000 / 0.743590 / 0.890323 / 0.542056 |
| 3 | 2 | 0.6822455124 | 0.8440594059 | 0.6206403148 | 0.666667 / 0.740741 / 0.904908 / 0.416667 |
| 4 | 1 | 0.7268438333 | 0.8535980149 | 0.6760494298 | 0.666667 / 0.724638 / 0.908228 / 0.607843 |

Common-first10 mean Macro-F1 is **0.7174048669**, sample SD
**0.1132044396**, and minimum **0.5439920998**. Only the mean gate passes;
the SD and minimum gates fail because fold 2 has not recovered its single
class-A case and has lower D F1. This reverses which fold is the current
bottleneck and confirms why the five-fold expansion was necessary.

The result is too early for rejection: in the completed screen, fold 3 did
not reach its selected checkpoint until epoch 34. Continue all expansion runs
unchanged to at least common20 and ultimately full50/audit. Do not tune on
fold 2 or replace the frozen split.
