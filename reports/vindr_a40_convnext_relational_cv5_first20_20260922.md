# A40 ConvNeXt-Tiny CV5: common first 20 epochs

All five folds are restricted to a matched first-20 horizon. The selected
checkpoints remain unchanged from first10.

| Fold | Best epoch <=20 | Macro-F1 | Accuracy | QWK | F1 A/B/C/D |
|---|---:|---:|---:|---:|---:|
| 0 | 8 | 0.8212558177 | 0.8688118812 | 0.6972285068 | 1.000000 / 0.701299 / 0.917058 / 0.666667 |
| 1 | 4 | 0.8126870715 | 0.8560794045 | 0.6873629019 | 1.000000 / 0.655172 / 0.907051 / 0.688525 |
| 2 | 3 | 0.5439920998 | 0.8287841191 | 0.6332256150 | 0.000000 / 0.743590 / 0.890323 / 0.542056 |
| 3 | 2 | 0.6822455124 | 0.8440594059 | 0.6206403148 | 0.666667 / 0.740741 / 0.904908 / 0.416667 |
| 4 | 1 | 0.7268438333 | 0.8535980149 | 0.6760494298 | 0.666667 / 0.724638 / 0.908228 / 0.607843 |

Mean Macro-F1 is **0.7174048669**, sample SD **0.1132044396**, and minimum
**0.5439920998**. Mean passes, while SD and minimum still fail because fold 2
has not improved after epoch 3. Fold 0 remains healthy at epoch 20 itself
(0.8078927073), whereas the other epoch-20 scores are approximately
0.513--0.533, so optimization trajectories differ substantially by fold.

Continue unchanged to full50 and audits. Do not adapt training specifically
to fold 2 or stop before the registered horizon; completed screen fold 3 did
not select its final checkpoint until epoch 34.
