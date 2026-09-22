# A43 CV5 common first40

Selection: independent best DEV Macro-F1 within epochs1--40, same horizon
for all folds. Expansion remains running; these are not independent test scores.

| Fold | Epoch | Macro-F1 | Accuracy | QWK | F1 A/B/C/D |
|---:|---:|---:|---:|---:|---|
| 0 | 6 | .816001 | .841584 | .694806 | 1/.703297/.894040/.666667 |
| 1 | 4 | .585024 | .811414 | .693671 | .2/.577778/.884354/.677966 |
| 2 | 7 | .799443 | .836228 | .668040 | 1/.715789/.892508/.589474 |
| 3 | 35 | .719963 | .844059 | .668921 | .666667/.702703/.900958/.609524 |
| 4 | 35 | .775651 | .801489 | .608852 | 1/.717949/.867987/.516667 |

Mean .7392162928, sample SD .0935365942, min .5850244052.
Mean accuracy .8269550156, QWK .6668580236, B/C/D F1 .7278439459.
Only the mean gate passes. Fold1 remains the bottleneck. Fold4's improvement
over its first30 checkpoint is A-driven, with lower accuracy/QWK/B/C/D.
Continue the registered50 and audit before a final architecture decision.
