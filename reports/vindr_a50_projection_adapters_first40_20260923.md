# A50 folds2/3: matched first40

Training array job1078 remains active on RTX5090 with worker2/Vesta excluded.
Both histories contain complete finite epochs1--40 under the immutable v17
snapshot, frozen split/cache/seed42 and offline W&B receipts
`h663tspa`/`dwm4ttxc`. This is selected DEV evidence, not an independent test
or final audit.

| Run | Selected epoch | Macro-F1 | Accuracy | QWK | F1 A/B/C/D | B/C/D mean | A-positive epochs | Macro >= .72 epochs | Adapter CC/MLO L2 |
|---|---:|---:|---:|---:|---|---:|---:|---:|---|
| A50/f2 | 4 | .539110 | .838710 | .630947 | .000000/.695652/.900787/.560000 | .718813 | 0/40 | 0 | .217559/.212518 |
| A50/f3 | 40 | .726897 | .858911 | .681406 | .666667/.720000/.912226/.608696 | .746974 | 8/40 | 1 | .754466/.705281 |

At the common horizon, Macro-F1 mean is `.6330034`, sample SD `.1327855`,
minimum `.5391099`, accuracy mean `.8488103`, QWK mean/minimum
`.6561764/.6309472`, and B/C/D mean/minimum `.7328935/.7188132`.

Fold3 materially improves at epoch40: it is A50's first epoch above `.72`,
passes its individual Macro gate and has stronger B/C/D and QWK than its
first20 checkpoint. Its adapter norms also grow, confirming continued use of
the projection-specific path. This does not rescue the treatment: fold2's
checkpoint remains epoch4, with zero positive-A epochs and zero epochs above
`.72`. The resulting SD exceeds the `.03` gate by `.1027855`; the QWK mean is
also `.0010573` below its registered gate. B/C/D and QWK minimum gates pass.

Epoch40 Macro-F1 is `.4879792/.7268970` on folds2/3. Continue unchanged to
epoch50 and the queued read-only audits. Folds0/1/4 remain locked regardless
of the isolated fold3 recovery.
