# A21 focal-scale 2 — first 10 epochs

Job949_0 remains running on RTX 5090 with finite losses. The selected epoch 6
has Macro-F1 `0.550700`, accuracy `0.821782`, QWK `0.665594`, class F1
`0.000000 / 0.666667 / 0.880672 / 0.655462`, and no severe error.

This is only `0.005451` above A5 at the same horizon (`0.545249`) and remains
far below the `0.75` expansion gate. Epoch 10 is `0.534886` with four severe
errors and does not support an early benefit claim. Continue the registered
fold0 run unchanged to 50 epochs; next review at epoch 20.
