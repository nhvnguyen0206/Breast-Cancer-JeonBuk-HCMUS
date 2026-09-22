# A34 fold-0 first-10 review

Job 997 remains RUNNING on permitted RTX 5090 hardware, with worker2/Vesta
excluded and no restart/requeue. Ten epochs completed with finite losses.
This is selected DEV, not independent evaluation.

Best-through-10 is epoch 6: Macro-F1 **0.6290481887**, accuracy 0.8118811881,
QWK 0.6551662174, class F1 A/B/C/D
[0.400000, 0.595745, 0.878939, 0.641509], and zero severe errors. Epoch 10
Macro-F1 is 0.4882642252; cumulative AMP skipped updates are 1.

At the matched horizon, A34 is above A30 (0.5896463748) but below direct
parent A6 (0.7829792575) and below the 0.70 expansion gate. Do not stop or
expand based on this early checkpoint. Continue the preregistered fold-0 run
unchanged; next score review at epoch 20.
