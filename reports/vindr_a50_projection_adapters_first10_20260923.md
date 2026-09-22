# A50 folds2/3: matched first10

Training array job1078 remains active on RTX5090 with worker2/Vesta excluded.
Both runs use the immutable v17 snapshot, frozen split/cache/seed42 and offline
W&B receipts `h663tspa` (fold2) and `dwm4ttxc` (fold3). This is an interim
selected-DEV analysis through epoch10, not an independent test or a final gate.

| Run | Selected epoch | Macro-F1 | Accuracy | QWK | F1 A/B/C/D | B/C/D mean | A-positive epochs | Epochs Macro >= .72 |
|---|---:|---:|---:|---:|---|---:|---:|---:|
| A50/f2 | 4 | .539110 | .838710 | .630947 | .000000/.695652/.900787/.560000 | .718813 | 0/10 | 0 |
| A50/f3 | 3 | .698196 | .804455 | .638305 | .666667/.647059/.869128/.609929 | .708705 | 4/10 | 0 |

The selected two-fold mean is `.6186527`, sample SD `.1124905`, minimum
`.5391099`, mean accuracy `.8215826`, mean QWK `.6346259`, and mean B/C/D F1
`.7137592`. No fold has reached the `.72` Macro-F1 screen. Relative to matched
A42/A49 first10, A50 mean is `.0401111` lower and its minimum is `.0671737`
lower. Fold2 never predicts its single A correctly; fold3's A signal appears
in four epochs with a longest initial streak of three and then disappears.

Both adapters are active rather than stuck at initialization. At the selected
checkpoints, CC/MLO output-projection L2 norms are `.217559/.212518` on fold2
and `.184555/.177149` on fold3. This proves optimization activity, not a
generalization benefit.

A50 currently fails both per-fold Macro gates and the SD gate. Continue the
preregistered run unchanged to epoch20/40/50; folds0/1/4 remain locked.
