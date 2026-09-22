# A48 folds2/3: matched first10

Both Slurm job1066 tasks remain RUNNING on `slurm-b20a-master-0` RTX5090.
Each history contains complete epochs1--10 with finite losses and no runtime
error markers. Values below select best DEV Macro-F1 independently within the
same first-ten-epoch horizon on the frozen cache/split and seed42.

| Arm/fold | Epoch | Macro-F1 | Accuracy | QWK | F1 A/B/C/D | B/C/D mean | A-positive epochs | D-head norm |
|---|---:|---:|---:|---:|---|---:|---:|---:|
| A42/f2 | 8 | .606175 | .774194 | .606120 | .4/.641026/.850340/.533333 | .674900 | 1/10 | n/a |
| A42/f3 | 7 | .738565 | .851485 | .709429 | .666667/.757895/.903437/.626263 | .762531 | 4/10 | n/a |
| A48/f2 | 3 | .540083 | .831266 | .627450 | 0/.685714/.892800/.581818 | .720111 | 0/10 | .015358 |
| A48/f3 | 6 | .738368 | .858911 | .701292 | .666667/.750000/.910543/.626263 | .762269 | 5/10 | .022067 |

| Aggregate | A42 | A48 | Delta A48-A42 |
|---|---:|---:|---:|
| Macro-F1 mean | .672370 | .639226 | -.033144 |
| Macro-F1 sample SD | .093614 | .140209 | +.046594 |
| Minimum Macro-F1 | .606175 | .540083 | -.066092 |
| B/C/D mean across folds | .718716 | .741190 | +.022474 |
| B/C/D minimum | .674900 | .720111 | +.045211 |
| QWK mean | .657775 | .664371 | +.006597 |
| QWK minimum | .606120 | .627450 | +.021331 |

The registered representation hypothesis is partially supported: fold2 D F1
improves by .048485, its B and C F1 also improve, and both B/C/D and QWK
aggregate gates already pass. Fold3 is essentially preserved. However, fold2
has zero A-positive epochs and loses its single A case at the selected epoch;
that alone removes .1 from its four-class Macro-F1 relative to an otherwise
strong B/C/D result. Consequently fold2 fails the per-fold .72 gate and the
two-fold sample SD .140209 fails the .03 gate. Fold3 alone passes .72.

The learned D projection norms confirm that the initially exact-zero treatment
is active. No gate is evaluated as final at this early horizon. Continue both
registered runs unchanged to20/40/50, without tuning on either screen fold or
launching folds0/1/4. These are selected DEV results, not an independent test.
W&B remains offline locally on Atlas (run IDs `qai5n15b` and `3ppb7vks`).
