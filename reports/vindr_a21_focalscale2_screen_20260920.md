# A21 focal-scale 2 completed fold0 screen

The audit passes: job949_0 completed 50 epochs on RTX 5090 with exit code 0,
no restart/requeue, fixed manifests and matching finished W&B data.

Selected epoch 30 has Macro-F1 `0.550949`, accuracy `0.831683`, QWK
`0.659494`, class F1 `0.000000 / 0.696629 / 0.890344 / 0.616822`, and no
severe errors. No checkpoint reaches `0.75`; epoch 50 is `0.530210`.

Reject A21 without folds1–4. It trails A5 fold0 by `0.238701`; the modest
focal increase improves neither the primary score nor class-A recognition.
The negative result also agrees directionally with the earlier failed
full-strength focal normalization. Keep A5 as the reference.
