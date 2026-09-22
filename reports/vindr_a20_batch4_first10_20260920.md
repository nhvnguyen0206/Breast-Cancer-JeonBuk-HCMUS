# A20 batch4 — first 10 epochs

Job943_0 remains running on RTX 5090. All scalar losses through epoch 10 are
finite. The selected checkpoint is epoch 7: Macro-F1 `0.726423`, accuracy
`0.849010`, QWK `0.687734`, class F1 A/B/C/D
`0.666667 / 0.689655 / 0.903537 / 0.645833`, with no severe error.

This is above A5's matched first-10 best (`0.545249`) and also improves its
B/C/D mean, accuracy and QWK, but remains below the preregistered `0.75`
expansion gate. Epoch 10 itself falls to `0.532588`, so no early success is
claimed. Continue the unchanged fold0 run to the mandatory 50 epochs; next
review at epoch 20.
