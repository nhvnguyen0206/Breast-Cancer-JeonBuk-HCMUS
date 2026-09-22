# A15 warm-up5 — fold-0 first 20 epochs

Job905_0 remains RUNNING on RTX5090. All scalar train losses are finite.
History proves epochs1--5 frozen and epochs6--20 unfrozen as preregistered.

A15 selected within epochs1--20: epoch17, Macro-F1 0.6286564490092774,
accuracy 0.8366336633663366, QWK 0.6659156279961649, class F1
[0.3333333333333333, 0.631578947368421, 0.8985507246376812,
0.6511627906976745], one severe error. Its confusion matrix is
[[1,0,0,0],[3,30,7,0],[1,25,279,6],[0,0,24,28]]. Epoch20 Macro-F1 is
0.56677234030271.

Matched A5 first20 selected epoch20: Macro-F1 0.7654421854687274,
accuracy 0.7970297029702971, QWK 0.6126648582920213, class F1
[1.0, 0.6086956521739131, 0.8637873754152824, 0.5892857142857143], no
severe errors. A15/A5 AMP-skipped updates are 10/11.

A15 trails A5 by 0.13678573645945 Macro-F1 at the matched horizon and remains
below the 0.75 expansion gate. A15 has higher accuracy, QWK, and B/C/D F1,
whereas A5's higher Macro-F1 depends heavily on correctly classifying the single
fold-0 class-A case. Continue the preregistered full50 unchanged; do not submit
folds1--4. Next report at epoch30.
