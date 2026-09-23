# A53 folds2/3: matched first10

Array job1096 remains active on RTX5090 with worker2/Vesta excluded. Both runs
use the immutable v20 snapshot, frozen split/cache/seed42 and offline W&B
receipts `6irwuqqa`/`82som6u1`. This selected-DEV interim analysis is not an
independent test or final gate decision.

| Run | Selected epoch | Macro-F1 | Accuracy | QWK | F1 A/B/C/D | B/C/D mean | A-positive epochs | Longest A streak | Epochs Macro >= .72 |
|---|---:|---:|---:|---:|---|---:|---:|---:|---:|
| A53/f2 | 9 | .544167 | .831266 | .640763 | .000000/.700000/.891761/.584906 | .725556 | 0/10 | 0 | 0 |
| A53/f3 | 3 | .674287 | .811881 | .608417 | .666667/.539683/.879227/.611570 | .676827 | 2/10 | 2 | 0 |

Selected aggregate Macro-F1 is mean `.6092266`, sample SD `.0920087`, and
minimum `.5441666`; mean accuracy is `.8215733`, mean QWK `.6245904`, and mean
B/C/D `.7011911` with minimum `.6768266`.

The direct A-gate replacement has not reproduced A43's fold2 result. Fold2's
selected epoch predicts no validation A sample correctly and no epoch in the
first ten has positive A F1. Fold3 recovers A only in two consecutive epochs,
while neither fold reaches Macro-F1 `.72`. This contradicts the narrow
preregistered explanation that A42's existing A logit alone was suppressing
the multiscale decision geometry. A more likely mechanism is insufficient
supervision: in A53 the multiscale representation receives gradients only
through the rare A gate, whereas A43 trained that representation from all
heads/tasks.

At first10, both fold Macro gates fail; sample SD fails; B/C/D mean and minimum
fail; QWK mean fails; QWK minimum alone passes. Do not retune or stop the
registered run: continue unchanged to epoch20/40/50 and queued read-only
audits1098/1099. Folds0/1/4 remain locked.
