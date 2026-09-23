# A52 folds2/3: matched first20

Array job1090 remains healthy on RTX5090 under the immutable v19 protocol.
This selected-DEV interim analysis is fixed to epochs1--20 and does not alter
the running experiment.

| Run | Selected epoch | Macro-F1 | Accuracy | QWK | F1 A/B/C/D | B/C/D mean | A-positive epochs | Longest A streak | Epochs Macro >= .72 |
|---|---:|---:|---:|---:|---|---:|---:|---:|---:|
| A52/f2 | 7 | .603462 | .781638 | .610149 | .400000/.622222/.857143/.534483 | .671283 | 1/20 | 1 | 0 |
| A52/f3 | 19 | .730541 | .856436 | .687798 | .666667/.727273/.909667/.618557 | .751832 | 7/20 | 2 | 1 |

Fold3 improves at epoch19, but fold2 remains unchanged at epoch7. Selected
aggregate Macro-F1 is mean `.6670014`, sample SD `.0898583`, and minimum
`.6034620`; mean accuracy is `.8190367`, mean QWK `.6489734`, and mean B/C/D
`.7115574`. Relative to first10, mean rises only `.0062458` while SD worsens by
`.0088329` because all improvement occurs on the stronger fold.

The selected A-expert head norm grows from `.173561` to `.347079` on fold3,
but fold2 remains `.174012` and its single positive-A epoch has not recurred.
Fold3 now passes its Macro gate once; fold2 Macro, SD, B/C/D mean/minimum and
QWK mean still fail. Continue unchanged to epoch40/50 and audits; folds0/1/4
remain locked.
