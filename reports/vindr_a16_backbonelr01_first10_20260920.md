# A16 backbone-LR 0.1x — fold-0 first 10 epochs

Job906_0 remains RUNNING on RTX5090. All scalar train losses are finite and
the backbone remains trainable for every epoch as registered.

A16 selected within epochs1--10: epoch4, Macro-F1 0.5522557246650255,
accuracy 0.8292079207920792, QWK 0.666555023923445, class F1
[0, 0.631578947368421, 0.8877887788778878, 0.6896551724137931], no severe
errors. Confusion matrix:
[[0,1,0,0],[0,36,4,0],[0,37,269,5],[0,0,22,30]].

Matched A5 first10 selected epoch7: Macro-F1 0.5452488631717199, accuracy
0.8217821782178217, QWK 0.6538131962296487, class F1
[0, 0.6086956521739131, 0.8826446280991735, 0.6896551724137931]. Both arms
have seven AMP-skipped updates. A16 is only 0.0070068614933056 higher.

At epoch10, A16 Macro-F1 is 0.48390220442083576 with 11 severe errors and
35 false class-A predictions, versus A5 epoch10 Macro-F1 0.5333565260660726
and one severe error. This is an unstable intermediate epoch, not the selected
checkpoint, but it warrants monitoring. A16 remains far below the 0.75 gate.
Continue the registered full50 unchanged; do not submit folds1--4. Next report
at epoch20.
