# A52 folds2/3: matched first10

Array job1090 remains active on RTX5090 with worker2/Vesta excluded. Both runs
use the immutable v19 snapshot, frozen split/cache/seed42 and offline W&B
receipts `o8i8cjx5`/`q6zqr8i4`. This selected-DEV interim analysis is not an
independent test or final gate decision.

| Run | Selected epoch | Macro-F1 | Accuracy | QWK | F1 A/B/C/D | B/C/D mean | A-positive epochs | Longest A streak | Epochs Macro >= .72 |
|---|---:|---:|---:|---:|---|---:|---:|---:|---:|
| A52/f2 | 7 | .603462 | .781638 | .610149 | .400000/.622222/.857143/.534483 | .671283 | 1/10 | 1 | 0 |
| A52/f3 | 7 | .718049 | .809406 | .664206 | .666667/.746988/.870307/.588235 | .735177 | 4/10 | 2 | 0 |

Selected aggregate Macro-F1 is mean `.6607556`, sample SD `.0810255`, and
minimum `.6034620`; mean accuracy is `.7955218`, mean QWK `.6371771`, and mean
B/C/D `.7032297`. Relative to matched A42 first10, both folds are lower
(about `-.00271/-.02052`), so the new expert has not yet reproduced A43's
fold2 gain. Relative to A51 first10, mean is about `.01113` lower with
essentially the same spread and slightly less persistent fold3 A behavior.

The treatment is active rather than stuck at its zero initialization: selected
A-expert output-projection norms are `.174012/.173561`. Nevertheless, fold2's
A region appears in only one isolated epoch, and neither fold reaches `.72`.
Both Macro gates, SD, B/C/D mean/minimum, and QWK mean currently fail; QWK
minimum alone passes. Continue unchanged to epoch20/40/50, with folds0/1/4
locked.
