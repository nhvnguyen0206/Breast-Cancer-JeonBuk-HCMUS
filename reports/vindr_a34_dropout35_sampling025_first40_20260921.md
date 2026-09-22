# A34 fold-0 first-40 review

Job 997 remains RUNNING on permitted RTX 5090 hardware, with worker2/Vesta
excluded and no restart/requeue. Forty epochs completed with finite losses.
This is selected DEV, not independent evaluation.

Best-through-40 improved at epoch 33 to Macro-F1 **0.7779130831**, accuracy
0.8391089109, QWK 0.6138535927, class F1 A/B/C/D
[1.000000, 0.589744, 0.899687, 0.622222], and one severe error. Epoch 40
Macro-F1 is 0.5245655142; cumulative AMP skipped updates are 0.

A34 now exceeds the numerical 0.70 screen gate and is close to parent A6's
matched/final fold-0 score 0.7829792575. The gain since epoch 20 depends in
part on the single class-A DEV study, so it is not evidence of cross-fold
stability. Continue unchanged through epoch 50, then audit the saved
checkpoint and W&B record before any folds 1–4 are submitted.
