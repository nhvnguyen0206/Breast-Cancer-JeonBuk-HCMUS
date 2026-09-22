# A50 folds2/3: matched first20

Training array job1078 remains active on RTX5090 with worker2/Vesta excluded.
Both histories contain complete finite epochs1--20 under the frozen v17
snapshot, split/cache/seed42 and offline W&B receipts `h663tspa`/`dwm4ttxc`.
This is selected DEV evidence, not an independent test or final audit.

| Run | Selected epoch | Macro-F1 | Accuracy | QWK | F1 A/B/C/D | B/C/D mean | A-positive epochs | Macro >= .72 epochs |
|---|---:|---:|---:|---:|---|---:|---:|---:|
| A50/f2 | 4 | .539110 | .838710 | .630947 | .000000/.695652/.900787/.560000 | .718813 | 0/20 | 0 |
| A50/f3 | 3 | .698196 | .804455 | .638305 | .666667/.647059/.869128/.609929 | .708705 | 5/20 | 0 |

The selected aggregate remains unchanged from first10: Macro-F1 mean
`.6186527`, sample SD `.1124905`, minimum `.5391099`, accuracy mean
`.8215826`, QWK mean/minimum `.6346259/.6309472`, and B/C/D mean/minimum
`.7137592/.7087051`. Fold2 has no positive-A epoch; fold3 has five with a
longest streak of three. Neither fold has any epoch at or above `.72`.

Epoch20 itself reaches only `.5032574/.6734800` Macro-F1 on folds2/3. The
selected CC/MLO adapter output norms remain `.217559/.212518` and
`.184555/.177149`; no later checkpoint replaced the first10 selections.
Accumulated AMP skipped updates are 11/12 and every recorded loss/metric is
finite.

A50 fails both fold Macro gates and the SD gate at this horizon. Continue the
registered run unchanged to epoch40/50 and final audits. Folds0/1/4 remain
locked. A51 was preregistered before this first20 inspection.
