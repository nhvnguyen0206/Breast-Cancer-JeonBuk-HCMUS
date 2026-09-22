# A51 folds2/3: matched first20

Array job1084 remains healthy on RTX5090 under the immutable v18 protocol.
This selected-DEV interim analysis uses only epochs1--20 and does not alter the
running experiment.

The selected checkpoints remain epoch7 on both folds:

| Run | Macro-F1 | Accuracy | QWK | F1 A/B/C/D | B/C/D mean | A-positive epochs | Longest A streak | Epochs Macro >= .72 |
|---|---:|---:|---:|---|---:|---:|---:|---:|
| A51/f2 | .615598 | .799007 | .625975 | .400000/.642857/.870861/.548673 | .687464 | 1/20 | 1 | 0 |
| A51/f3 | .728170 | .831683 | .677823 | .666667/.780488/.889256/.576271 | .748672 | 8/20 | 3 | 3 |

Aggregate selected Macro-F1 is unchanged at mean `.6718841`, sample SD
`.0796010` and minimum `.6155977`; mean B/C/D is `.7180676` and mean QWK is
`.6518994`. Fold3 has added two more epochs at or above `.72` and three more
positive-A epochs since the first10 window, but none exceeds its epoch7
checkpoint. Fold2's sole positive-A epoch remains epoch7, so the intended
bilateral treatment has not yet made the weak fold's rare-A boundary stable.
Epoch20 itself falls to `.5139056/.5315171` with A F1 zero on both folds; this
does not replace the preregistered best-checkpoint selection.

Fold2 Macro, sample SD, B/C/D mean and QWK mean gates still fail. Continue the
unchanged full50 run and inspect next at epoch40; folds0/1/4 remain locked.
