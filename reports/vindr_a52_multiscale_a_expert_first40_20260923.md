# A52 folds2/3: matched first40

Array job1090 remains healthy on RTX5090 under the immutable v19 protocol.
This selected-DEV interim analysis is restricted to epochs1--40.

| Run | Selected epoch | Macro-F1 | Accuracy | QWK | F1 A/B/C/D | B/C/D mean | A-positive epochs | Longest A streak | Epochs Macro >= .72 |
|---|---:|---:|---:|---:|---|---:|---:|---:|---:|
| A52/f2 | 7 | .603462 | .781638 | .610149 | .400000/.622222/.857143/.534483 | .671283 | 1/40 | 1 | 0 |
| A52/f3 | 19 | .730541 | .856436 | .687798 | .666667/.727273/.909667/.618557 | .751832 | 8/40 | 3 | 1 |

The selected checkpoints and aggregate remain unchanged from first20: Macro
mean `.6670014`, sample SD `.0898583`, minimum `.6034620`; mean accuracy
`.8190367`, mean QWK `.6489734`, and mean B/C/D `.7115574`. Fold3 records only
one additional positive-A epoch after epoch20, and epoch40 itself has A F1 zero
on both folds.

The expert is learned and non-zero, but all selected improvement remains on the
stronger fold. Fold2 has no checkpoint gain after epoch7, no epoch at or above
`.72`, and no recurrence of its A region. Fold2 Macro, SD, B/C/D mean/minimum
and QWK mean gates fail. Finish epoch50 and audits1092/1093; folds0/1/4 remain
locked. A53 was preregistered before this first40 inspection and stays
Atlas/training-locked pending audited A52 rejection.
