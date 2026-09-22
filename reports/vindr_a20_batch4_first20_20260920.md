# A20 batch4 — first 20 epochs

Job943_0 remains running on RTX 5090 with finite scalar losses. The selected
checkpoint improves to epoch 13: Macro-F1 `0.773328`, accuracy `0.816832`, QWK
`0.612385`, class F1 A/B/C/D
`1.000000 / 0.648649 / 0.881029 / 0.563636`, with no severe errors.

One of the first 20 checkpoints reaches `0.75`. The selected score is
`0.007886` above A5 at the same horizon (`0.765442`), and its B/C/D mean is
also higher, but the result still depends on the single fold0 class-A case.
Epoch 20 itself is `0.521790`; finish all 50 epochs and audit before deciding
whether to expand folds 1–4.
