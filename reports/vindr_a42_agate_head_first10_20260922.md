# A42 A-gate diagnostic control — common first 10 epochs

Both job-1037 tasks remain RUNNING on master RTX 5090 and have passed epoch
10. Selection below uses only epochs 1--10 independently within each fixed
fold; this is an interim DEV analysis, not a final result.

| Fold | Selected epoch | Macro-F1 | Accuracy | QWK | F1 A/B/C/D |
|---:|---:|---:|---:|---:|---|
| 1 | 5 | 0.580333 | 0.873449 | 0.696890 | 0.0000 / 0.7536 / 0.9219 / 0.6458 |
| 3 | 7 | 0.738565 | 0.851485 | 0.709429 | 0.6667 / 0.7579 / 0.9034 / 0.6263 |

The two-fold mean is `0.6594491`, sample SD `0.1118872`, and minimum
`0.5803329`. A42 therefore does not meet the screen gates at this horizon and
is materially weaker than A41's matched first-10 two-fold mean `0.7692354`,
mostly because fold 1 loses its single A case. This is evidence against the
A-gate as a simple universal repair, but it is not a stopping rule: complete
the registered 50 epochs and audit both runs. Do not expand A42 early.
