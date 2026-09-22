# A20 batch4 — first 40 epochs

Job943_0 remains healthy on RTX 5090. The selected checkpoint remains epoch 13
with Macro-F1 `0.773328`; no checkpoint in epochs 14–40 improves it. Epoch 40
is `0.509356`, and only one of 40 checkpoints reaches `0.75`.

A20 remains below A5 fold0's `0.789650`. Continue unchanged through epoch 50,
then run the complete screen audit. Do not submit confirmation folds before
that audit.
