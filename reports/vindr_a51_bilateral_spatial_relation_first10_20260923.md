# A51 folds2/3: matched first10

Training array job1084 remains active on RTX5090 with worker2/Vesta excluded.
Both runs use the read-only v18 snapshot, frozen split/cache/seed42 and offline
W&B receipts `5hzj03pt` (fold2) and `oeauqr5m` (fold3). This is an interim
selected-DEV analysis through epoch10, not an independent test or a final
gate decision.

| Run | Selected epoch | Macro-F1 | Accuracy | QWK | F1 A/B/C/D | B/C/D mean | A-positive epochs | Epochs Macro >= .72 |
|---|---:|---:|---:|---:|---|---:|---:|---:|
| A51/f2 | 7 | .615598 | .799007 | .625975 | .400000/.642857/.870861/.548673 | .687464 | 1/10 | 0 |
| A51/f3 | 7 | .728170 | .831683 | .677823 | .666667/.780488/.889256/.576271 | .748672 | 5/10 | 1 |

The selected two-fold Macro-F1 mean is `.6718841`, sample SD `.0796010` and
minimum `.6155977`; mean accuracy is `.8153453`, mean QWK `.6518994`, and mean
B/C/D F1 `.7180676`. Relative to matched A42 first10, A51 improves fold2 by
about `.00942` but lowers fold3 by about `.01039`, leaving the mean essentially
unchanged (about `-.00049`) while reducing the spread from about `.09361` to
`.07960`.

The new path is active: its zero-initialized exam output-projection L2 norm is
`1.283545` on fold2 and `1.181045` on fold3 at both selected epoch7
checkpoints. Fold2 has recovered a positive A decision in one epoch, unlike
A50's zero through epoch10, while fold3 has five positive-A epochs and one
epoch above `.72`.

At this horizon fold2 still fails its `.72` Macro gate, sample SD fails `.03`,
B/C/D mean misses its registered threshold by about `.00363`, and QWK mean
misses by about `.00533`; fold3 Macro and both B/C/D/QWK minimum gates pass.
Continue unchanged to epoch20/40/50. Folds0/1/4 remain locked.
