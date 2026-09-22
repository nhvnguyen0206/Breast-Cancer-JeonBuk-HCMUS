# A34 fold-0 first-20 review

Job 997 remains RUNNING on permitted RTX 5090 hardware, with worker2/Vesta
excluded and no restart/requeue. Twenty epochs completed with finite losses.
This is selected DEV, not independent evaluation.

Best-through-20 remains epoch 6: Macro-F1 **0.6290481887**, accuracy
0.8118811881, QWK 0.6551662174, class F1 A/B/C/D
[0.400000, 0.595745, 0.878939, 0.641509], and zero severe errors. Epoch 20
Macro-F1 is 0.5103016099; cumulative AMP skipped updates are 0.

A34 remains below the 0.70 expansion gate and trails both A6 (0.7829792575)
and A30 (0.7025951909) at the matched first-20 horizon. Continue the
preregistered fold-0 run unchanged through 50 epochs; do not launch folds
1–4. Next score review at epoch 40.
